import json

import faiss
import pytest
from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding

from pekael.core.schemas import RetrievedDocument
from pekael.vectorstores.base import IndexNotReadyError, VectorStoreError
from pekael.vectorstores.factory import VectorStoreFactory
from pekael.vectorstores.faiss_vector_store import FaissVectorStore

TEXTS = [
    "Waktu pelaksanaan PKL minimal 4 bulan.",
    "Mahasiswa dapat menjadi peserta PKL jika telah memenuhi minimal 100 SKS.",
    "Telah memperoleh nilai minimal B+ dari pembimbing lapangan dan dosen pembimbing.",
]


class FakeEmbeddings(DeterministicFakeEmbedding):
    model: str = "fake-embedding"


class BrokenEmbeddings(FakeEmbeddings):
    def embed_documents(self, texts):
        raise RuntimeError("quota exhausted")


def _chunks(texts=TEXTS, source_hash="565a9929ea00a999") -> list[Document]:
    return [
        Document(page_content=t, metadata={"source_file": "pedoman.pdf", "source_hash": source_hash, "page": i + 7, "chunk_id": f"c{i}"})
        for i, t in enumerate(texts)
    ]


def _store(tmp_path, embeddings=None, **kwargs) -> FaissVectorStore:
    return FaissVectorStore(tmp_path / "index", embeddings or FakeEmbeddings(size=16), **kwargs)


def test_ingest_writes_versioned_index_and_manifest(tmp_path):
    store = _store(tmp_path, build_info={"chunk_size": 1000, "chunk_overlap": 150})

    report = store.ingest_document(_chunks())

    folder = tmp_path / "index" / "versions" / report.build_id
    assert (tmp_path / "index" / "ACTIVE").read_text(encoding="utf-8").strip() == report.build_id
    assert {p.name for p in folder.iterdir()} == {"index.faiss", "index.pkl", "manifest.json"}
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["index_type"] == "IndexFlatL2"
    assert manifest["dimension"] == 16
    assert manifest["chunk_count"] == 3
    assert manifest["pages"] == [7, 8, 9]
    assert manifest["chunk_size"] == 1000
    assert manifest["sources"] == [{"source_file": "pedoman.pdf", "source_hash": "565a9929ea00a999"}]
    assert (report.chunk_count, report.dimension, report.embedding_model) == (3, 16, "fake-embedding")


def test_index_is_flat_l2(tmp_path):
    store = _store(tmp_path)
    store.ingest_document(_chunks())

    assert isinstance(store._store.index, faiss.IndexFlatL2)


def test_new_process_can_reload_and_search(tmp_path):
    _store(tmp_path).ingest_document(_chunks())
    fresh = _store(tmp_path)  # simulates an application restart

    results = fresh.get_relevant_document(TEXTS[1], k=2)

    assert fresh.is_ready
    assert all(isinstance(r, RetrievedDocument) for r in results)
    assert results[0].document.page_content == TEXTS[1]
    assert results[0].document.metadata["page"] == 8
    assert results[0].distance == pytest.approx(0.0, abs=1e-5)
    assert results[0].distance <= results[1].distance


def test_default_k_is_used(tmp_path):
    store = _store(tmp_path, default_k=2)
    store.ingest_document(_chunks())

    assert len(store.get_relevant_document("PKL")) == 2
    assert len(store.get_relevant_document("PKL", k=3)) == 3


def test_search_without_index_reports_not_ready(tmp_path):
    with pytest.raises(IndexNotReadyError, match="not been built"):
        _store(tmp_path).get_relevant_document("PKL")


def test_failed_build_keeps_previous_index_active(tmp_path):
    good = _store(tmp_path)
    first = good.ingest_document(_chunks())

    with pytest.raises(VectorStoreError, match="failed"):
        _store(tmp_path, embeddings=BrokenEmbeddings(size=16)).ingest_document(_chunks(["teks baru"]))

    assert good.active_build_id() == first.build_id
    versions = list((tmp_path / "index" / "versions").iterdir())
    assert [v.name for v in versions] == [first.build_id]  # no half-written temporary folder left behind
    assert _store(tmp_path).get_relevant_document(TEXTS[0], k=1)[0].document.page_content == TEXTS[0]


def test_rebuild_switches_version_and_keeps_only_recent_ones(tmp_path):
    store = _store(tmp_path, keep_versions=2)
    builds = [store.ingest_document(_chunks([f"versi {i}"])).build_id for i in range(3)]

    remaining = sorted(p.name for p in (tmp_path / "index" / "versions").iterdir())
    assert store.active_build_id() == builds[-1]
    assert remaining == builds[1:]
    assert store.get_relevant_document("versi 2", k=1)[0].document.page_content == "versi 2"


def test_empty_input_is_rejected(tmp_path):
    with pytest.raises(VectorStoreError, match="No chunks"):
        _store(tmp_path).ingest_document([])


def test_missing_active_version_reports_not_ready(tmp_path):
    (tmp_path / "index").mkdir()
    (tmp_path / "index" / "ACTIVE").write_text("20260101T000000-deadbeef\n", encoding="utf-8")

    with pytest.raises(IndexNotReadyError, match="missing"):
        _store(tmp_path).load()


def test_index_built_with_other_embedding_model_must_be_rebuilt(tmp_path):
    _store(tmp_path).ingest_document(_chunks())

    class OtherModel(FakeEmbeddings):
        model: str = "other-embedding"

    with pytest.raises(IndexNotReadyError, match="rebuild"):
        _store(tmp_path, embeddings=OtherModel(size=16)).load()


def test_factory_builds_faiss_store(tmp_path):
    store = VectorStoreFactory.get_vector_store("faiss", index_path=tmp_path, embeddings=FakeEmbeddings(size=8), default_k=3)

    assert isinstance(store, FaissVectorStore)
    assert store.default_k == 3


@pytest.mark.parametrize(("k", "keep"), [(0, 2), (4, 0)])
def test_invalid_parameters(tmp_path, k, keep):
    with pytest.raises(ValueError):
        _store(tmp_path, default_k=k, keep_versions=keep)
