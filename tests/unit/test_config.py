from pathlib import Path

import pytest

from pekael.config.app_configurator import AppConfigurator
from pekael.config.settings import AppConfig, ConfigError

ENV_KEYS = ["GEMINI_API_KEY", "CHUNK_SIZE", "ADMIN_USERNAME", "ADMIN_PASSWORD"]


def test_defaults_match_spec_starting_values():
    config = AppConfig.from_env({})

    assert config.gemini_embedding_model == "gemini-embedding-001"
    assert config.embedding_output_dimension == 768
    assert (config.chunk_size, config.chunk_overlap, config.retrieval_k) == (1000, 150, 4)
    assert config.retrieval_max_l2_distance is None
    assert config.faiss_index_path == Path("data/index")
    assert config.tesseract_lang == "ind+eng"


def test_values_are_parsed_from_strings():
    config = AppConfig.from_env({"CHUNK_SIZE": "800", "RETRIEVAL_MAX_L2_DISTANCE": "0.85", "LOG_LEVEL": "debug"})

    assert config.chunk_size == 800
    assert config.retrieval_max_l2_distance == pytest.approx(0.85)
    assert config.log_level == "DEBUG"


@pytest.mark.parametrize("value", ["", "   ", "replace_with_your_new_gemini_key"])
def test_empty_and_placeholder_values_count_as_unset(value):
    config = AppConfig.from_env({"GEMINI_API_KEY": value})

    assert config.gemini_api_key is None
    assert config.missing_runtime_settings() == ["GEMINI_API_KEY"]


def test_invalid_number_names_the_variable():
    with pytest.raises(ConfigError, match="CHUNK_SIZE"):
        AppConfig.from_env({"CHUNK_SIZE": "abc"})


def test_overlap_must_be_smaller_than_chunk_size():
    with pytest.raises(ConfigError, match="CHUNK_OVERLAP"):
        AppConfig.from_env({"CHUNK_SIZE": "100", "CHUNK_OVERLAP": "100"})


def test_secrets_are_not_shown_in_repr():
    config = AppConfig.from_env({"GEMINI_API_KEY": "real-key-123", "ADMIN_PASSWORD": "pw-456"})

    assert "real-key-123" not in repr(config)
    assert "pw-456" not in repr(config)
    assert set(config.secret_values()) == {"real-key-123", "pw-456"}


def test_admin_disabled_without_credentials():
    assert not AppConfig.from_env({"ADMIN_USERNAME": "admin"}).admin_enabled
    assert AppConfig.from_env({"ADMIN_USERNAME": "admin", "ADMIN_PASSWORD": "s3cret"}).admin_enabled


def test_read_config_uses_env_file_and_environment_wins(tmp_path, monkeypatch):
    for key in ENV_KEYS:
        monkeypatch.delenv(key, raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text("CHUNK_SIZE=700\nGEMINI_API_KEY=from-file\n", encoding="utf-8")
    monkeypatch.setenv("CHUNK_SIZE", "900")

    config = AppConfigurator.read_config(env_file)

    assert config.chunk_size == 900
    assert config.gemini_api_key.get_secret_value() == "from-file"


def test_read_config_without_env_file(tmp_path, monkeypatch):
    for key in ENV_KEYS:
        monkeypatch.delenv(key, raising=False)

    config = AppConfigurator.read_config(tmp_path / "missing.env")

    assert config.missing_runtime_settings() == ["GEMINI_API_KEY"]
