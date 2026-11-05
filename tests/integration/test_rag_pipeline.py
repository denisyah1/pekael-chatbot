"""Chunks -> FAISS -> reload in a new process-like instance -> answer, with fake embeddings and LLM (no API calls)."""

from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding

from pekael.core.chatbot_manager import ChatbotManager
from pekael.core.prompts import SYSTEM_PROMPT
from pekael.core.schemas import ResponseStatus
from pekael.loaders.base import BaseLoader
from pekael.splitters.recursive_character_splitter import RecursiveCharacterSplitter
from pekael.vectorstores.faiss_vector_store import FaissVectorStore

PAGES = {
    7: "A. Waktu Pelaksanaan\nWaktu pelaksanaan PKL minimal 4 bulan.",
    10: "B. Persyaratan\nMahasiswa dapat menjadi peserta PKL jika telah memenuhi minimal 100 SKS.",
}


class FakeEmbeddings(DeterministicFakeEmbedding):
    model: str = "fake-embedding"


class PageLoader(BaseLoader):
    def load(self, source_path, *, pages=None, on_page=None):
        return [
            Document(text, metadata={"source_file": "pedoman.pdf", "source_hash": "565a9929ea00", "page": page,
                                     "extraction_method": "tesseract_ocr", "manually_corrected": True})
            for page, text in PAGES.items()
        ]


class QuotingLLM:
    """Answers with the first context block, like a grounded model would."""

    def generate_response(self, prompt, system_prompt=None):
        return "Sesuai buku panduan.\nSUMBER: 1"


def _manager(index_path) -> ChatbotManager:
    store = FaissVectorStore(index_path, FakeEmbeddings(size=16), default_k=2)
    return ChatbotManager(SYSTEM_PROMPT, PageLoader(), RecursiveCharacterSplitter(1000, 150), store, QuotingLLM(), retrieval_k=2)


def test_build_then_answer_after_restart(tmp_path):
    report = _manager(tmp_path / "index").initialize_knowledge_base("pedoman.pdf")

    restarted = _manager(tmp_path / "index")  # new instance, index loaded from disk
    response = restarted.generate_response(PAGES[10])

    assert report.chunk_count == 2
    assert restarted.vector_store.active_build_id() == report.indexing.build_id
    assert response.status is ResponseStatus.ANSWERED
    assert response.sources[0].page == 10  # identical text embeds to the same vector
    assert response.sources[0].chunk_id.endswith("-p010-c01")
    assert response.sources[0].section == "B. Persyaratan"
    assert response.distances[0] < 1e-6


def test_question_before_build_reports_missing_knowledge_base(tmp_path):
    response = _manager(tmp_path / "index").generate_response("Berapa SKS minimal?")

    assert response.status is ResponseStatus.UNAVAILABLE
