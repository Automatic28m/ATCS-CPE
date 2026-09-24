import json
import os
import sys
import time

# Add the project root so imports like `src.generator` work when running this file directly.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.generator import LLM


def format_fallback_entry(item):
    title = (item.get("title") or "Portfolio item").strip()
    contents = (item.get("contents") or "").strip()
    location = (item.get("event_location") or "").strip()
    date = (item.get("event_date") or "").strip()

    if item.get("portfolio_type_id") == 6:
        category = "Education"
        question = f"What is {title}?"
        answer_parts = [f"{title} is an education milestone."]
        if contents:
            answer_parts.append(f"It includes {contents}.")
        if location:
            answer_parts.append(f"It was completed at {location}.")
        if date:
            answer_parts.append(f"Date: {date}.")
    else:
        category = "Skills"
        question = f"What can you say about {title}?"
        answer_parts = [f"{title} is listed as one of the portfolio skills."]
        if contents:
            answer_parts.append(f"Details: {contents}.")
        if location:
            answer_parts.append(f"Associated location: {location}.")
        if date:
            answer_parts.append(f"Date: {date}.")

    answer = " ".join(answer_parts).strip()
    return f"[Category: {category}]\nQ: {question}\nA: {answer}"


def main():
    print("=== Portfolio Translation Service ===")

    input_file = os.path.join(config.DATA_DIR, "portfolio_202607221027.json")
    output_file = os.path.join(config.DATA_DIR, "portfolio_qa_en.txt")

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print(f"Loading data from {input_file}")
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    portfolio_items = data.get("portfolio", [])
    print(f"Found {len(portfolio_items)} items to translate.")

    try:
        llm = LLM()
        print(f"Initialized LLM ({config.LLM_PROVIDER}: {llm.model})")
    except Exception as e:
        print(f"Failed to initialize LLM: {e}")
        llm = None

    system_prompt = (
        "You are a helpful translation assistant. I will provide you with a JSON object representing "
        "a portfolio entry. Please translate its content into natural English and format it strictly "
        "as a Q&A pair suitable for a RAG knowledge base. "
        "\n\nOutput format MUST be exactly:\n"
        "[Category: <Category Name in English>]\n"
        "Q: <A natural question someone might ask about this entry in English>\n"
        "A: <A detailed answer based on the JSON fields in English>\n"
        "\nDo NOT include any markdown formatting, code blocks, or extra text. Just the 3 lines above."
    )

    print(f"Output will be saved to {output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Portfolio Q&A Knowledge Base (English Auto-translated)\n")
        f.write("# ================================================================\n\n")

    for idx, item in enumerate(portfolio_items, start=1):
        print(f"\nProcessing item {idx}/{len(portfolio_items)} (ID: {item.get('id')})...")

        clean_item = {k: v for k, v in item.items() if v}
        item_json_str = json.dumps(clean_item, ensure_ascii=False, indent=2)
        prompt = f"Please translate and format the following JSON entry:\n{item_json_str}"

        response = ""
        if llm is not None:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]
            try:
                response = llm.chat(messages).strip()
            except Exception as e:
                print(f"Error processing item {idx}: {e}")

        if not response:
            response = format_fallback_entry(item)
            print("Using fallback entry instead...")

        print("-" * 40)
        print(response)
        print("-" * 40)

        with open(output_file, "a", encoding="utf-8") as f:
            f.write(response + "\n\n")

        if config.LLM_PROVIDER != "ollama":
            time.sleep(1)

    print(f"\n✅ Translation complete! Data saved to {output_file}")
    print("Don't forget to update config.SOURCE_FILE to point to this new file!")


if __name__ == "__main__":
    main()
