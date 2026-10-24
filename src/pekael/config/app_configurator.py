"""Reads configuration and assembles the chatbot (class diagram: AppConfigurator)."""

import os
from pathlib import Path

from dotenv import dotenv_values

from pekael.config.settings import AppConfig

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
    def create_manager_from_config(config: AppConfig):
        """Build a ChatbotManager wired with loader, splitter, vector store and LLM."""
        raise NotImplementedError("AppConfigurator.create_manager_from_config is implemented in Sprint 3")
