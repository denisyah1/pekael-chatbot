import pytest
from langchain_core.embeddings import DeterministicFakeEmbedding

from pekael.loaders.base import BaseLoader
from pekael.loaders.factory import DocumentLoaderFactory
from pekael.loaders.pdf_loader import PDFLoader
from pekael.splitters.base import BaseSplitter
from pekael.splitters.factory import DocumentSplitterFactory
from pekael.splitters.recursive_character_splitter import RecursiveCharacterSplitter
from pekael.vectorstores.base import BaseVectorStore
from pekael.vectorstores.factory import VectorStoreFactory
from pekael.vectorstores.faiss_vector_store import FaissVectorStore


@pytest.mark.parametrize("source_type", ["pdf", "PDF", ".pdf"])
def test_loader_factory_returns_pdf_loader(source_type):
    loader = DocumentLoaderFactory.get_loader(source_type, min_text_chars=40)

    assert isinstance(loader, PDFLoader)
    assert isinstance(loader, BaseLoader)
    assert loader.min_text_chars == 40


def test_splitter_factory_returns_recursive_splitter():
    splitter = DocumentSplitterFactory.get_splitter("recursive_character", chunk_size=1000, chunk_overlap=150)

    assert isinstance(splitter, RecursiveCharacterSplitter)
    assert isinstance(splitter, BaseSplitter)
    assert (splitter.chunk_size, splitter.chunk_overlap) == (1000, 150)


def test_vector_store_factory_returns_faiss_store(tmp_path):
    store = VectorStoreFactory.get_vector_store(
        "faiss", index_path=tmp_path, embeddings=DeterministicFakeEmbedding(size=8), default_k=4
    )

    assert isinstance(store, FaissVectorStore)
    assert isinstance(store, BaseVectorStore)


@pytest.mark.parametrize(
    ("create", "kind"),
    [
        (lambda: DocumentLoaderFactory.get_loader("docx"), "source type"),
        (lambda: DocumentSplitterFactory.get_splitter("semantic"), "splitter type"),
        (lambda: VectorStoreFactory.get_vector_store("chroma"), "vector store type"),
    ],
)
def test_factories_reject_unsupported_types(create, kind):
    with pytest.raises(ValueError, match=f"Unsupported {kind}"):
        create()


@pytest.mark.parametrize(("size", "overlap"), [(0, 0), (100, 100), (100, -1)])
def test_splitter_rejects_invalid_parameters(size, overlap):
    with pytest.raises(ValueError):
        RecursiveCharacterSplitter(chunk_size=size, chunk_overlap=overlap)


@pytest.mark.parametrize("base", [BaseLoader, BaseSplitter, BaseVectorStore])
def test_base_contracts_are_abstract(base):
    with pytest.raises(TypeError):
        base()
