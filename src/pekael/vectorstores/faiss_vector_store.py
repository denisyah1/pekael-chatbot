"""FAISS IndexFlatL2 vector store with versioned, persistent indexes (class diagram: FaissVectorStore, D-04).

Layout under ``index_path``::

    ACTIVE                        one line: the build_id in use
    versions/<build_id>/          index.faiss, index.pkl (LangChain docstore), manifest.json

A new build is written to a temporary folder, saved, reloaded and checked before ACTIVE is
switched to it, so a failed build never replaces a working index (FR-07). Distances are the
squared L2 values returned by IndexFlatL2: smaller means closer, they are not probabilities.
"""

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from pekael import __version__
from pekael.core.schemas import IndexingReport, RetrievedDocument
from pekael.vectorstores.base import BaseVectorStore, IndexNotReadyError, VectorStoreError

ACTIVE_FILE = "ACTIVE"
VERSIONS_DIR = "versions"
MANIFEST_FILE = "manifest.json"
TEMP_PREFIX = ".building-"


class FaissVectorStore(BaseVectorStore):
    def __init__(
        self,
        index_path: str | Path,
        embeddings: Embeddings,
        default_k: int = 4,
        keep_versions: int = 2,
        build_info: dict | None = None,
    ) -> None:
        if default_k <= 0:
            raise ValueError("default_k must be > 0")
        if keep_versions < 1:
            raise ValueError("keep_versions must be >= 1")
        self.index_path = Path(index_path)
        self.embeddings = embeddings
        self.default_k = default_k
        self.keep_versions = keep_versions
        self.build_info = build_info or {}  # e.g. chunk settings, recorded in the manifest
        self._store: FAISS | None = None
        self.manifest: dict | None = None

    # ---------- building ----------

    def ingest_document(self, documents: list[Document]) -> IndexingReport:
        """Build a new index version from chunks and activate it only after it reloads correctly."""
        if not documents:
            raise VectorStoreError("No chunks to index")
        build_id = self._new_build_id(documents)
        versions = self.index_path / VERSIONS_DIR
        temp = versions / f"{TEMP_PREFIX}{build_id}"
        final = versions / build_id
        try:
            store = FAISS.from_documents(documents, self.embeddings, distance_strategy=DistanceStrategy.EUCLIDEAN_DISTANCE)
            temp.mkdir(parents=True)
            store.save_local(str(temp))
            manifest = self._manifest(build_id, documents, store)
            (temp / MANIFEST_FILE).write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
            reloaded = self._load_folder(temp)
            if reloaded.index.ntotal != len(documents):
                raise VectorStoreError(f"Reloaded index has {reloaded.index.ntotal} vectors, expected {len(documents)}")
            os.replace(temp, final)
        except Exception as exc:
            shutil.rmtree(temp, ignore_errors=True)
            if isinstance(exc, VectorStoreError):
                raise
            raise VectorStoreError(f"Building the index failed: {type(exc).__name__}") from exc

        self._activate(build_id)
        self._store, self.manifest = self._load_folder(final), manifest
        self._prune()
        return IndexingReport(
            build_id=build_id,
            chunk_count=len(documents),
            embedding_model=manifest["embedding_model"],
            dimension=manifest["dimension"],
            index_path=str(final),
        )

    def _new_build_id(self, documents: list[Document]) -> str:
        source_hash = str(documents[0].metadata.get("source_hash", "nohash"))[:8]
        return f"{datetime.now(timezone.utc):%Y%m%dT%H%M%S%f}-{source_hash}"

    def _manifest(self, build_id: str, documents: list[Document], store: FAISS) -> dict:
        sources = sorted({(d.metadata.get("source_file"), d.metadata.get("source_hash")) for d in documents}, key=str)
        pages = sorted({d.metadata["page"] for d in documents if "page" in d.metadata})
        return {
            "build_id": build_id,
            "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "pekael_version": __version__,
            "index_type": type(store.index).__name__,
            "distance": "squared_l2",
            "embedding_model": getattr(self.embeddings, "model", type(self.embeddings).__name__),
            "dimension": store.index.d,
            "normalized": getattr(self.embeddings, "normalize", None),
            "chunk_count": len(documents),
            "pages": pages,
            "sources": [{"source_file": f, "source_hash": h} for f, h in sources],
            **self.build_info,
        }

    def _activate(self, build_id: str) -> None:
        """Point ACTIVE at a build atomically (write a temporary file, then replace)."""
        pointer = self.index_path / ACTIVE_FILE
        temp = pointer.with_name(ACTIVE_FILE + ".tmp")
        temp.write_text(build_id + "\n", encoding="utf-8")
        os.replace(temp, pointer)

    def _prune(self) -> None:
        versions = self.index_path / VERSIONS_DIR
        active = self.active_build_id()
        builds = sorted((p for p in versions.iterdir() if p.is_dir() and not p.name.startswith(TEMP_PREFIX)), key=lambda p: p.name)
        for old in builds[: -self.keep_versions]:
            if old.name != active:
                shutil.rmtree(old, ignore_errors=True)

    # ---------- loading ----------

    def active_build_id(self) -> str | None:
        pointer = self.index_path / ACTIVE_FILE
        if not pointer.is_file():
            return None
        return pointer.read_text(encoding="utf-8").strip() or None

    @property
    def is_ready(self) -> bool:
        return self._store is not None

    def load(self) -> None:
        """Load the active index. Raises IndexNotReadyError if it is missing or incompatible."""
        build_id = self.active_build_id()
        if build_id is None:
            raise IndexNotReadyError("Knowledge base has not been built yet")
        folder = self.index_path / VERSIONS_DIR / build_id
        manifest_file = folder / MANIFEST_FILE
        if not manifest_file.is_file():
            raise IndexNotReadyError(f"Active index {build_id} is missing or incomplete")
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        expected_model = getattr(self.embeddings, "model", None)
        if expected_model and manifest.get("embedding_model") != expected_model:
            raise IndexNotReadyError(
                f"Index was built with {manifest.get('embedding_model')}, configured model is {expected_model}: rebuild it"
            )
        try:
            self._store = self._load_folder(folder)
        except Exception as exc:
            raise IndexNotReadyError(f"Active index {build_id} could not be loaded") from exc
        self.manifest = manifest

    def _load_folder(self, folder: Path) -> FAISS:
        # The docstore is a pickle written by this application only, never an uploaded file.
        return FAISS.load_local(str(folder), self.embeddings, allow_dangerous_deserialization=True)

    # ---------- searching ----------

    def get_relevant_document(self, query: str, k: int | None = None) -> list[RetrievedDocument]:
        if self._store is None:
            self.load()
        results = self._store.similarity_search_with_score(query, k=k or self.default_k)
        return [RetrievedDocument(document=doc, distance=float(distance)) for doc, distance in results]
