import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_secrets.py"
spec = importlib.util.spec_from_file_location("check_secrets", SCRIPT)
check_secrets = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_secrets)

# Fake keys are assembled at runtime so this file itself never matches the patterns.
FAKE_OPENAI = "sk-" + "proj-" + "x" * 40
FAKE_GOOGLE_TOKEN = "AQ." + "A" * 40
FAKE_GOOGLE_KEY = "AIza" + "B" * 35


@pytest.mark.parametrize(
    "line",
    [
        f"OPENAI_API_KEY={FAKE_OPENAI}",
        f"GEMINI_API_KEY={FAKE_GOOGLE_TOKEN}",
        f'key = "{FAKE_GOOGLE_KEY}"',
        "ADMIN_PASSWORD=pkl" + "12345",
    ],
)
def test_detects_secrets(line):
    assert check_secrets.find_secrets(line)


@pytest.mark.parametrize(
    "line",
    [
        "GEMINI_API_KEY=replace_with_your_new_gemini_key",
        "ADMIN_PASSWORD=replace_with_a_strong_secret",
        "GEMINI_API_KEY=",
        "RETRIEVAL_K=4",
        "Use sk-learn style naming",
    ],
)
def test_ignores_placeholders_and_normal_text(line):
    assert check_secrets.find_secrets(line) == []


@pytest.mark.parametrize(("path", "forbidden"), [(".env", True), ("config/.env.local", True), (".env.example", False), ("src/env.py", False)])
def test_env_files_are_forbidden(path, forbidden):
    assert check_secrets.is_forbidden_file(path) is forbidden


def test_env_example_in_repo_is_clean():
    example = SCRIPT.parents[1] / ".env.example"

    for line in example.read_text(encoding="utf-8").splitlines():
        assert check_secrets.find_secrets(line) == [], line
