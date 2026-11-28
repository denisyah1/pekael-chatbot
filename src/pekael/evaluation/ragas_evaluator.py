"""Ragas scoring of Pekael answers with the three research metrics (spec §10.1, FR-11, D-52).

Ragas, the OpenAI client (pointed at Groq) and google-genai are imported only when an evaluator
is built, so the chatbot never needs them. Every intermediate result of the metrics (statements,
verdicts, generated questions, similarities, attributions) is recorded next to the score, so each
score can be explained and checked by hand.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Any

import numpy as np

METRICS = ("faithfulness", "answer_relevancy", "context_recall")


@dataclass
class MetricOutcome:
    name: str
    score: float | None
    seconds: float
    details: dict = field(default_factory=dict)
    error: str | None = None


class _Recorder:
    """Records what the evaluator LLM and the embeddings return while one metric runs."""

    def __init__(self, llm: Any, embeddings: Any) -> None:
        self.llm_calls: list[dict] = []
        self.vectors: list[tuple[str, list[float]]] = []
        original_generate = llm.agenerate
        original_text = embeddings.aembed_text
        original_texts = embeddings.aembed_texts

        async def agenerate(prompt, response_model, *args, **kwargs):
            result = await original_generate(prompt, response_model, *args, **kwargs)
            self.llm_calls.append({"output_type": response_model.__name__, "output": result.model_dump()})
            return result

        async def aembed_text(text, *args, **kwargs):
            vector = await original_text(text, *args, **kwargs)
            self.vectors.append((text, list(vector)))
            return vector

        async def aembed_texts(texts, *args, **kwargs):
            vectors = await original_texts(texts, *args, **kwargs)
            self.vectors.extend((t, list(v)) for t, v in zip(texts, vectors))
            return vectors

        llm.agenerate = agenerate
        embeddings.aembed_text = aembed_text
        embeddings.aembed_texts = aembed_texts

    def take(self) -> tuple[list[dict], list[tuple[str, list[float]]]]:
        calls, vectors = self.llm_calls, self.vectors
        self.llm_calls, self.vectors = [], []
        return calls, vectors


def _cosine(a: list[float], b: list[float]) -> float:
    a_, b_ = np.asarray(a), np.asarray(b)
    return float(a_ @ b_ / (np.linalg.norm(a_) * np.linalg.norm(b_)))


def explain_faithfulness(calls: list[dict]) -> dict:
    statements = next((c["output"]["statements"] for c in calls if c["output_type"] == "StatementGeneratorOutput"), [])
    verdicts = next((c["output"]["statements"] for c in calls if c["output_type"] == "NLIStatementOutput"), [])
    supported = sum(1 for v in verdicts if v.get("verdict"))
    return {"statements": statements, "verdicts": verdicts, "supported": supported, "total": len(verdicts)}


def explain_answer_relevancy(user_input: str, calls: list[dict], vectors: list[tuple[str, list[float]]]) -> dict:
    generated = [c["output"] for c in calls if c["output_type"] == "AnswerRelevanceOutput"]
    lookup = dict(vectors)
    original = lookup.get(user_input)
    questions = []
    for item in generated:
        vector = lookup.get(item.get("question"))
        similarity = _cosine(vector, original) if vector is not None and original is not None else None
        questions.append({"question": item.get("question"), "noncommittal": item.get("noncommittal"), "cosine_similarity": similarity})
    all_noncommittal = bool(generated) and all(bool(g.get("noncommittal")) for g in generated)
    return {"generated_questions": questions, "all_noncommittal": all_noncommittal}


def explain_context_recall(calls: list[dict]) -> dict:
    classifications = next((c["output"]["classifications"] for c in calls if c["output_type"] == "ContextRecallOutput"), [])
    attributed = sum(1 for c in classifications if c.get("attributed"))
    return {"classifications": classifications, "attributed": attributed, "total": len(classifications)}


class RagasEvaluator:
    """Faithfulness, Answer Relevancy and Context Recall with a Groq evaluator LLM and Gemini embeddings."""

    def __init__(self, groq_api_key: str, groq_model: str, groq_base_url: str, gemini_api_key: str,
                 embedding_model: str, max_retries: int = 8, max_tokens: int = 4096) -> None:
        from google import genai
        from openai import AsyncOpenAI
        from ragas.embeddings import GoogleEmbeddings
        from ragas.llms import llm_factory
        from ragas.metrics.collections import AnswerRelevancy, ContextRecall, Faithfulness

        # The openai client waits for Groq's retry-after on 429 (8000 tokens per minute on the free tier).
        client = AsyncOpenAI(api_key=groq_api_key, base_url=groq_base_url, max_retries=max_retries)
        # gpt-oss is a reasoning model: Ragas' default of 1024 output tokens cut Faithfulness verdicts short (EXP-012 probe).
        self.llm = llm_factory(groq_model, provider="openai", client=client, max_tokens=max_tokens)
        self.embeddings = GoogleEmbeddings(client=genai.Client(api_key=gemini_api_key), model=embedding_model)
        self.recorder = _Recorder(self.llm, self.embeddings)
        self.faithfulness = Faithfulness(llm=self.llm)
        self.answer_relevancy = AnswerRelevancy(llm=self.llm, embeddings=self.embeddings)
        self.context_recall = ContextRecall(llm=self.llm)
        self.groq_model = groq_model
        self.embedding_model = embedding_model

    async def _run(self, name: str, coroutine, explain) -> MetricOutcome:
        started = time.perf_counter()
        self.recorder.take()
        try:
            result = await coroutine
        except Exception as exc:  # one failing metric must not stop the others
            calls, vectors = self.recorder.take()
            return MetricOutcome(name, None, round(time.perf_counter() - started, 2), {"llm_calls": calls},
                                 f"{type(exc).__name__}: {str(exc)[:300]}")
        calls, vectors = self.recorder.take()
        value = float(result.value)
        return MetricOutcome(name, None if math.isnan(value) else value, round(time.perf_counter() - started, 2), explain(calls, vectors))

    async def score(self, user_input: str, response: str, retrieved_contexts: list[str], reference: str) -> dict[str, MetricOutcome]:
        return {
            "faithfulness": await self._run(
                "faithfulness",
                self.faithfulness.ascore(user_input=user_input, response=response, retrieved_contexts=retrieved_contexts),
                lambda calls, _: explain_faithfulness(calls),
            ),
            "answer_relevancy": await self._run(
                "answer_relevancy",
                self.answer_relevancy.ascore(user_input=user_input, response=response),
                lambda calls, vectors: explain_answer_relevancy(user_input, calls, vectors),
            ),
            "context_recall": await self._run(
                "context_recall",
                self.context_recall.ascore(user_input=user_input, retrieved_contexts=retrieved_contexts, reference=reference),
                lambda calls, _: explain_context_recall(calls),
            ),
        }
