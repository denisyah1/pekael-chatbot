import pytest
from langchain_core.documents import Document

from pekael.core import messages
from pekael.core.prompts import CONVERSATION_PROMPT, OFF_TOPIC_MESSAGES, REDIRECT_MESSAGES, SYSTEM_PROMPT
from pekael.core.rag_steps import RagSteps, source_reference
from pekael.core.schemas import ChainState, ResponseStatus, RetrievedDocument
from pekael.models.embeddings import EmbeddingError
from pekael.models.gemini_model import LLMError
from pekael.vectorstores.base import BaseVectorStore, IndexNotReadyError, VectorStoreError

TEXTS = [
    ("Mahasiswa dapat menjadi peserta PKL jika telah memenuhi minimal 100 SKS.", 10, "B. Persyaratan"),
    ("Waktu pelaksanaan PKL minimal 4 bulan.", 7, None),
    ("Telah memperoleh nilai minimal B+ dari pembimbing lapangan.", 11, "E. Kelulusan"),
]


def _retrieved(distances=(0.35, 0.42, 0.55)) -> list[RetrievedDocument]:
    return [
        RetrievedDocument(
            Document(
                page_content=text,
                metadata={"source_file": "pedoman.pdf", "page": page, "chunk_id": f"565a9929-p{page:03d}-c01", "section": section},
            ),
            distance,
        )
        for (text, page, section), distance in zip(TEXTS, distances)
    ]


class FakeStore(BaseVectorStore):
    def __init__(self, results=None, error: Exception | None = None) -> None:
        self.results = _retrieved() if results is None else results
        self.error = error
        self.queries: list[tuple[str, int | None]] = []

    def ingest_document(self, documents):
        raise NotImplementedError

    def get_relevant_document(self, query, k=None):
        self.queries.append((query, k))
        if self.error:
            raise self.error
        return self.results


class FakeLLM:
    def __init__(self, answer: str = "Minimal 100 SKS.\nSUMBER: 1", error: Exception | None = None) -> None:
        self.answer = answer
        self.error = error
        self.calls: list[tuple[str, str | None]] = []

    def generate_response(self, prompt, system_prompt=None):
        self.calls.append((prompt, system_prompt))
        if self.error:
            raise self.error
        return self.answer


def _ask(question="Berapa SKS minimal untuk PKL?", store=None, llm=None, **kwargs):
    store = store or FakeStore()
    llm = llm or FakeLLM()
    chain = RagSteps(store, llm, **kwargs).build_chain()
    return chain.invoke(ChainState(question=question)).response, store, llm


def test_steps_follow_spec_order():
    chain = RagSteps(FakeStore(), FakeLLM()).build_chain()

    assert chain.step_names == [
        "validate_input",
        "retrieve",
        "relevancy_gate",
        "build_prompt",
        "generate",
        "validate_citations",
    ]


def test_answer_cites_only_chunks_named_on_sources_line():
    response, store, llm = _ask(llm=FakeLLM("Minimal 100 SKS dan nilai B+.\nSUMBER: 1, 3"), retrieval_k=4)

    assert response.status is ResponseStatus.ANSWERED
    assert response.answer == "Minimal 100 SKS dan nilai B+."
    assert [(s.page, s.section) for s in response.sources] == [(10, "B. Persyaratan"), (11, "E. Kelulusan")]
    assert response.sources[0].chunk_id == "565a9929-p010-c01"
    assert response.sources[0].source_file == "pedoman.pdf"
    assert response.distances == (0.35, 0.42, 0.55)
    assert store.queries == [("Berapa SKS minimal untuk PKL?", 4)]


def test_prompt_holds_question_context_and_system_prompt():
    _, _, llm = _ask(question="  Berapa SKS minimal?  ")

    prompt, system_prompt = llm.calls[0]
    assert system_prompt.startswith(SYSTEM_PROMPT) and "Catatan untuk aturan no. 7" in system_prompt
    assert prompt.endswith("PERTANYAAN MAHASISWA:\nBerapa SKS minimal?")
    assert "GAYA BAHASA PERTANYAAN: netral" in prompt
    assert "[1] (pedoman, halaman PDF 10, B. Persyaratan)" in prompt
    assert "[3] (pedoman, halaman PDF 11, E. Kelulusan)" in prompt


def test_sources_number_outside_context_is_ignored():
    response, _, _ = _ask(llm=FakeLLM("Minimal 100 SKS.\nSUMBER: 2, 9"))

    assert [s.page for s in response.sources] == [7]


def test_missing_sources_line_cites_every_context_chunk():
    response, _, _ = _ask(llm=FakeLLM("Minimal 100 SKS."))

    assert response.status is ResponseStatus.ANSWERED
    assert [s.page for s in response.sources] == [10, 7, 11]


def test_not_found_without_redirection_uses_a_ready_made_one():
    response, _, _ = _ask(llm=FakeLLM("TIDAK_DITEMUKAN"))

    assert response.status is ResponseStatus.OUT_OF_SCOPE
    assert response.answer in REDIRECT_MESSAGES
    assert response.sources == ()


def test_model_redirection_is_kept_with_related_pages():
    redirect = "Jadwalnya ditetapkan tiap semester, tanyakan ke Admin Prodi PTIK. Syaratnya minimal 100 SKS."

    response, _, _ = _ask(llm=FakeLLM(f"TIDAK_DITEMUKAN\n{redirect}\nSUMBER: 1"))

    assert response.status is ResponseStatus.OUT_OF_SCOPE
    assert response.answer == redirect
    assert [s.page for s in response.sources] == [10]


def test_redirection_with_discouraged_wording_is_replaced():
    response, _, _ = _ask(llm=FakeLLM("TIDAK_DITEMUKAN\nMaaf, informasi ini tidak ditemukan di konteks.\nSUMBER: -"))

    assert response.answer in REDIRECT_MESSAGES


def test_snippet_is_short_and_from_chunk_text():
    long_text = "kata " * 100
    item = RetrievedDocument(Document(long_text, metadata={"source_file": "a.pdf", "page": 4, "chunk_id": "c"}), 0.1)

    snippet = source_reference(item).snippet

    assert len(snippet) <= 202
    assert snippet.endswith("…")
    assert source_reference(item).section is None


@pytest.mark.parametrize("question", ["", "   ", "\n"])
def test_empty_question_is_rejected_before_retrieval(question):
    response, store, llm = _ask(question=question)

    assert response.status is ResponseStatus.INVALID_INPUT
    assert response.answer == messages.EMPTY_QUESTION
    assert store.queries == [] and llm.calls == []


def test_too_long_question_is_rejected_before_retrieval():
    response, store, _ = _ask(question="a" * 21, question_max_chars=20)

    assert response.status is ResponseStatus.INVALID_INPUT
    assert "20 karakter" in response.answer
    assert store.queries == []


def test_question_at_length_limit_is_accepted():
    response, _, _ = _ask(question="a" * 20, question_max_chars=20)

    assert response.status is ResponseStatus.ANSWERED


def test_gate_rejection_gets_a_conversational_reply_without_handbook_context():
    reply = "Halo juga! Ada yang mau kamu tanyakan soal PKL?"

    response, _, llm = _ask(question="halo kak", llm=FakeLLM(reply), max_distance=0.30)

    assert response.status is ResponseStatus.OUT_OF_SCOPE
    assert response.answer == reply
    assert response.distances == (0.35, 0.42, 0.55)
    (prompt, system), = llm.calls
    assert system == CONVERSATION_PROMPT
    assert prompt.endswith("PESAN MAHASISWA:\nhalo kak") and "KONTEKS" not in prompt  # no handbook passages
    assert "GAYA BAHASA PERTANYAAN: santai" in prompt


@pytest.mark.parametrize(
    "reply",
    ["PKL minimal 100 SKS kok.", "Maaf, itu tidak dapat dijawab.", "TIDAK_DITEMUKAN", ""],
)
def test_conversational_reply_with_facts_or_discouraged_wording_is_replaced(reply):
    response, _, _ = _ask(question="apa itu machine learning", llm=FakeLLM(reply), max_distance=0.30)

    assert response.answer in OFF_TOPIC_MESSAGES


def test_conversational_reply_falls_back_when_gemini_fails():
    response, _, _ = _ask(llm=FakeLLM(error=LLMError("quota", "Gemini request failed")), max_distance=0.30)

    assert response.status is ResponseStatus.OUT_OF_SCOPE
    assert response.answer in OFF_TOPIC_MESSAGES


def test_question_passing_the_gate_keeps_all_chunks():
    """D-47: only the nearest chunk decides; farther chunks may hold a rule the answer needs."""
    _, _, llm = _ask(max_distance=0.42)

    prompt = llm.calls[0][0]
    assert "[2] (pedoman, halaman PDF 7)" in prompt
    assert "[3] (pedoman, halaman PDF 11, E. Kelulusan)" in prompt


def test_gate_disabled_when_threshold_not_set():
    response, _, llm = _ask(store=FakeStore(_retrieved((1.5, 1.7, 1.9))))

    assert response.status is ResponseStatus.ANSWERED
    assert len(llm.calls) == 1


def test_empty_retrieval_gets_a_conversational_reply():
    response, _, llm = _ask(store=FakeStore(results=[]), llm=FakeLLM("Siap, ada yang bisa dibantu soal PKL?"))

    assert response.status is ResponseStatus.OUT_OF_SCOPE
    assert [system for _, system in llm.calls] == [CONVERSATION_PROMPT]


def test_index_not_ready_returns_status_without_calling_llm():
    response, _, llm = _ask(store=FakeStore(error=IndexNotReadyError("Knowledge base has not been built yet")))

    assert response.status is ResponseStatus.UNAVAILABLE
    assert response.answer == messages.INDEX_NOT_READY
    assert llm.calls == []


def _embedding_error(provider_text: str) -> EmbeddingError:
    try:
        try:
            raise RuntimeError(provider_text)
        except RuntimeError as cause:
            raise EmbeddingError("Embedding request failed: RuntimeError") from cause
    except EmbeddingError as exc:
        return exc


@pytest.mark.parametrize(
    ("error", "status", "answer"),
    [
        (_embedding_error("429 RESOURCE_EXHAUSTED"), ResponseStatus.UNAVAILABLE, messages.QUOTA_EXHAUSTED),
        (_embedding_error("400 API key not valid"), ResponseStatus.UNAVAILABLE, messages.SERVICE_MISCONFIGURED),
        (_embedding_error("503 UNAVAILABLE"), ResponseStatus.UNAVAILABLE, messages.SERVICE_UNAVAILABLE),
        (VectorStoreError("corrupt"), ResponseStatus.ERROR, messages.RETRIEVAL_FAILED),
    ],
)
def test_retrieval_failures_become_safe_status(error, status, answer):
    response, _, llm = _ask(store=FakeStore(error=error))

    assert (response.status, response.answer) == (status, answer)
    assert llm.calls == []


@pytest.mark.parametrize(
    ("kind", "status", "answer"),
    [
        ("quota", ResponseStatus.UNAVAILABLE, messages.QUOTA_EXHAUSTED),
        ("auth", ResponseStatus.UNAVAILABLE, messages.SERVICE_MISCONFIGURED),
        ("unavailable", ResponseStatus.UNAVAILABLE, messages.SERVICE_UNAVAILABLE),
        ("empty", ResponseStatus.ERROR, messages.GENERATION_FAILED),
        ("other", ResponseStatus.ERROR, messages.GENERATION_FAILED),
    ],
)
def test_generation_failures_become_safe_status(kind, status, answer):
    response, _, _ = _ask(llm=FakeLLM(error=LLMError(kind, "Gemini request failed")))

    assert (response.status, response.answer) == (status, answer)
    assert response.sources == ()


def test_redirection_written_without_the_marker_is_treated_as_one():
    answer = "Kamu bisa tanyakan ke Admin Prodi PTIK ya, karena infonya belum ada di panduan kita.\nSUMBER: 1, 2"

    response, _, _ = _ask(llm=FakeLLM(answer))

    assert response.status is ResponseStatus.OUT_OF_SCOPE
    assert response.answer in REDIRECT_MESSAGES
    assert response.sources == ()


def test_real_answer_mentioning_a_contact_is_kept():
    answer = "Minimal 100 SKS. Untuk cek SKS-mu, tanyakan ke Admin Prodi PTIK.\nSUMBER: 1"

    response, _, _ = _ask(llm=FakeLLM(answer))

    assert response.status is ResponseStatus.ANSWERED

