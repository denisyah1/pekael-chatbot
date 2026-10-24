"""Manual live smoke test for the three Ragas research metrics (spec §10.4; OD-05, OD-06).

Scores ONE fictional sample with Faithfulness, Answer Relevancy and Context Recall using
the OpenAI evaluator LLM and Gemini embeddings. The sample is not research data.
Costs a few small gpt-4o-mini calls. Usage from the project root:

    .venv\\Scripts\\python.exe scripts\\smoke_test_ragas.py
"""

import asyncio
import sys
import time
from importlib.metadata import version

from google import genai
from openai import AsyncOpenAI
from ragas.embeddings import GoogleEmbeddings
from ragas.llms import llm_factory
from ragas.metrics.collections import AnswerRelevancy, ContextRecall, Faithfulness

from pekael.config.app_configurator import AppConfigurator
from pekael.config.settings import ConfigError

# Fictional sample used only to check that the metric APIs work end to end.
SAMPLE = {
    "user_input": "Berapa lama durasi pelaksanaan PKL?",
    "retrieved_contexts": ["[Contoh fiktif] PKL dilaksanakan selama dua bulan di instansi mitra."],
    "response": "PKL dilaksanakan selama dua bulan di instansi mitra.",
    "reference": "Durasi PKL adalah dua bulan.",
}


async def _score(name: str, coroutine, secrets: list[str]) -> bool:
    start = time.perf_counter()
    try:
        result = await coroutine
    except Exception as exc:  # report provider/API errors and continue with the other metrics
        message = f"{type(exc).__name__}: {exc}"
        for secret in secrets:
            message = message.replace(secret, "***")
        print(f"[GAGAL] {name} ({time.perf_counter() - start:.2f} s) - {message[:500]}")
        return False
    print(f"[OK]    {name} ({time.perf_counter() - start:.2f} s) - skor {result.value:.3f}")
    return True


async def run() -> int:
    try:
        config = AppConfigurator.read_config()
    except ConfigError as exc:
        print(exc)
        return 2
    missing = [name for name, value in (("OPENAI_API_KEY", config.openai_api_key), ("GEMINI_API_KEY", config.gemini_api_key)) if not value]
    if missing:
        print("Variabel berikut belum diisi di .env:", ", ".join(missing))
        return 2

    secrets = config.secret_values()
    llm = llm_factory(
        config.openai_eval_model, client=AsyncOpenAI(api_key=config.openai_api_key.get_secret_value(), max_retries=0)
    )
    embeddings = GoogleEmbeddings(
        client=genai.Client(api_key=config.gemini_api_key.get_secret_value()), model=config.gemini_embedding_model
    )

    print(f"ragas {version('ragas')} | evaluator LLM: {config.openai_eval_model} | embeddings: {config.gemini_embedding_model} (Gemini)")
    print("Sampel: 1 contoh fiktif (bukan data penelitian)")
    print()

    s = SAMPLE
    results = [
        await _score(
            "Faithfulness",
            Faithfulness(llm=llm).ascore(
                user_input=s["user_input"], response=s["response"], retrieved_contexts=s["retrieved_contexts"]
            ),
            secrets,
        ),
        await _score(
            "Answer Relevancy",
            AnswerRelevancy(llm=llm, embeddings=embeddings).ascore(user_input=s["user_input"], response=s["response"]),
            secrets,
        ),
        await _score(
            "Context Recall",
            ContextRecall(llm=llm).ascore(
                user_input=s["user_input"], retrieved_contexts=s["retrieved_contexts"], reference=s["reference"]
            ),
            secrets,
        ),
    ]
    print()
    print(f"Ringkasan: {sum(results)}/{len(results)} metrik berjalan")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(run()))
