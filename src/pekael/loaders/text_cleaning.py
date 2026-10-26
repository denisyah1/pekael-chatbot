"""Conservative clean-up of extracted page text (spec §4.1 step 5).

Only layout noise is removed: whitespace, wrapped lines, and typographic ligatures.
Words, numbers, punctuation and list markers are never changed, and hyphens are
kept as-is because Indonesian uses them meaningfully (e.g. "seluas-luasnya").
"""

import re
import unicodedata

LIGATURES = {"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl"}
INVISIBLE = {"­": "", "​": "", "﻿": "", " ": " ", "\t": " "}

# A line that starts a new item and must not be merged into the previous line:
# "1.", "1)", "a.", "b)", "A.", "IV.", "-", "•"
LIST_ITEM = re.compile(r"^(\d{1,3}[.)]|[a-zA-Z][.)]|[IVXLC]{1,6}\.|[-•▪●])\s")
HEADING_MAX_CHARS = 60


def clean_page_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    for source, target in {**LIGATURES, **INVISIBLE}.items():
        text = text.replace(source, target)
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\f", "\n")

    paragraphs: list[str] = []
    for block in re.split(r"\n\s*\n", text):
        lines = [re.sub(r" {2,}", " ", line).strip() for line in block.split("\n")]
        lines = [line for line in lines if line]
        if not lines:
            continue
        paragraph = _unwrap(lines)
        if paragraphs and _continues_sentence(paragraphs[-1], paragraph):
            paragraphs[-1] = f"{paragraphs[-1]} {paragraph}"
        else:
            paragraphs.append(paragraph)
    return "\n\n".join(paragraphs)


def _continues_sentence(previous: str, current: str) -> bool:
    """OCR sometimes inserts a blank line mid-sentence: rejoin when the sentence clearly runs on."""
    return not re.search(r"[.:;?!)]$", previous) and current[0].islower() and not LIST_ITEM.match(current)


def _unwrap(lines: list[str]) -> str:
    """Join wrapped lines of one paragraph, keeping list items, headings and table rows on their own lines."""
    merged = [lines[0]]
    for line in lines[1:]:
        is_table_row = "|" in line or "|" in merged[-1]
        if is_table_row or LIST_ITEM.match(line) or (_is_heading(merged[-1]) and line[0].isupper()):
            merged.append(line)
        else:
            merged[-1] = f"{merged[-1]} {line}"
    return "\n".join(merged)


def _is_heading(line: str) -> bool:
    """A short line without closing punctuation, e.g. "8. Penggunaan Angka Desimal".

    Wrapped body text fills the full page width, so it is much longer than this.
    """
    return len(line) <= HEADING_MAX_CHARS and not re.search(r"[.,;:]$", line)
