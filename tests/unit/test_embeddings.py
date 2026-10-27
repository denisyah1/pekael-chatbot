import math

import pytest
from pydantic import SecretStr

from pekael.config.settings import AppConfig
from pekael.models.embeddings import (
    DOCUMENT_TASK,
    QUERY_TASK,
    EmbeddingError,
    GeminiEmbeddings,
    build_embeddings,
    l2_normalize,
)


class FakeClient:
    """Records calls like GoogleGenerativeAIEmbeddings and returns unnormalised vectors."""

    def __init__(self, dim: int = 4, failures: list[Exception] | None = None, wrong_dim: bool = False):
        self.dim = dim
        self.failures = list(failures or [])
        self.wrong_dim = wrong_dim
        self.calls: list[tuple[str, int, str, int]] = []

    def _vector(self, text: str) -> list[float]:
        size = self.dim + 1 if self.wrong_dim else self.dim
        return [float(len(text) + i) for i in range(size)]

    def embed_documents(self, texts, *, task_type=None, output_dimensionality=None):
        self._maybe_fail()
        self.calls.append(("documents", len(texts), task_type, output_dimensionality))
        return [self._vector(t) for t in texts]

    def embed_query(self, text, *, task_type=None, output_dimensionality=None):
        self._maybe_fail()
        self.calls.append(("query", 1, task_type, output_dimensionality))
        return self._vector(text)

    def _maybe_fail(self):
        if self.failures:
            raise self.failures.pop(0)


def _embeddings(client, **kwargs) -> GeminiEmbeddings:
    waits: list[float] = []
    embeddings = GeminiEmbeddings("gemini-embedding-001", None, 4, client=client, sleep=waits.append, **kwargs)
    embeddings.waits = waits
    return embeddings


def test_documents_and_queries_use_retrieval_task_types_and_dimension():
    client = FakeClient()
    embeddings = _embeddings(client)

    embeddings.embed_documents(["a", "bb"])
    embeddings.embed_query("apa itu PKL?")

    assert client.calls == [("documents", 2, DOCUMENT_TASK, 4), ("query", 1, QUERY_TASK, 4)]


def test_vectors_are_normalised_by_default():
    vectors = _embeddings(FakeClient()).embed_documents(["satu", "dua"]) + [_embeddings(FakeClient()).embed_query("tiga")]

    assert all(math.isclose(math.sqrt(sum(v * v for v in vector)), 1.0) for vector in vectors)


def test_normalisation_can_be_disabled_for_experiments():
    vector = _embeddings(FakeClient(), normalize=False).embed_query("abc")

    assert vector == [3.0, 4.0, 5.0, 6.0]


def test_documents_are_sent_in_batches_in_order():
    client = FakeClient()
    texts = [f"teks {'x' * i}" for i in range(7)]

    vectors = _embeddings(client, batch_size=3, normalize=False).embed_documents(texts)

    assert [c[1] for c in client.calls] == [3, 3, 1]
    assert [v[0] for v in vectors] == [float(len(t)) for t in texts]


def test_quota_errors_are_retried_with_growing_wait():
    client = FakeClient(failures=[RuntimeError("429 RESOURCE_EXHAUSTED"), RuntimeError("503 UNAVAILABLE")])
    embeddings = _embeddings(client, retry_wait_seconds=10)

    embeddings.embed_query("pertanyaan")

    assert embeddings.waits == [10, 20]
    assert len(client.calls) == 1


def test_quota_error_after_last_retry_raises_embedding_error():
    client = FakeClient(failures=[RuntimeError("429 RESOURCE_EXHAUSTED")] * 3)
    embeddings = _embeddings(client, max_retries=2)

    with pytest.raises(EmbeddingError, match="failed"):
        embeddings.embed_query("pertanyaan")
    assert len(embeddings.waits) == 2


def test_other_errors_are_not_retried():
    client = FakeClient(failures=[RuntimeError("400 INVALID_ARGUMENT")])
    embeddings = _embeddings(client)

    with pytest.raises(EmbeddingError):
        embeddings.embed_query("pertanyaan")
    assert embeddings.waits == []


def test_wrong_dimension_is_rejected():
    with pytest.raises(EmbeddingError, match="dimensions"):
        _embeddings(FakeClient(wrong_dim=True)).embed_query("x")


def test_missing_api_key_is_reported():
    with pytest.raises(EmbeddingError, match="GEMINI_API_KEY"):
        GeminiEmbeddings("gemini-embedding-001", None, 768)


def test_error_message_does_not_leak_provider_details():
    client = FakeClient(failures=[RuntimeError("400 bad request key=AIzaSECRET")])

    with pytest.raises(EmbeddingError) as info:
        _embeddings(client).embed_query("x")
    assert "AIzaSECRET" not in str(info.value)


def test_over_long_or_empty_text_is_rejected_before_calling_the_service():
    client = FakeClient()
    embeddings = _embeddings(client, max_input_chars=10)

    with pytest.raises(EmbeddingError, match="limit"):
        embeddings.embed_documents(["pendek", "x" * 11])
    with pytest.raises(EmbeddingError, match="empty"):
        embeddings.embed_query("   ")
    assert client.calls == []


def test_zero_vector_is_rejected():
    with pytest.raises(EmbeddingError):
        l2_normalize([0.0, 0.0])


def test_build_embeddings_uses_config():
    config = AppConfig.from_env({"GEMINI_API_KEY": "test-key", "EMBEDDING_OUTPUT_DIMENSION": "768"})

    embeddings = build_embeddings(config, client=FakeClient(dim=768))

    assert embeddings.model == "gemini-embedding-001"
    assert embeddings.output_dimensionality == 768
