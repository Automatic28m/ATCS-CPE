# Portfolio RAG System

This project is a complete full-stack Retrieval-Augmented Generation (RAG) system for a personal portfolio. It consists of a **FastAPI Python Backend** (powered by FAISS, BM25, and LLMs) and a **Next.js Frontend** user interface.

## 🚀 Key Backend Features
- **Hybrid Retrieval:** Combines FAISS (dense embeddings) and BM25 (keyword search) via Reciprocal Rank Fusion (RRF).
- **Advanced Deduplication:** Automatically cleans redundant chunks from the Q&A dataset.
- **Smart Query Routing:** Dynamically bypasses HyDE (Hypothetical Document Embeddings) for factual queries to prevent hallucinations.
- **Temporal Boost:** Automatically sorts chronological data (e.g., "What is your most recent project?") by extracting dates from chunks.
- **Metadata Filtering:** Extracts intents (like "Education" or "Certificate") to dynamically filter the vector space during retrieval.

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
