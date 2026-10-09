# Portfolio RAG System

This project is a complete full-stack Retrieval-Augmented Generation (RAG) system for a personal portfolio. It consists of a **FastAPI Python Backend** (powered by FAISS, BM25, and LLMs) and a **Next.js Frontend** user interface.

## 🚀 Key Backend Features
- **Hybrid Retrieval:** Combines FAISS (dense embeddings) and BM25 (keyword search) via Reciprocal Rank Fusion (RRF).
- **Advanced Deduplication:** Automatically cleans redundant chunks from the Q&A dataset.
- **Smart Query Routing:** Dynamically bypasses HyDE (Hypothetical Document Embeddings) for factual queries to prevent hallucinations.
- **Temporal Boost:** Automatically sorts chronological data (e.g., "What is your most recent project?") by extracting dates from chunks.
- **Metadata Filtering:** Extracts intents (like "Education" or "Certificate") to dynamically filter the vector space during retrieval.

---

## 🔧 7 Solved RAG Pipeline Problems & Fixes

During the development of this system, we encountered and solved 7 advanced RAG challenges:

### 1. Data Quality (Missing Deduplication)
**Problem:** The raw dataset contained overlapping or identical Q&A pairs, causing redundant information to flood the top retrieved results.
**Solution:** Added a Cosine Similarity check before building the FAISS index to automatically drop chunks that are 98% identical to existing ones.
```python
# build_index.py snippet
sims = cosine_similarity([new_embedding], unique_embeddings)[0]
if max(sims) <= 0.98:
    unique_embeddings.append(new_embedding)
```

### 2. Metadata Filtering Gap
**Problem:** The vector search blindly searched the entire database, completely ignoring the category metadata attached to the chunks.
**Solution:** Implemented Self-Querying logic in `rag_pipeline.py` to extract categories, and updated `hybrid_retriever.py` to apply the filter post-retrieval.
```python
# hybrid_retriever.py snippet
if filter_category and filter_category.lower() not in chunk.get("category", "").lower():
    continue # Skip non-matching chunks
```

### 3. Technical Keyword Destruction (BM25)
**Problem:** The English tokenizer aggressively stripped special characters, breaking crucial searches for "C++", "C#", and "React.js".
**Solution:** Upgraded the BM25 regular expression to mathematically preserve symbols like `+` and `#`.
```python
# hybrid_retriever.py snippet
ENGLISH_PATTERN = re.compile(r"[A-Za-z0-9\+#\.]+") 
```

### 4. HyDE Factual Drift
**Problem:** Hypothetical Document Embeddings (HyDE) hallucinated fake facts (e.g., fake TOEIC scores) to help semantic search, which distorted factual lookups.
**Solution:** Built a heuristic detector to bypass HyDE for factual queries (scores, dates, grades), routing them to a standard rewriter instead.
```python
# query_transform.py snippet
if self.is_factual_query(query):
    return self.rewrite(query, history) # Bypass HyDE to prevent drift
return self.hyde(query)
```

### 5. Temporal Blindness
**Problem:** FAISS purely relies on semantic similarity and had no concept of time, failing on queries for "the most recent" projects.
**Solution:** Implemented regex to extract years from text chunks and applied a mathematical scalar boost to the Reciprocal Rank Fusion (RRF) score for newer dates.
```python
# hybrid_retriever.py snippet
if "recent" in query.lower():
    years = re.findall(r"\b(20\d{2})\b", chunk["text"])
    if years:
        recency_boost = max(0.0, 0.5 - ((current_year - max(int(y) for y in years)) * 0.1)) 
        chunk["score"] += recency_boost
```

### 6. Aggressive Metadata Over-Filtering
**Problem:** Simple intent triggers caused category collisions. E.g., asking "Do you have experience in Next.js?" triggered the `Experience` filter, completely blocking `Web Application` chunks.
**Solution:** Dropped broad single-word matches (like "experience") and upgraded the pipeline to require strict compound phrases ("work experience", "internship").

### 7. Chunk Boundary URL Destruction
**Problem:** The text splitter sliced chunks exactly at 400 characters. If the 400th character landed in the middle of a URL (e.g., "https:/"), the URL was destroyed.
**Solution:** Upgraded the text splitter to scan backwards from the 400th character to find the closest space character, guaranteeing chunks only break on whole words.
```python
# text_splitter.py snippet
last_space = text.rfind(' ', start, start + chunk_size)
if last_space != -1:
    end = last_space # Safely break at the space instead of cutting the URL
```

---

## 🛠️ Part 1: Backend Setup & Execution

### 1. Activate the Virtual Environment
Navigate to the `backend` folder and activate the Python virtual environment:
```bash
cd backend

# On macOS/Linux
source ../.venv/bin/activate

# On Windows
..\.venv\Scripts\activate
```

### 2. Configure Environment Variables
Rename the `.env.example` file to `.env`:
```bash
mv .env.example .env
```
Open `.env` and fill in your API keys:
- **`GROQ_API_KEY`**: Required for the LLM to generate answers.
- **`HF_TOKEN`**: Recommended for downloading HuggingFace models without rate limits.

### 3. Build the Vector Database
Before you can ask questions, ingest the dataset and build the FAISS/BM25 indices:
```bash
python3 build_index.py
```

### 4. Start the Backend API
Run the FastAPI server:
```bash
python3 main.py
```
*The API will start running at `http://0.0.0.0:8000`.*

*(Optional) You can also run `python3 evaluate_system.py` to test the pipeline logic without the frontend.*

---

## 💻 Part 2: Frontend Setup & Execution

Open a **new terminal tab/window** (leave the backend running) and navigate to the frontend directory:
```bash
cd frontend/portfolio-rag
```

### 1. Install Dependencies
Install the required Node.js packages (you only need to do this once):
```bash
npm install
```

### 2. Start the Frontend Application
Run the Next.js development server:
```bash
npm run dev
```

*The frontend UI will now be available in your browser at `http://localhost:3000`!*
