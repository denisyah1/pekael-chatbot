from pekael.vectorstores.base import BaseVectorStore
from pekael.vectorstores.faiss_vector_store import FaissVectorStore


class VectorStoreFactory:
    _stores: dict[str, type[BaseVectorStore]] = {"faiss": FaissVectorStore}

    @classmethod
    def get_vector_store(cls, store_type: str, **kwargs) -> BaseVectorStore:
        key = store_type.lower()
        if key not in cls._stores:
            supported = ", ".join(sorted(cls._stores))
            raise ValueError(f"Unsupported vector store type {store_type!r}; supported: {supported}")
        return cls._stores[key](**kwargs)
