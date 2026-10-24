"""Wrapper around the Gemini chat model (class diagram: LLM / GeminiModel)."""

from pydantic import SecretStr


class GeminiModel:
    def __init__(self, model_name: str, api_key: SecretStr | None) -> None:
        if not model_name:
            raise ValueError("model_name is required (GEMINI_CHAT_MODEL)")
        self.model_name = model_name
        self._api_key = api_key

    def generate_response(self, prompt: str) -> str:
        raise NotImplementedError("GeminiModel.generate_response is implemented in Sprint 3")
