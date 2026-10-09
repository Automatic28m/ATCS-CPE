from src.rag_pipeline import RAGPipeline

def evaluate():
    pipeline = RAGPipeline()
    q = "Can you give me the GitHub link and the thumbnail URL for the Air Monitor Pro project?"
    print(f"\nQuery: '{q}'")
    res = pipeline.ask(q)
    print("Retrieved Chunks:")
    for idx, c in enumerate(res['retrieved']):
        print(f"  {idx+1}. [Cat: {c.get('category')}] {c.get('question')} (Score: {c.get('score', 0):.4f})")
        print(f"     Text Preview: {c.get('text')[:150]}...")

if __name__ == "__main__":
    evaluate()
