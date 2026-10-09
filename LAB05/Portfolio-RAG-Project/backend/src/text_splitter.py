


# text_splitter.py
# Split long documents into smaller chunks before generating embeddings.
# Smaller chunks produce more focused embeddings and improve retrieval accuracy.
# Most answers fit into a single chunk; only long answers are split.



def split_text(text, chunk_size, overlap):
# Split text into chunks of chunk_size characters.
# Adjacent chunks overlap by overlap characters.
# This preserves context across chunk boundaries.




    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        
        if end < len(text):
            # Find the last space before the chunk boundary to prevent cutting URLs in half
            last_space = text.rfind(' ', start, end)
            if last_space != -1 and last_space > start + (chunk_size // 2):
                end = last_space
                
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
            
        start = end - overlap
    return chunks


def build_chunks(records, chunk_size, overlap):
# Build chunks from Q&A records and attach metadata.
# Each embedding uses the combined question and answer text.
# This improves retrieval from both questions and answers.



    chunks = []
    for record in records:
        full_text = f"Question: {record['question']} Answer: {record['answer']}"

        for part_idx, piece in enumerate(split_text(full_text, chunk_size, overlap)):
            chunks.append({
                "chunk_id": len(chunks),
                "qa_id": record["id"],
                "category": record["category"],
                "question": record["question"],
                "answer": record["answer"],
                "text": piece,
                "part_idx": part_idx,
                "line_no": record["line_no"],
            })
    return chunks
