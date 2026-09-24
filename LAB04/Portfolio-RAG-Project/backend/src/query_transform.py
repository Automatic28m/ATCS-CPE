import re
import os
from openai import OpenAI
from config import config

# Prompts for Query Transformation
REWRITE_PROMPT = """Rewrite the question to be clear and suitable for searching the portfolio database.
- Correct any spelling mistakes.
- If it is a follow-up question, add context from the previous conversation so it is self-contained.
- Output only a single-line search query, with no explanations.

{history}Original Question: {question}

Rewritten Query:"""

MULTI_QUERY_PROMPT = """Generate {n} different versions of the given question to broaden the search coverage.
- Use different phrasing and keywords.
- The meaning must remain the same as the original question.
- Output 1 question per line, without numbering.

Original Question: {question}

Generated Questions:"""

HYDE_PROMPT = """Write a "hypothetical answer" to this question in the style of a portfolio/resume document.
- Keep it 3-5 sentences long and use relevant professional keywords.
- Don't worry if the facts are incorrect, as this will only be used for search retrieval.

Question: {question}

Hypothetical Answer:"""

SLANG_MAP = {
    "Uni": "University",
    "BSc": "Bachelor's Degree",
    "Program": "Software",
    "App": "Application",
    "Work history": "Experience",
    "What you can do": "Skills",
    "AI": "Artificial Intelligence",
    "CompEng": "Computer Engineering",
    "Repo": "Repository"
}

ENDING_WORDS = re.compile(r"\s*(please|thanks|thank you|anyway)\s*$", re.IGNORECASE)

def normalize_query(query):
    text = re.sub(r"\s+", " ", query).strip()
    for slang, formal in SLANG_MAP.items():
        text = text.replace(slang, formal)
    text = ENDING_WORDS.sub("", text)
    return text.strip() or query.strip()

def clean_line(line):
    text = line.strip()
    text = re.sub(r"^\s*(\d+[\.\)]|[-*•])\s*", "", text)
    text = re.sub(r"^(คำถาม|คำค้นหา|Query)\s*[:：]\s*", "", text)
    return text.strip().strip('"').strip("'")

class QueryTransformer:
    def __init__(self, llm_placeholder=None):
        base_url, default_model, key_name = config.LLM_PROVIDERS[config.LLM_PROVIDER]
        self.model = config.LLM_MODEL or default_model
        api_key = os.getenv(key_name) if key_name else "ollama-no-key"
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def ask_llm(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=config.LLM_TEMPERATURE,
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()

    def rewrite(self, query, history):
        history_block = f"Previous conversation:\n{history}\n\n" if history else ""
        prompt = REWRITE_PROMPT.format(history=history_block, question=query)
        return [clean_line(self.ask_llm(prompt))]

    def multi_query(self, query):
        prompt = MULTI_QUERY_PROMPT.format(n=config.MULTI_QUERY_COUNT, question=query)
        answer = self.ask_llm(prompt)
        queries = [normalize_query(query)]
        for line in answer.splitlines():
            new_query = clean_line(line)
            if new_query and new_query not in queries:
                queries.append(new_query)
        return queries[: config.MULTI_QUERY_COUNT + 1]

    def hyde(self, query):
        fake_answer = self.ask_llm(HYDE_PROMPT.format(question=query)).strip()
        return [normalize_query(query), fake_answer]

    def transform(self, query, history=""):
        if not config.USE_QUERY_TRANSFORM:
            return [normalize_query(query)]

        try:
            if config.QUERY_TRANSFORM_MODE == "rewrite":
                return self.rewrite(query, history)
            if config.QUERY_TRANSFORM_MODE == "hyde":
                return self.hyde(query)
            return self.multi_query(query)
        except Exception as error:
            print(f"[query_transform] Failed ({error}) — Using original query")
            return [normalize_query(query)]
