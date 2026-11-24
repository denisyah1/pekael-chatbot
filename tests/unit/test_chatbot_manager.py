import pytest
from langchain_core.documents import Document
from pydantic import SecretStr

from pekael.config.app_configurator import AppConfigurator
from pekael.config.settings import AppConfig, ConfigError
from pekael.core import messages
from pekael.core.chain import Chain
from pekael.core.chatbot_manager import ChatbotManager
from pekael.core.prompts import SYSTEM_PROMPT
from pekael.core.schemas import ChainState, IndexingReport, ResponseStatus
from pekael.loaders.base import BaseLoader
from pekael.loaders.pdf_loader import PDFLoader
from pekael.splitters.base import BaseSplitter
from pekael.splitters.recursive_character_splitter import RecursiveCharacterSplitter
from pekael.vectorstores.base import BaseVectorStore, VectorStoreError
from pekael.vectorstores.faiss_vector_store import FaissVectorStore


class FakeLoader(BaseLoader):
    def load(self, source_path, *, pages=None, on_page=None):
        return [
            Document("Halaman empat.", metadata={"source_file": "pedoman.pdf", "source_hash": "abc", "page": 4,
                                                 "extraction_method": "tesseract_ocr", "manually_corrected": True}),
            Document("Halaman lima.", metadata={"source_file": "pedoman.pdf", "source_hash": "abc", "page": 5,
                                                "extraction_method": "tesseract_ocr", "manually_corrected": False}),
            Document("Halaman enam.", metadata={"source_file": "pedoman.pdf", "source_hash": "abc", "page": 6,
                                                "extraction_method": "native_text", "manually_corrected": False}),
        ]


class FakeSplitter(BaseSplitter):
    def split(self, documents):
        return [Document(d.page_content, metadata={**d.metadata, "chunk_id": f"c{i}"}) for i, d in enumerate(documents)]


class FakeStore(BaseVectorStore):
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error
        self.ingested = None

    def ingest_document(self, documents):
        if self.error:
            raise self.error
        self.ingested = documents
        return IndexingReport("build-1", len(documents), "fake", 16, "data/index/versions/build-1")

    def get_relevant_document(self, query, k=None):
        return []


def _manager(store=None, chain=None) -> ChatbotManager:
    return ChatbotManager(SYSTEM_PROMPT, FakeLoader(), FakeSplitter(), store or FakeStore(), llm=object(), chain=chain)


def test_initialize_knowledge_base_reports_pages_chunks_and_unchecked_ocr():
    store = FakeStore()

    report = _manager(store).initialize_knowledge_base("pedoman.pdf")

    assert (report.source_file, report.source_hash) == ("pedoman.pdf", "abc")
    assert (report.page_count, report.native_pages, report.ocr_pages, report.chunk_count) == (3, 1, 2, 3)
    assert report.indexing.build_id == "build-1"
    assert report.warnings == ("OCR pages without a correction file, confirm they were checked: [5]",)
    assert len(store.ingested) == 3


def test_failed_build_raises_and_is_not_reported_as_success():
    with pytest.raises(VectorStoreError):
        _manager(FakeStore(error=VectorStoreError("Building the index failed"))).initialize_knowledge_base("x.pdf")


def test_manager_builds_rag_chain_by_default():
    assert _manager().chain.step_names[0] == "validate_input"
    assert len(_manager().chain.step_names) == 6


def test_custom_chain_with_steps_is_kept():
    def answer(state: ChainState) -> ChainState:
        return state

    chain = Chain().add(answer)

    assert _manager(chain=chain).chain.step_names == ["answer"]


def test_unexpected_step_error_becomes_safe_error_response():
    def broken(state: ChainState) -> ChainState:
        raise KeyError("secret-looking detail")

    response = _manager(chain=Chain().add(broken)).generate_response("Apa itu PKL?")

    assert response.status is ResponseStatus.ERROR
    assert response.answer == messages.UNEXPECTED_ERROR
    assert "secret" not in response.answer


def test_chain_without_response_becomes_error():
    response = _manager(chain=Chain().add(lambda state: state, name="noop")).generate_response("Apa itu PKL?")

    assert response.status is ResponseStatus.ERROR


def test_questions_are_independent():
    """No conversation memory: each question starts from a fresh state (FR-10)."""
    seen = []

    def record(state: ChainState) -> ChainState:
        seen.append((state.question, state.retrieved, state.answer))
        state.answer = "x"
        return state

    manager = _manager(chain=Chain().add(record))
    manager.generate_response("satu")
    manager.generate_response("dua")

    assert seen == [("satu", [], ""), ("dua", [], "")]


def test_progress_reports_only_steps_that_run():
    """Empty retrieval ends the chain early, so later steps are not reported to the UI."""
    reported = []

    response = _manager().generate_response("Berapa SKS minimal?", on_step=reported.append)

    assert response.status is ResponseStatus.OUT_OF_SCOPE
    assert reported == ["validate_input", "retrieve"]


def test_create_manager_requires_gemini_key():
    with pytest.raises(ConfigError, match="GEMINI_API_KEY"):
        AppConfigurator.create_manager_from_config(AppConfig.from_env({}))


def test_create_manager_wires_components_from_config(tmp_path):
    config = AppConfig(
        gemini_api_key=SecretStr("test-key-not-real"),
        chunk_size=800,
        chunk_overlap=100,
        retrieval_k=3,
        retrieval_max_l2_distance=0.6,
        faiss_index_path=tmp_path / "index",
        knowledge_base_pages="4-6,9",
        question_max_chars=300,
    )

    manager = AppConfigurator.create_manager_from_config(config)

    assert isinstance(manager.loader, PDFLoader)
    assert manager.loader.pages == [4, 5, 6, 9]
    assert isinstance(manager.splitter, RecursiveCharacterSplitter)
    assert isinstance(manager.vector_store, FaissVectorStore)
    assert manager.vector_store.default_k == 3
    assert manager.vector_store.build_info["chunk_size"] == 800
    assert manager.llm.model_name == config.gemini_chat_model
    assert manager.system_prompt == SYSTEM_PROMPT
    assert len(manager.chain.step_names) == 6


class TwoDocumentLoader(BaseLoader):
    """Handbook pages honour the selection, the additional document is loaded in full (D-53)."""

    def __init__(self) -> None:
        self.calls = []

    def load(self, source_path, *, pages=None, on_page=None, all_pages=False):
        self.calls.append((str(source_path), pages, all_pages))
        name = str(source_path)
        count = 2 if name == "pedoman.pdf" else 3
        hash_ = "abc" if name == "pedoman.pdf" else "def"
        docs = [Document(f"{name} {n}", metadata={"source_file": name, "source_hash": hash_, "page": n,
                                                  "extraction_method": "native_text", "manually_corrected": False})
                for n in range(1, count + 1)]
        for done in range(1, count + 1):
            if on_page:
                on_page(done, count)
        return docs


class CountingSplitter(FakeSplitter):
    def __init__(self) -> None:
        self.calls = 0

    def split(self, documents):
        self.calls += 1
        assert len({d.metadata["source_file"] for d in documents}) == 1  # never mixes documents
        return super().split(documents)


def test_extra_documents_are_loaded_in_full_split_separately_and_recorded():
    loader, splitter, store = TwoDocumentLoader(), CountingSplitter(), FakeStore()
    store.build_info = {}
    manager = ChatbotManager(SYSTEM_PROMPT, loader, splitter, store, llm=object(), chain=Chain())

    report = manager.initialize_knowledge_base("pedoman.pdf", pages=[1, 2], extra_paths=["kb.pdf"])

    assert loader.calls == [("pedoman.pdf", [1, 2], False), ("kb.pdf", None, True)]
    assert splitter.calls == 2
    assert [d.metadata["source_file"] for d in store.ingested] == ["pedoman.pdf"] * 2 + ["kb.pdf"] * 3
    assert (report.source_file, report.page_count, report.extra_sources) == ("pedoman.pdf", 5, ("kb.pdf",))
    assert store.build_info["extra_paths"] == ["kb.pdf"]


def test_build_without_extra_documents_records_an_empty_list():
    store = FakeStore()
    store.build_info = {}

    report = _manager(store).initialize_knowledge_base("pedoman.pdf")

    assert report.extra_sources == ()
    assert store.build_info["extra_paths"] == []


def test_extra_knowledge_paths_are_read_from_a_comma_separated_setting():
    config = AppConfig.from_env({"KNOWLEDGE_BASE_EXTRA_PATHS": " data/source/kb.pdf , data/source/faq.pdf ,"})

    assert [p.as_posix() for p in config.extra_knowledge_paths] == ["data/source/kb.pdf", "data/source/faq.pdf"]
    assert AppConfig.from_env({}).extra_knowledge_paths == []


def test_groq_evaluator_key_is_optional_and_redacted():
    config = AppConfig.from_env({"GROQ_API_KEY": "gsk_" + "x" * 30})

    assert config.groq_eval_model == "openai/gpt-oss-120b"
    assert config.groq_base_url.startswith("https://api.groq.com/")
    assert "gsk_" + "x" * 30 in config.secret_values()
    assert AppConfig.from_env({"GROQ_API_KEY": "replace_with_your_groq_key"}).groq_api_key is None
