"""Wrapper around the Gemini chat model (class diagram: LLM / GeminiModel).

Provider errors are translated into ``LLMError`` with a ``kind`` the UI can turn into a
friendly message (FR-08, NFR-04). The configured model is never swapped for a paid one.
"""

import logging
import time
from collections.abc import Callable

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import SecretStr

logger = logging.getLogger(__name__)

QUOTA = "quota"
UNAVAILABLE = "unavailable"
AUTH = "auth"
EMPTY = "empty"
OTHER = "other"

_MARKERS = [
    (QUOTA, ("429", "RESOURCE_EXHAUSTED", "quota")),
    (AUTH, ("401", "403", "API_KEY_INVALID", "API key not valid", "PERMISSION_DENIED")),
    (UNAVAILABLE, ("503", "UNAVAILABLE", "500", "INTERNAL", "DEADLINE_EXCEEDED", "timed out", "Timeout")),
]


class LLMError(RuntimeError):
    def __init__(self, kind: str, message: str) -> None:
        super().__init__(message)
        self.kind = kind


def classify_error(exc: Exception) -> str:
    text = f"{type(exc).__name__} {exc}"
    return next((kind for kind, markers in _MARKERS if any(m in text for m in markers)), OTHER)


def _text(reply) -> str:
    content = getattr(reply, "text", None)  # a str property in langchain-core 1.x
    if not isinstance(content, str):
        content = reply.content if isinstance(reply.content, str) else str(reply.content)
    return content.strip()


class GeminiModel:
    def __init__(
        self,
        model_name: str,
        api_key: SecretStr | None,
        temperature: float = 0.0,
        timeout: float = 30.0,
        max_retries: int = 1,
        retry_wait_seconds: float = 2.0,
        reasoning_effort: str | None = None,
        client: BaseChatModel | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        if not model_name:
            raise ValueError("model_name is required (GEMINI_CHAT_MODEL)")
        self.model_name = model_name
        self.max_retries = max_retries
        self.retry_wait_seconds = retry_wait_seconds
        self._sleep = sleep
        if client is None:
            if api_key is None or not api_key.get_secret_value():
                raise LLMError(AUTH, "GEMINI_API_KEY is not set")
            from langchain_google_genai import ChatGoogleGenerativeAI

            client = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key.get_secret_value(),
                temperature=temperature,
                timeout=timeout,
                max_retries=0,  # retries are handled here, only for temporary unavailability
                # None keeps the model default. EXP-003 showed no consistent latency gain from "minimal"/"low".
                reasoning_effort=reasoning_effort,
            )
        self._client = client

    def generate_response(self, prompt: str, system_prompt: str | None = None) -> str:
        """Return the model's answer text. Only a temporarily unavailable service is retried."""
        messages = ([SystemMessage(system_prompt)] if system_prompt else []) + [HumanMessage(prompt)]
        for attempt in range(self.max_retries + 1):
            try:
                text = _text(self._client.invoke(messages))
            except Exception as exc:  # provider SDKs raise several error types
                kind = classify_error(exc)
                if kind == UNAVAILABLE and attempt < self.max_retries:
                    logger.warning("Gemini temporarily unavailable, retrying")
                    self._sleep(self.retry_wait_seconds)
                    continue
                raise LLMError(kind, f"Gemini request failed ({kind}): {type(exc).__name__}") from exc
            if not text:
                raise LLMError(EMPTY, "Gemini returned an empty answer")
            return text
        raise AssertionError("unreachable")
