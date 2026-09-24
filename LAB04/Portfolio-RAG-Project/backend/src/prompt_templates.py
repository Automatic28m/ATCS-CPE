# prompt_templates.py
# Store all prompt templates in one place.
# Makes prompts easier to manage, compare, and update.
# Answers must be based only on the retrieved context.
# Inline citations are required for traceable and verifiable responses.


import config

SYSTEM_PROMPT = """You are Phanlop Boonluea. You are answering questions about your own portfolio and background. Answer using ONLY the provided "Reference Data" as if they are your own memories and experiences.

Rules:
1. Synthesize and consolidate information from all references to generate one true, complete, and natural answer.
2. Use ONLY the information in the "Reference Data". Do not add outside knowledge.
3. If the information is insufficient, answer with "{no_context}". Do not guess.
4. Cite the reference numbers in the format [1], [2] at the end of the sentence that uses that data.
5. Use polite, professional, and straightforward language.
6. Keep the answer concise and cover the key points.
7. Answer in the first person ("I", "my", "me").
8. If your answer mentions a specific project or repository from the reference data, you MUST include its URL link in your response.
9. You MUST ALWAYS answer in English."""

USER_PROMPT = """{history}Reference Data:
{context}

User's Question: {question}

Answer using ONLY the reference data above, and cite using [n]."""


def format_context(chunks, max_chars=6000):
    """
    Format chunks into numbered reference blocks.

    max_chars prevents the prompt from exceeding the context window.
    Since chunks are ordered by relevance, we drop the least relevant ones at the end.
    """
    blocks, used = [], 0
    for i, chunk in enumerate(chunks, start=1):
        block = f"[{i}] {chunk.get('answer') or chunk.get('text', '')}"
        if used + len(block) > max_chars:
            break
        blocks.append(block)
        used += len(block)
    return "\n\n".join(blocks)


def build_messages(question, chunks, history=""):
    """Construct the messages list for the LLM"""
    history_block = f"Previous conversation:\n{history}\n\n" if history else ""
    return [
        {"role": "system", "content": SYSTEM_PROMPT.format(no_context=config.NO_CONTEXT_MESSAGE)},
        {
            "role": "user",
            "content": USER_PROMPT.format(
                history=history_block,
                context=format_context(chunks),
                question=question,
            ),
        },
    ]


# --------------------------------------------------- query transform
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


# ------------------------------------------- LLM judge (for evaluation)
JUDGE_PROMPT = """Evaluate the "Answer" based on the criteria {criteria}. Give a score from 1-5.
(5 = Excellent, 3 = Fair, 1 = Poor)

{reference}
Question: {question}

Answer:
{answer}

Respond ONLY with JSON format: {{"score": <1-5>, "reason": "<short reason>"}}"""
