import os
import sys
from dotenv import load_dotenv

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")

load_dotenv()

class Config:
    # --- Feature Toggles ---
    USE_HYBRID = True
    USE_RERANK = True
    USE_QUERY_TRANSFORM = False
    USE_MEMORY = True
    USE_LLM = True
    SHOW_SOURCES = False
    SHOW_DEBUG = False

    # --- Paths ---
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
    VECTOR_DB_DIR = os.path.join(BASE_DIR, "vector_db")

    SOURCE_FILE = os.path.join(DATA_DIR, "portfolio_qa_en.txt")
    GOLDEN_SET_FILE = os.path.join(DATA_DIR, "portfolio_golden_set.json")

    EXTRACTED_TEXT_FILE = os.path.join(OUTPUT_DIR, "extracted_text.json")
    CHUNKS_FILE = os.path.join(OUTPUT_DIR, "chunks.json")
    EMBEDDINGS_FILE = os.path.join(OUTPUT_DIR, "embeddings.npy")
    RETRIEVAL_RESULTS_FILE = os.path.join(OUTPUT_DIR, "retrieval_results.json")
    EVAL_RETRIEVAL_FILE = os.path.join(OUTPUT_DIR, "eval_retrieval.json")
    EVAL_GENERATION_FILE = os.path.join(OUTPUT_DIR, "eval_generation.json")

    FAISS_INDEX_FILE = os.path.join(VECTOR_DB_DIR, "document.index")
    CHUNK_STORE_FILE = os.path.join(VECTOR_DB_DIR, "chunk_store.json")
    BM25_INDEX_FILE = os.path.join(VECTOR_DB_DIR, "bm25_index.pkl")
    INDEX_META_FILE = os.path.join(VECTOR_DB_DIR, "index_meta.json")

    # --- Preparation ---
    CHUNK_SIZE = 400
    CHUNK_OVERLAP = 50
    EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

    # --- Retrieval ---
    TOP_K = 3
    CANDIDATE_K = 30
    RRF_K = 60
    RERANK_MODEL_NAME = "BAAI/bge-reranker-v2-m3"

    QUERY_TRANSFORM_MODE = "multi_query"
    MULTI_QUERY_COUNT = 3

    # --- LLM ---
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

    LLM_PROVIDER = "groq"
    LLM_MODEL = "openai/gpt-oss-120b"
    LLM_TEMPERATURE = 0.2
    LLM_MAX_TOKENS = 800

    LLM_PROVIDERS = {
        "ollama": ("http://localhost:11434/v1", "llama3.1:8b", None),
        "groq": ("https://api.groq.com/openai/v1", "openai/gpt-oss-120b", "GROQ_API_KEY"),
    }

    # --- Messages and Evaluation ---
    MEMORY_MAX_TURNS = 6
    NO_CONTEXT_MESSAGE = "Sorry, there's no related answer."
    DISCLAIMER = ""

    EVAL_K_VALUES = [1, 3, 5, 10]
    GOLDEN_SET_SIZE = 60
    
    SYSTEM_PROMPT = """You are Phanlop Boonluea, speaking directly to the user as yourself. You are sharing your own portfolio, skills, and experiences. Be friendly, humble, and professional.

Rules:
1. If the user is simply greeting you (e.g., "Hello", "Hi", "สวัสดี", "สวัสดีจ้า"), respond with a friendly greeting in character as yourself, welcoming them to your portfolio.
2. For specific questions about skills or experience, answer proudly but humbly using ONLY the provided context as your own memory/experience.
3. Do not add outside knowledge or make up experiences that are not in the context.
4. If the user asks a factual question and the context is insufficient, you MUST answer EXACTLY with:
   - "Sorry, there's no related answer." (if the user asked in English)
   - "ขออภัยครับ ไม่มีข้อมูลที่เกี่ยวข้องครับ" (if the user asked in Thai)
   Do not guess or apologize further.
5. Keep the answer concise and cover the key points naturally.
6. If your answer mentions a specific project or repository from the context, you MUST include its URL link.
7. Always answer in the same language that the user used (e.g., if they ask in Thai, reply in Thai).

Context:
{context}
"""

config = Config()

os.makedirs(config.OUTPUT_DIR, exist_ok=True)
os.makedirs(config.VECTOR_DB_DIR, exist_ok=True)
