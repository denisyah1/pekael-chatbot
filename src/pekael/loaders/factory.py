from pekael.loaders.base import BaseLoader
from pekael.loaders.pdf_loader import PDFLoader


class DocumentLoaderFactory:
    _loaders: dict[str, type[BaseLoader]] = {"pdf": PDFLoader}

    @classmethod
    def get_loader(cls, source_type: str, **kwargs) -> BaseLoader:
        key = source_type.lower().lstrip(".")
        if key not in cls._loaders:
            supported = ", ".join(sorted(cls._loaders))
            raise ValueError(f"Unsupported source type {source_type!r}; supported: {supported}")
        return cls._loaders[key](**kwargs)
