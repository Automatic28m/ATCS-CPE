import os
from openai import OpenAI
from config import config

class Generator:
    def __init__(self):
        base_url, default_model, key_name = config.LLM_PROVIDERS[config.LLM_PROVIDER]
        self.model = config.LLM_MODEL or default_model
        
        # Load API Key
        api_key = os.getenv(key_name) if key_name else "ollama-no-key"
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def generate(self, query, context_chunks, chat_history=None):
        if not config.USE_LLM:
            return "DEBUG MODE (LLM OFF):\n\n" + "\n\n".join([f"[{c.get('metadata', {}).get('situation', 'Source')}] {c.get('text', c.get('answer', ''))}" for c in context_chunks])

        # Build context string from retrieved chunks
        context_str = "\n\n".join([f"Source [{i+1}]: {c.get('text', c.get('answer', ''))}" for i, c in enumerate(context_chunks)])
        system_prompt = config.SYSTEM_PROMPT.replace("{context}", context_str)
        
        messages = [{"role": "system", "content": system_prompt}]
        
        if chat_history:
            recent_history = chat_history[-6:]
            for msg in recent_history:
                # Ensure correct role names for OpenAI spec
                role = "assistant" if msg["role"] == "ai" else msg["role"]
                messages.append({"role": role, "content": msg["content"]})
        else:
            messages.append({"role": "user", "content": query})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=config.LLM_TEMPERATURE,
                max_tokens=config.LLM_MAX_TOKENS,
            )
            return response.choices[0].message.content.strip()
        except Exception as error:
            print(f"[Generator] Generation Failed ({error}) — Returning raw chunks instead.")
            return "\n\n".join([f"[{i+1}] {c.get('text', c.get('answer', ''))}" for i, c in enumerate(context_chunks)])

# Helper to maintain compatibility if anything imports get_llm
def get_llm():
    return Generator()
