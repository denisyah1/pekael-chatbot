"""Wrapper around LangChain's RecursiveCharacterTextSplitter (class diagram: RecursiveCharacterSplitter)."""

import re

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pekael.splitters.base import BaseSplitter

# Prefer paragraph, line, then sentence boundaries before cutting inside a sentence.
SEPARATORS = ["\n\n", "\n", ". ", " ", ""]

# Headings in the handbook: chapters ("BAB III" followed by its title line) and
# sub-chapters ("G. Persyaratan Peserta PKL": capital letter, no closing period).
CHAPTER_HEADING = re.compile(r"^BAB [IVXL]+\n[A-Z][A-Z /&,()-]{3,80}$", re.MULTILINE)
SECTION_HEADING = re.compile(r"^[A-Z]\.\s+[A-Z][^.\n]{2,80}$", re.MULTILINE)
SECTION_SEPARATOR = " / "


def _headings(text: str) -> list[tuple[int, str]]:
    found = [(m.start(), " ".join(m.group(0).split())) for m in CHAPTER_HEADING.finditer(text)]
    found += [(m.start(), m.group(0).strip()) for m in SECTION_HEADING.finditer(text)]
    return sorted(found)


class RecursiveCharacterSplitter(BaseSplitter):
    def __init__(self, chunk_size: int, chunk_overlap: int) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be > 0")
        if not 0 <= chunk_overlap < chunk_size:
            raise ValueError("chunk_overlap must be >= 0 and smaller than chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=SEPARATORS,
            add_start_index=True,
        )

    def split(self, documents: list[Document]) -> list[Document]:
        """Split page documents into chunks, in page order.

        Every chunk keeps the page metadata and gains ``chunk_id`` (stable within one ingestion),
        ``chunk_index`` and ``section``: the heading in effect where the chunk starts plus every heading
        inside the chunk that has text after it, joined by " / ". Chunks never span two pages, so page
        citations stay exact.
        """
        chunks: list[Document] = []
        section = ""  # carried over when a page starts in the middle of a sub-chapter
        for document in documents:
            if not document.page_content.strip():
                continue
            headings = _headings(document.page_content)
            source_hash = document.metadata.get("source_hash", "")
            page = document.metadata.get("page", 0)
            for index, chunk in enumerate(self._splitter.split_documents([document]), start=1):
                start = chunk.metadata.pop("start_index")
                end = start + len(chunk.page_content)
                at_start = [title for pos, title in headings if pos <= start]
                # A heading that only closes the chunk (no text after it) belongs to the next chunk.
                inside = [title for pos, title in headings if start < pos and pos + len(title) < end]
                titles = [at_start[-1] if at_start else section, *inside]
                chunk.metadata.update(
                    chunk_id=f"{source_hash[:8]}-p{page:03d}-c{index:02d}",
                    chunk_index=index,
                    section=SECTION_SEPARATOR.join(dict.fromkeys(t for t in titles if t)),
                )
                chunks.append(chunk)
            if headings:
                section = headings[-1][1]
        return chunks
