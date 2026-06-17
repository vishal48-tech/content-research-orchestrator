import os
from langsmith import traceable
from openai import OpenAI
# from src.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL
from src.config import GROQ_API_KEY, GROQ_BASE_URL, LANGSMITH_API_KEY, LANGSMITH_PROJECT, LANGSMITH_TRACING

MODEL = os.getenv("MODEL", "nex-agi/nex-n2-pro:free")

# client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=OPENROUTER_API_KEY)
client = OpenAI(base_url=GROQ_BASE_URL, api_key=GROQ_API_KEY)

@traceable(run_type="llm", name="llm_chat")
def chat(prompt: str, max_tokens: int = 500, temperature: float = 0.2, stream: bool = False):
    try:
        return client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            stream=stream,
        )
    except Exception as e:
        raise RuntimeError(f"OpenRouter API error: {e}") from e