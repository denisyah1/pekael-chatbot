"""Typed application configuration read from environment variables."""

import logging
from collections.abc import Mapping
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, SecretStr, ValidationError, field_validator, model_validator

# Values copied unchanged from .env.example are treated as "not set".
PLACEHOLDER_PREFIX = "replace_with_"


class ConfigError(ValueError):
    """Raised when configuration values are present but invalid."""


class AppConfig(BaseModel):
    """All runtime, ingestion, admin, and evaluation settings.

    Each field maps to an environment variable with the same name in upper case
    (e.g. ``chunk_size`` -> ``CHUNK_SIZE``).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    # Gemini runtime
    gemini_api_key: SecretStr | None = None
    gemini_chat_model: str = "gemini-3.5-flash-lite"
    gemini_embedding_model: str = "gemini-embedding-001"
    embedding_output_dimension: int = Field(default=768, gt=0)

    # RAG / FAISS
    chunk_size: int = Field(default=1000, gt=0)
    chunk_overlap: int = Field(default=150, ge=0)
    retrieval_k: int = Field(default=4, gt=0)
    retrieval_max_l2_distance: float | None = Field(default=None, ge=0)
    faiss_index_path: Path = Path("data/index")
    knowledge_base_path: Path = Path("data/source/handbook.pdf")
    pdf_max_upload_mb: int = Field(default=30, gt=0)
    question_max_chars: int = Field(default=500, gt=0)
    ocr_min_text_chars_per_page: int = Field(default=40, ge=0)
    # 200 dpi matches the handbook scan resolution (EXP-001)
    ocr_render_dpi: int = Field(default=200, ge=72, le=600)
    ocr_corrections_path: Path = Path("data/corrections")
    tesseract_cmd: str | None = None
    tesseract_lang: str = "ind+eng"

    # Admin (single account)
    admin_username: str | None = None
    admin_password: SecretStr | None = None

    # Ragas evaluator (evaluation scripts only)
    openai_api_key: SecretStr | None = None
    openai_eval_model: str = "gpt-4o-mini"
    openai_eval_embedding_model: str = "text-embedding-3-small"
    ragas_dataset_path: Path = Path("data/evaluation/ground_truth.jsonl")

    # Operational
    app_env: str = "development"
    log_level: str = "INFO"

    @field_validator("log_level")
    @classmethod
    def _valid_log_level(cls, value: str) -> str:
        level = value.upper()
        if level not in logging.getLevelNamesMapping():
            raise ValueError(f"unknown log level {value!r}")
        return level

    @model_validator(mode="after")
    def _overlap_smaller_than_chunk(self) -> "AppConfig":
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE")
        return self

    @classmethod
    def from_env(cls, environ: Mapping[str, str]) -> "AppConfig":
        """Build a config from an environment mapping; empty and placeholder values count as unset."""
        values = {}
        for name in cls.model_fields:
            raw = environ.get(name.upper())
            if raw is None:
                continue
            raw = raw.strip()
            if raw and not raw.startswith(PLACEHOLDER_PREFIX):
                values[name] = raw
        try:
            return cls.model_validate(values)
        except ValidationError as exc:
            problems = []
            for error in exc.errors():
                field = ".".join(str(part) for part in error["loc"]).upper() or "CONFIG"
                problems.append(f"{field}: {error['msg']}")
            raise ConfigError("Invalid configuration — " + "; ".join(problems)) from None

    def missing_runtime_settings(self) -> list[str]:
        """Environment variables required to answer student questions that are not set."""
        return [] if self.gemini_api_key else ["GEMINI_API_KEY"]

    @property
    def admin_enabled(self) -> bool:
        return bool(self.admin_username and self.admin_password and self.admin_password.get_secret_value())

    def secret_values(self) -> list[str]:
        """Plain secret values, used only to redact them from logs."""
        secrets = (self.gemini_api_key, self.admin_password, self.openai_api_key)
        return [s.get_secret_value() for s in secrets if s and s.get_secret_value()]
