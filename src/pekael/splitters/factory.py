from pekael.splitters.base import BaseSplitter
from pekael.splitters.recursive_character_splitter import RecursiveCharacterSplitter


class DocumentSplitterFactory:
    _splitters: dict[str, type[BaseSplitter]] = {"recursive_character": RecursiveCharacterSplitter}

    @classmethod
    def get_splitter(cls, splitter_type: str, **kwargs) -> BaseSplitter:
        key = splitter_type.lower()
        if key not in cls._splitters:
            supported = ", ".join(sorted(cls._splitters))
            raise ValueError(f"Unsupported splitter type {splitter_type!r}; supported: {supported}")
        return cls._splitters[key](**kwargs)
