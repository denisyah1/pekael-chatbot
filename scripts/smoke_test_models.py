"""Manual live smoke test for the configured Gemini models (spec §9.1; OD-01, OD-02).

Makes exactly three small API calls (chat, document embedding, query embedding) with
no retries. Never run by pytest. Usage from the project root:

    .venv\\Scripts\\python.exe scripts\\smoke_test_models.py
"""

import math
import sys
import time
from collections.abc import Callable

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from pekael.config.app_configurator import AppConfigurator
from pekael.config.settings import AppConfig, ConfigError

CHAT_PROMPT = "Jawab dalam satu kalimat Bahasa Indonesia: apa kepanjangan dari PKL dalam konteks perkuliahan?"


def _chat(config: AppConfig, api_key: str) -> str:
    llm = ChatGoogleGenerativeAI(
        model=config.gemini_chat_model, google_api_key=api_key, temperature=0, max_retries=0, timeout=30
    )
    reply = llm.invoke(CHAT_PROMPT)
    text = reply.text if isinstance(reply.text, str) else str(reply.content)
    return f"jawaban: {text.strip()[:200]!r}"


def _embeddings(config: AppConfig, api_key: str) -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(model=config.gemini_embedding_model, google_api_key=api_key)


def _describe_vector(vector: list[float], expected_dim: int) -> str:
    if len(vector) != expected_dim:
        raise AssertionError(f"dimensi {len(vector)} != EMBEDDING_OUTPUT_DIMENSION {expected_dim}")
    norm = math.sqrt(sum(v * v for v in vector))
    return f"dimensi {len(vector)}, norma L2 {norm:.4f}"


def _embed_document(config: AppConfig, api_key: str) -> str:
    dim = config.embedding_output_dimension
    vectors = _embeddings(config, api_key).embed_documents(
        ["Mahasiswa wajib mengikuti pembekalan sebelum PKL."], output_dimensionality=dim
    )
    return "RETRIEVAL_DOCUMENT, " + _describe_vector(vectors[0], dim)


def _embed_query(config: AppConfig, api_key: str) -> str:
    dim = config.embedding_output_dimension
    vector = _embeddings(config, api_key).embed_query("Apa syarat mengikuti PKL?", output_dimensionality=dim)
    return "RETRIEVAL_QUERY, " + _describe_vector(vector, dim)


def _run(name: str, check: Callable[[], str], secrets: list[str]) -> bool:
    start = time.perf_counter()
    try:
        detail = check()
    except Exception as exc:  # report any provider error without crashing the remaining checks
        message = f"{type(exc).__name__}: {exc}"
        for secret in secrets:
            message = message.replace(secret, "***")
        print(f"[GAGAL] {name} ({time.perf_counter() - start:.2f} s) - {message[:500]}")
        return False
    print(f"[OK]    {name} ({time.perf_counter() - start:.2f} s) - {detail}")
    return True


def main() -> int:
    try:
        config = AppConfigurator.read_config()
    except ConfigError as exc:
        print(exc)
        return 2
    missing = config.missing_runtime_settings()
    if missing:
        print("Variabel berikut belum diisi di .env:", ", ".join(missing))
        return 2

    api_key = config.gemini_api_key.get_secret_value()
    secrets = config.secret_values()
    print(f"Chat model      : {config.gemini_chat_model}")
    print(f"Embedding model : {config.gemini_embedding_model} (dimensi {config.embedding_output_dimension})")
    print()

    results = [
        _run("chat", lambda: _chat(config, api_key), secrets),
        _run("embedding dokumen", lambda: _embed_document(config, api_key), secrets),
        _run("embedding query", lambda: _embed_query(config, api_key), secrets),
    ]
    print()
    print(f"Ringkasan: {sum(results)}/{len(results)} lulus")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
