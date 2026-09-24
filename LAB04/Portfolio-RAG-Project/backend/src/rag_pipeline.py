import time
from config import config
from src.embedding_model import EmbeddingModel
from src.hybrid_retriever import HybridRetriever
from src.rerankers import get_reranker
from src.generator import Generator
from src.query_transform import QueryTransformer
from src.memory import global_memory

class RAGPipeline:
    def __init__(self):
        print("Initializing Portfolio RAG Pipeline components...")
        self.retriever = HybridRetriever(reranker=get_reranker())
        
        # We pass the OpenAI client wrapper to QueryTransformer if needed, or instantiate it
        # Actually Portfolio's QueryTransformer expects an LLM instance. 
        # I'll modify QueryTransformer slightly if needed, or just pass a basic LLM wrapper.
        from src.generator import get_llm
        self.transformer = QueryTransformer(get_llm()) 
        
        self.generator = Generator()
        print("RAG Pipeline is online and ready!")

    def ask(self, query: str, chat_history=None):
        start_time = time.time()
        
        # ── MEMORY: load conversation history ───────────────────────────────
        if config.USE_MEMORY:
            chat_history = global_memory.get_history()

        # ── QUERY REFORMULATION: make standalone if needed ──────────────────
        if config.USE_QUERY_TRANSFORM:
            # Send history to query transformer only if it's a followup
            transform_history = chat_history if chat_history else ""
            queries = self.transformer.transform(query, transform_history)
            standalone_query = queries[0]
            print(f"[Reformulation] '{query}' → '{standalone_query}'")
        else:
            standalone_query = query
            queries = [query]
        
        time_after_transform = time.time()

        # ── RAG RETRIEVAL ───────────────────────────────────────────────────
        print(f"[Pipeline] Activating RAG retrieval.")
        chunks = self.retriever.retrieve(
            standalone_query,
            top_k=config.TOP_K,
            extra_queries=queries[1:] if len(queries) > 1 else None,
        )
        time_after_retrieve = time.time()

        # ── GENERATE: send chunks + history to LLM ──────────────────────────
        if config.USE_MEMORY:
            full_history = global_memory.get_history() + [{"role": "user", "content": query}]
        else:
            full_history = chat_history if chat_history else [{"role": "user", "content": query}]

        # generator now handles the direct system prompt replacement 
        answer = self.generator.generate(query, chunks, full_history)
        time_after_generate = time.time()

        # ── MEMORY: save exchange ────────────────────────────────────────────
        if config.USE_MEMORY:
            global_memory.add_user_message(query)
            global_memory.add_ai_message(answer)

        # ── FORMAT RESULT ───────────────────────────────────────────────────
        result = {
            "answer": answer,
            "queries_used": queries,
            "retrieved": chunks,
            "timings": {
                "transform": round(time_after_transform - start_time, 2),
                "retrieve": round(time_after_retrieve - time_after_transform, 2),
                "generate": round(time_after_generate - time_after_retrieve, 2),
                "total": round(time_after_generate - start_time, 2),
            }
        }
        return result

    def reset(self):
        global_memory.clear()

    def show_settings(self):
        settings = [
            ("Hybrid search BM25 + dense", config.USE_HYBRID),
            ("Reranking", config.USE_RERANK),
            ("Query transformation", config.USE_QUERY_TRANSFORM),
            ("Conversation memory", config.USE_MEMORY),
            ("LLM Generation", config.USE_LLM),
        ]
        print("Settings (can be edited in config.py):")
        for name, enabled in settings:
            print(f"  {'ON ' if enabled else 'OFF'}  {name}")
