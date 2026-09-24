




# Central configuration for the entire project.
# Change settings here to experiment without modifying the source code.

import os
import sys

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")

# 1. ลองปิดทีละตัวแล้วรัน evaluation ดูว่าคะแนนเปลี่ยนไปแค่ไหน

USE_HYBRID = True            # ค้นด้วย BM25 ควบคู่กับ dense (ปิด = dense อย่างเดียว)
USE_RERANK = True            # จัดอันดับใหม่ด้วย cross-encoder — แม่นขึ้นแต่ช้ามาก
USE_QUERY_TRANSFORM = False      # แปลงคำถามก่อนค้น — เสีย LLM เพิ่ม 1 ครั้งต่อคำถาม
USE_MEMORY = True              # จำบทสนทนา เพื่อตอบคำถามต่อเนื่องได้
USE_LLM = True              # False = แสดงข้อความที่ค้นได้ดิบ ๆ ไม่เรียก LLM เลย
SHOW_SOURCES =  False        # True = แสดงรายการแหล่งอ้างอิงท้ายคำตอบ
SHOW_DEBUG = False          # True = แสดงคะแนนและเวลาของแต่ละขั้น


# 2. ที่อยู่ไฟล์
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
VECTOR_DB_DIR = os.path.join(BASE_DIR, "vector_db")


# clack python build_index.py
SOURCE_FILE = os.path.join(DATA_DIR, "portfolio_qa_en.txt")
GOLDEN_SET_FILE = os.path.join(DATA_DIR, "portfolio_golden_set.json")

# ผลลัพธ์ระหว่างทางจาก build_index.py
EXTRACTED_TEXT_FILE = os.path.join(OUTPUT_DIR, "extracted_text.json")
CHUNKS_FILE = os.path.join(OUTPUT_DIR, "chunks.json")
EMBEDDINGS_FILE = os.path.join(OUTPUT_DIR, "embeddings.npy")
RETRIEVAL_RESULTS_FILE = os.path.join(OUTPUT_DIR, "retrieval_results.json")
EVAL_RETRIEVAL_FILE = os.path.join(OUTPUT_DIR, "eval_retrieval.json")
EVAL_GENERATION_FILE = os.path.join(OUTPUT_DIR, "eval_generation.json")

# ฐานข้อมูลที่ระบบใช้ค้นจริง
FAISS_INDEX_FILE = os.path.join(VECTOR_DB_DIR, "document.index")
CHUNK_STORE_FILE = os.path.join(VECTOR_DB_DIR, "chunk_store.json")
BM25_INDEX_FILE = os.path.join(VECTOR_DB_DIR, "bm25_index.pkl")
INDEX_META_FILE = os.path.join(VECTOR_DB_DIR, "index_meta.json")

# 3. การเตรียมข้อมูล  (แก้แล้วต้องรัน build_index.py ใหม่)
CHUNK_SIZE = 400        # ตัวอักษรต่อ chunk (คำตอบส่วนใหญ่สั้นกว่านี้อยู่แล้ว)
CHUNK_OVERLAP = 50      # ให้ chunk ที่ติดกันเหลื่อมกัน กันใจความขาดตอน

# ตัวโมเดลจริงถูกดาวน์โหลดไปเก็บที่ C:\Users\----\.cache\huggingface
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# 4. การค้นหา
TOP_K = 3               # ส่งกี่ chunk ให้ LLM เขียนคำตอบ
CANDIDATE_K = 30        # ดึง TOP_K
RRF_K = 60              # ค่าคงที่ของสูตร RRF 

RERANK_MODEL_NAME = "BAAI/bge-reranker-v2-m3"   # ใช้เมื่อ USE_RERANK = True

QUERY_TRANSFORM_MODE = "multi_query"   # rewrite | multi_query | hyde
MULTI_QUERY_COUNT = 3

# 5. LLM
os.environ["GROQ_API_KEY"] = "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"

LLM_PROVIDER = "groq"
LLM_MODEL = ""          # เว้นว่าง = ใช้ค่า default 
LLM_TEMPERATURE = 0.2   # เหมือนค่าเทรดโฮล 
LLM_MAX_TOKENS = 800

LLM_PROVIDERS = {
    "ollama": ("http://localhost:11434/v1", "llama3.1:8b", None),
    "groq": ("https://api.groq.com/openai/v1", "llama-3.1-8b-instant", "GROQ_API_KEY"),
}

# 6. ข้อความและการวัดผล
MEMORY_MAX_TURNS = 6    # จำนวนรอบของการจำบทสนทนา
NO_CONTEXT_MESSAGE = "Sorry, there's no related answer."
DISCLAIMER = ""

EVAL_K_VALUES = [1, 3, 5, 10]
GOLDEN_SET_SIZE = 60


# create output directories if they don't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VECTOR_DB_DIR, exist_ok=True)
