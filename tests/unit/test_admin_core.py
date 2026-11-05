"""Answer cache, build progress, page override, and stored versions (Sprint 4 admin support)."""

import pytest
from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding

from pekael.core.chain import Chain
from pekael.core.chatbot_manager import ChatbotManager, normalise_question
from pekael.core.prompts import SYSTEM_PROMPT
from pekael.core.schemas import ChainState, ChatbotResponse, ResponseStatus
from pekael.loaders.base import BaseLoader
from pekael.loaders.pdf_loader import PDFLoader
from pekael.splitters.recursive_character_splitter import RecursiveCharacterSplitter
from pekael.vectorstores.base import IndexNotReadyError
from pekael.vectorstores.faiss_vector_store import FaissVectorStore
from tests.unit.test_pdf_loader import NATIVE_PAGE, _make_pdf


class FakeEmbeddings(DeterministicFakeEmbedding):
    model: str = "fake-embedding"


class CountingChain(Chain):
    """A one-step chain that answers with a fixed status and counts how often it runs."""

    def __init__(self, status=ResponseStatus.ANSWERED) -> None:
        super().__init__()
        self.runs = 0

        def answer(state: ChainState) -> ChainState:
            self.runs += 1
            state.response = ChatbotResponse(f"jawaban {self.runs}", status)
            return state

        self.add(answer)


class PageLoader(BaseLoader):
    def __init__(self) -> None:
        self.calls = []

    def load(self, source_path, *, pages=None, on_page=None):
        self.calls.append(pages)
        numbers = pages or [4, 5]
        documents = []
        for done, page in enumerate(numbers, start=1):
            documents.append(Document(f"Isi halaman {page} tentang PKL.", metadata={
                "source_file": "pedoman.pdf", "source_hash": "565a9929ea00", "page": page, "total_pages": 29,
                "extraction_method": "native_text", "manually_corrected": False}))
            if on_page:
                on_page(done, len(numbers))
        return documents


class Store:
    manifest = {"build_id": "build-1"}


def _manager(chain=None, store=None, **kwargs) -> ChatbotManager:
    return ChatbotManager(SYSTEM_PROMPT, PageLoader(), RecursiveCharacterSplitter(1000, 150), store or Store(), object(),
                          chain=chain or CountingChain(), **kwargs)


# ---------- answer cache ----------

def test_same_question_is_answered_once():
    chain = CountingChain()
    manager = _manager(chain)

    first = manager.generate_response("Berapa SKS minimal?")
    second = manager.generate_response("  berapa sks   MINIMAL ")

    assert chain.runs == 1
    assert second is first
    assert manager.cached_answers() == 1


@pytest.mark.parametrize("status", [ResponseStatus.UNAVAILABLE, ResponseStatus.ERROR, ResponseStatus.INVALID_INPUT])
def test_failures_are_not_cached(status):
    chain = CountingChain(status)
    manager = _manager(chain)

    manager.generate_response("Berapa SKS minimal?")
    manager.generate_response("Berapa SKS minimal?")

    assert chain.runs == 2
    assert manager.cached_answers() == 0


def test_out_of_scope_answers_are_cached():
    chain = CountingChain(ResponseStatus.OUT_OF_SCOPE)
    manager = _manager(chain)

    manager.generate_response("Apa itu machine learning?")
    manager.generate_response("Apa itu machine learning?")

    assert chain.runs == 1


def test_new_build_does_not_reuse_old_answers():
    chain, store = CountingChain(), Store()
    store.manifest = {"build_id": "build-1"}
    manager = _manager(chain, store)

    manager.generate_response("Berapa SKS minimal?")
    store.manifest = {"build_id": "build-2"}
    manager.generate_response("Berapa SKS minimal?")

    assert chain.runs == 2


def test_oldest_answers_are_dropped_beyond_cache_size():
    chain = CountingChain()
    manager = _manager(chain, cache_size=2)

    for question in ("satu", "dua", "tiga", "satu"):
        manager.generate_response(question)

    assert chain.runs == 4
    assert manager.cached_answers() == 2


def test_cache_can_be_disabled_and_cleared():
    chain = CountingChain()
    manager = _manager(chain, cache_size=0)
    manager.generate_response("satu")
    manager.generate_response("satu")
    assert chain.runs == 2

    manager = _manager(CountingChain())
    manager.generate_response("satu")
    manager.clear_cache()
    assert manager.cached_answers() == 0


def test_question_normalisation():
    assert normalise_question("  Berapa  SKS\nminimal?? ") == "berapa sks minimal"
    assert normalise_question("   ") == ""


# ---------- building with progress and page override ----------

def test_build_reports_stages_and_pages_and_clears_cache(tmp_path):
    store = FaissVectorStore(tmp_path / "index", FakeEmbeddings(size=8), build_info={"knowledge_base_pages": "4-5"})
    manager = ChatbotManager(SYSTEM_PROMPT, PageLoader(), RecursiveCharacterSplitter(1000, 150), store, object(),
                             chain=CountingChain())
    manager.generate_response("satu")
    events = []

    report = manager.initialize_knowledge_base("pedoman.pdf", pages=[4, 6, 7], on_progress=lambda *e: events.append(e))

    assert manager.loader.calls == [[4, 6, 7]]
    assert events[0] == ("load", 0, 0)
    assert ("load", 3, 3) in events
    assert [e[0] for e in events][-2:] == ["split", "index"]
    assert report.page_count == 3
    assert store.manifest["knowledge_base_pages"] == "4,6,7"
    assert store.manifest["chunks_per_page"] == {"4": 1, "6": 1, "7": 1}
    assert store.manifest["total_pages"] == 29
    assert manager.cached_answers() == 0


def test_pdf_loader_page_override_and_progress(tmp_path):
    path = _make_pdf(tmp_path / "pedoman.pdf", [NATIVE_PAGE, NATIVE_PAGE, NATIVE_PAGE])
    progress = []

    documents = PDFLoader(pages=[1]).load(path, pages=[2, 3], on_page=lambda done, total: progress.append((done, total)))

    assert [d.metadata["page"] for d in documents] == [2, 3]
    assert progress == [(1, 2), (2, 2)]


# ---------- stored versions ----------

def _build(store: FaissVectorStore, text: str):
    return store.ingest_document([Document(text, metadata={"source_file": "p.pdf", "source_hash": "abc", "page": 4, "chunk_id": "c", "total_pages": 9})])


def test_versions_listed_newest_first_and_rollback(tmp_path):
    store = FaissVectorStore(tmp_path / "index", FakeEmbeddings(size=8))
    old = _build(store, "versi lama")
    new = _build(store, "versi baru")

    versions = store.versions()
    assert [v["build_id"] for v in versions] == [new.build_id, old.build_id]
    assert [v["active"] for v in versions] == [True, False]

    store.activate_version(old.build_id)

    assert store.active_build_id() == old.build_id
    assert store.manifest["build_id"] == old.build_id
    assert store.get_relevant_document("versi lama", k=1)[0].document.page_content == "versi lama"
    reloaded = FaissVectorStore(tmp_path / "index", FakeEmbeddings(size=8))
    assert reloaded.active_build_id() == old.build_id


def test_activating_unknown_or_incompatible_version_fails(tmp_path):
    store = FaissVectorStore(tmp_path / "index", FakeEmbeddings(size=8))
    built = _build(store, "teks")

    with pytest.raises(IndexNotReadyError):
        store.activate_version("tidak-ada")

    class OtherModel(DeterministicFakeEmbedding):
        model: str = "other-model"

    with pytest.raises(IndexNotReadyError):
        FaissVectorStore(tmp_path / "index", OtherModel(size=8)).activate_version(built.build_id)
    assert store.active_build_id() == built.build_id


def test_page_statistics_fall_back_to_docstore_for_older_builds(tmp_path):
    store = FaissVectorStore(tmp_path / "index", FakeEmbeddings(size=8))
    _build(store, "teks")
    store.manifest = {key: value for key, value in store.manifest.items() if key not in ("chunks_per_page", "total_pages")}

    assert store.chunks_per_page() == {4: 1}
    assert store.total_pages() == 9
