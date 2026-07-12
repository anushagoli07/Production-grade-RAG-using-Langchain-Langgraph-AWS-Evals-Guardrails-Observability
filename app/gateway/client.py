import logfire
from groq import Groq

from app.config import settings

primary_client = Groq(api_key=settings.GROQ_API_KEY)
fallback_client = Groq(api_key=settings.GROQ_FALLBACK_API_KEY)

PRIMARY_MODEL = settings.GROQ_MODEL          # llama-3.3-70b-versatile
FALLBACK_MODEL = "llama-3.1-8b-instant"


def get_groq_completion(messages, temperature: float = 0.0):
    """
    Calls Groq directly. Tries the primary key/model first; on any
    failure (rate limit, 5xx, timeout) falls back to the secondary
    key/model. Returns (response, used_fallback: bool).
    """
    try:
        response = primary_client.chat.completions.create(
            model=PRIMARY_MODEL,
            messages=messages,
            temperature=temperature,
        )
        return response, False
    except Exception as e:
        logfire.warning(f"Primary Groq call failed, falling back: {e}")
        response = fallback_client.chat.completions.create(
            model=FALLBACK_MODEL,
            messages=messages,
            temperature=temperature,
        )
        return response, True