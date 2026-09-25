import requests
import json
from config import config

# ---------------------------------------------------------------------------
# Token estimation constant (rough: 1 token ≈ 4 characters)
# ---------------------------------------------------------------------------
CHARS_PER_TOKEN = 4
MAX_HISTORY_TOKENS = 3000    # Summarize when history exceeds this limit
RECENT_MESSAGES_TO_KEEP = 4  # Always preserve the last N messages verbatim

class ConversationMemory:
    """
    Stores conversation history for the backend session.
    Summarizes old messages when the context gets too long.
    """

    def __init__(self):
        self.history = []

    def add_user_message(self, message: str):
        self.history.append({"role": "user", "content": message})
        self._maybe_summarize()

    def add_ai_message(self, message: str):
        self.history.append({"role": "assistant", "content": message})
        self._maybe_summarize()

    def get_history(self) -> list:
        return self.history

    def clear(self):
        self.history = []

    def _estimate_tokens(self) -> int:
        """Rough token count based on total character length."""
        total_chars = sum(len(m["content"]) for m in self.history)
        return total_chars // CHARS_PER_TOKEN

    def _maybe_summarize(self):
        if self._estimate_tokens() <= MAX_HISTORY_TOKENS:
            return

        if len(self.history) <= RECENT_MESSAGES_TO_KEEP:
            return

        old_messages = self.history[:-RECENT_MESSAGES_TO_KEEP]
        recent_messages = self.history[-RECENT_MESSAGES_TO_KEEP:]

        summary_text = self._summarize_with_llm(old_messages)

        summary_entry = {
            "role": "assistant",
            "content": f"[Earlier conversation summary: {summary_text}]"
        }
        self.history = [summary_entry] + recent_messages

    def _summarize_with_llm(self, messages: list) -> str:
        """
        Uses the LLM provider to produce a concise summary of old conversation turns.
        """
        if not config.GROQ_API_KEY:
            return " | ".join(f"{m['role']}: {m['content'][:80]}" for m in messages[-6:])

        transcript = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages)

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {config.GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": config.LLM_MODEL,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are a conversation summarizer. "
                                "Summarize the following conversation turns into 2-3 concise sentences. "
                                "Be factual and brief."
                            )
                        },
                        {"role": "user", "content": transcript}
                    ],
                    "temperature": 0.0,
                    "max_tokens": 200
                },
                timeout=10
            )
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return " | ".join(f"{m['role']}: {m['content'][:80]}" for m in messages[-4:])

# Global memory instance shared across the entire backend session
global_memory = ConversationMemory()
