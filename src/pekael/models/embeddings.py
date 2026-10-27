"""Gemini embeddings for retrieval (spec §4.1 step 9, §4.3 step 3; D-05).

Supporting component of FaissVectorStore: documents use task type RETRIEVAL_DOCUMENT and
questions RETRIEVAL_QUERY, every vector has the configured dimension, and vectors are
L2-normalised so FAISS L2 distance ranks like cosine similarity.
"""

import logging
import math
import time
from collections.abc import Callable, Sequence

from langchain_core.embeddings import Embeddings
from pydantic import SecretStr

from pekael.config.settings import AppConfig

logger = logging.getLogger(__name__)

DOCUMENT_TASK = "RETRIEVAL_DOCUMENT"
QUERY_TASK = "RETRIEVAL_QUERY"
# Errors worth waiting for: free-tier quota (429) and temporary overload (503).
RETRYABLE_MARKERS = ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE")
# gemini-embedding-001 accepts about 2,048 tokens and silently truncates longer input
# (a 40,000-character text was accepted in Sprint 2). ~8,000 characters stays below that limit.
DEFAULT_MAX_INPUT_CHARS = 8000


class EmbeddingError(RuntimeError):
    """Embedding failed: missing key, quota still exhausted after retries, or an invalid result."""


def l2_normalize(vector: Sequence[float]) -> list[float]:
    norm = math.sqrt(sum(v * v for v in vector))
    if norm == 0:
        raise EmbeddingError("Embedding service returned a zero vector")
    return [v / norm for v in vector]


class GeminiEmbeddings(Embeddings):
    def __init__(
        self,
        model: str,
        api_key: SecretStr | None,
        output_dimensionality: int,
        normalize: bool = True,
        batch_size: int = 50,
        max_retries: int = 3,
        retry_wait_seconds: float = 20.0,
        max_input_chars: int = DEFAULT_MAX_INPUT_CHARS,
        client: Embeddings | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        if client is None:
            if api_key is None or not api_key.get_secret_value():
                raise EmbeddingError("GEMINI_API_KEY is not set")
            from langchain_google_genai import GoogleGenerativeAIEmbeddings

            client = GoogleGenerativeAIEmbeddings(model=model, google_api_key=api_key.get_secret_value())
        self.model = model
        self.output_dimensionality = output_dimensionality
        self.normalize = normalize
        self.batch_size = batch_size
        self.max_retries = max_retries
        self.retry_wait_seconds = retry_wait_seconds
        self.max_input_chars = max_input_chars
        self._client = client
        self._sleep = sleep

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        for text in texts:
            self._check_length(text)
        vectors: list[list[float]] = []
        for start in range(0, len(texts), self.batch_size):
            batch = texts[start : start + self.batch_size]
            vectors.extend(
                self._call(
                    lambda b=batch: self._client.embed_documents(
                        b, task_type=DOCUMENT_TASK, output_dimensionality=self.output_dimensionality
                    )
                )
            )
        if len(vectors) != len(texts):
            raise EmbeddingError(f"Expected {len(texts)} vectors, received {len(vectors)}")
        return [self._finish(v) for v in vectors]

    def embed_query(self, text: str) -> list[float]:
        self._check_length(text)
        vector = self._call(
            lambda: self._client.embed_query(text, task_type=QUERY_TASK, output_dimensionality=self.output_dimensionality)
        )
        return self._finish(vector)

    def _check_length(self, text: str) -> None:
        """Refuse over-long input instead of letting the service truncate it silently."""
        if not text.strip():
            raise EmbeddingError("Cannot embed empty text")
        if len(text) > self.max_input_chars:
            raise EmbeddingError(f"Text has {len(text)} characters, limit is {self.max_input_chars}")

    def _finish(self, vector: Sequence[float]) -> list[float]:
        if len(vector) != self.output_dimensionality:
            raise EmbeddingError(f"Vector has {len(vector)} dimensions, expected {self.output_dimensionality}")
        return l2_normalize(vector) if self.normalize else list(vector)

    def _call(self, request: Callable[[], object]):
        for attempt in range(self.max_retries + 1):
            try:
                return request()
            except Exception as exc:  # provider SDKs raise several error types
                retryable = any(marker in str(exc) for marker in RETRYABLE_MARKERS)
                if not retryable or attempt == self.max_retries:
                    raise EmbeddingError(f"Embedding request failed: {type(exc).__name__}") from exc
                wait = self.retry_wait_seconds * (attempt + 1)
                logger.warning("Embedding service busy or quota reached, retrying in %.0f s", wait)
                self._sleep(wait)
        raise AssertionError("unreachable")


def build_embeddings(config: AppConfig, **overrides) -> GeminiEmbeddings:
    return GeminiEmbeddings(
        model=config.gemini_embedding_model,
        api_key=config.gemini_api_key,
        output_dimensionality=config.embedding_output_dimension,
        **overrides,
    )
