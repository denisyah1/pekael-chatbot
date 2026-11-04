"""Reads configuration and assembles the chatbot (class diagram: AppConfigurator)."""

import os
from pathlib import Path

from dotenv import dotenv_values

from pekael.config.settings import AppConfig, ConfigError
from pekael.core.chatbot_manager import ChatbotManager
from pekael.core.prompts import SYSTEM_PROMPT
from pekael.loaders.factory import DocumentLoaderFactory
from pekael.loaders.pdf_loader import parse_page_ranges
from pekael.models.embeddings import build_embeddings
from pekael.models.gemini_model import GeminiModel
from pekael.services.ocr_service import OcrService
from pekael.splitters.factory import DocumentSplitterFactory
from pekael.vectorstores.factory import VectorStoreFactory

DEFAULT_ENV_FILE = Path(".env")


class AppConfigurator:
    @staticmethod
    def read_config(config_path: str | Path | None = None) -> AppConfig:
        """Read settings from an optional .env file; real environment variables take precedence.

        Hosting secrets managers expose secrets as environment variables, so the same
        code path works locally and in deployment.
        """
        env_file = Path(config_path) if config_path else DEFAULT_ENV_FILE
        file_values = dotenv_values(env_file) if env_file.is_file() else {}
        merged = {key: value for key, value in file_values.items() if value is not None}
        merged.update(os.environ)
        return AppConfig.from_env(merged)

    @staticmethod
    def create_manager_from_config(config: AppConfig) -> ChatbotManager:
        """Build a ChatbotManager wired with loader, splitter, vector store and LLM via the factories."""
        missing = config.missing_runtime_settings()
        if missing:
            raise ConfigError("Missing required settings: " + ", ".join(missing))
        loader = DocumentLoaderFactory.get_loader(
            "pdf",
            ocr_service=OcrService(config.tesseract_cmd, config.tesseract_lang),
            min_text_chars=config.ocr_min_text_chars_per_page,
            ocr_dpi=config.ocr_render_dpi,
            corrections_dir=config.ocr_corrections_path,
            pages=parse_page_ranges(config.knowledge_base_pages),
        )
        splitter = DocumentSplitterFactory.get_splitter(
            "recursive_character", chunk_size=config.chunk_size, chunk_overlap=config.chunk_overlap
        )
        vector_store = VectorStoreFactory.get_vector_store(
            "faiss",
            index_path=config.faiss_index_path,
            embeddings=build_embeddings(config),
            default_k=config.retrieval_k,
            build_info={
                "chunk_size": config.chunk_size,
                "chunk_overlap": config.chunk_overlap,
                "knowledge_base_pages": config.knowledge_base_pages,
                "ocr_render_dpi": config.ocr_render_dpi,
            },
        )
        llm = GeminiModel(
            config.gemini_chat_model,
            config.gemini_api_key,
            timeout=config.gemini_timeout_seconds,
            reasoning_effort=config.gemini_reasoning_effort,
        )
        return ChatbotManager(
            SYSTEM_PROMPT,
            loader,
            splitter,
            vector_store,
            llm,
            retrieval_k=config.retrieval_k,
            max_distance=config.retrieval_max_l2_distance,
            question_max_chars=config.question_max_chars,
        )
