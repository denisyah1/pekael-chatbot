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
    def load(self, source_path):
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
