"""Ground truth dataset of the evaluation (spec §10.2, D-57), written by scripts/build_ground_truth.py."""

import json
from dataclasses import dataclass, field
from pathlib import Path

# The 36 test questions of Sprint 4 (pertanyaan_uji.md): numbers 1-30 and E1-E6
SPRINT4_IDS = tuple([str(n) for n in range(1, 31)] + [f"E{n}" for n in range(1, 7)])


@dataclass(frozen=True)
class GroundTruthEntry:
    id: str
    category: str  # pkl (scored with Ragas), pkl_redirect or non_pkl (checked by status)
    user_input: str
    reference: str
    reference_contexts: tuple[str, ...] = ()
    reference_sources: tuple[dict, ...] = ()
    expected_status: str = "answered"
    topic: str = ""
    question_type: str = ""
    version: str = ""
    note: str | None = None
    extra: dict = field(default_factory=dict)


def load_dataset(path: str | Path) -> list[GroundTruthEntry]:
    entries = []
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        missing = [k for k in ("id", "category", "user_input", "reference") if not row.get(k)]
        if missing:
            raise ValueError(f"Line {number} of {path} lacks {missing}")
        known = {f for f in GroundTruthEntry.__dataclass_fields__ if f != "extra"}
        entries.append(GroundTruthEntry(
            **{k: tuple(v) if k in ("reference_contexts", "reference_sources") else v for k, v in row.items() if k in known},
            extra={k: v for k, v in row.items() if k not in known},
        ))
    ids = [e.id for e in entries]
    if len(ids) != len(set(ids)):
        raise ValueError(f"Duplicate ids in {path}")
    return entries


def select(entries: list[GroundTruthEntry], scope: str = "uji36", ids: list[str] | None = None) -> list[GroundTruthEntry]:
    """``uji36``: the 36 Sprint 4 test questions, ``pkl``: every entry scored with Ragas (38), ``all``: all 44."""
    if ids:
        wanted = set(ids)
        unknown = wanted - {e.id for e in entries}
        if unknown:
            raise ValueError(f"Unknown ids: {sorted(unknown)}")
        return [e for e in entries if e.id in wanted]
    if scope == "uji36":
        return [e for e in entries if e.id in SPRINT4_IDS]
    if scope == "pkl":
        return [e for e in entries if e.category == "pkl"]
    if scope == "all":
        return list(entries)
    raise ValueError(f"Unknown scope {scope!r}")
