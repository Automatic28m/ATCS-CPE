import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from config import config
from src import index_meta
from src.rag_pipeline import RAGPipeline

app = FastAPI(title="RAG Backend API")

# Configure CORS to allow frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production to match your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Pipeline globally
rag_pipeline = None

@app.on_event("startup")
def startup_event():
    global rag_pipeline
    print("--- Starting RAG System ---")
    if not os.path.exists(config.FAISS_INDEX_FILE):
        print("Vector database not found. Please run: python build_index.py")
    else:
        # Check if index needs rebuild
        index_meta.warn_if_stale()
        rag_pipeline = RAGPipeline()
        print("RAG Pipeline initialized successfully.")

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask_question(req: QueryRequest):
    if not rag_pipeline:
        return {"error": "RAG Pipeline is not initialized. Please build the index first."}
    
    if not req.query.strip():
        return {"error": "Query cannot be empty."}

    result = rag_pipeline.ask(req.query.strip())
    
    # Return the answer along with debug info if needed
    return {
        "answer": result.get("answer", ""),
        "queries_used": result.get("queries_used", []),
        "timings": result.get("timings", {})
    }

@app.get("/health")
def health_check():
    return {"status": "ok", "rag_initialized": rag_pipeline is not None}

if __name__ == "__main__":
    # Open the port on 0.0.0.0 to accept connections from any interface
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
