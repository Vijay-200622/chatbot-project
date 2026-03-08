"""HuggingFace Inference API wrapper for LLM calls."""

import logging
from huggingface_hub import InferenceClient

from backend.config import settings

logger = logging.getLogger(__name__)

# Initialize client (lazy — only fails when actually called without token)
_client: InferenceClient | None = None


def _get_client() -> InferenceClient:
    global _client
    if _client is None:
        _client = InferenceClient(token=settings.hf_api_token or None)
    return _client


def generate_response(
    user_message: str,
    system_prompt: str,
    max_tokens: int = 1024,
    temperature: float = 0.7,
) -> str:
    """Generate a text response using HuggingFace Inference API.

    Tries the primary model first, falls back to the secondary model on failure.
    """
    client = _get_client()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    for model_id in [settings.hf_model, settings.hf_fallback_model]:
        try:
            response = client.chat_completion(
                model=model_id,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
        except Exception as e:
            logger.warning(f"Model {model_id} failed: {e}")
            continue

    return (
        "Sorry, the AI model is not responding right now. "
        "Please try again in a moment! \U0001f64f"
    )


def generate_with_context(
    user_message: str,
    system_prompt: str,
    conversation_history: list[dict] | None = None,
    max_tokens: int = 1024,
    temperature: float = 0.7,
) -> str:
    """Generate response with optional conversation history."""
    client = _get_client()

    messages = [{"role": "system", "content": system_prompt}]
    if conversation_history:
        # Keep last 6 messages to stay within context limits
        messages.extend(conversation_history[-6:])
    messages.append({"role": "user", "content": user_message})

    for model_id in [settings.hf_model, settings.hf_fallback_model]:
        try:
            response = client.chat_completion(
                model=model_id,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
        except Exception as e:
            logger.warning(f"Model {model_id} failed: {e}")
            continue

    return (
        "Sorry, the AI model is not responding right now. "
        "Please try again in a moment! 🙏"
    )
