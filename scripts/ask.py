"""Ask Pekael questions from the terminal, without the web interface (Sprint 3 smoke test).

Each question is answered on its own (no conversation memory) and costs one embedding call
plus, if the relevancy gate passes, one Gemini call.

Usage from the project root:
    .venv\\Scripts\\python.exe scripts\\ask.py "Berapa SKS minimal untuk PKL?" ["pertanyaan lain" ...]
    .venv\\Scripts\\python.exe scripts\\ask.py            (interactive, empty line to stop)
"""

import argparse
import sys
import time

from pekael.config.app_configurator import AppConfigurator
from pekael.config.logging_config import configure_logging
from pekael.config.settings import ConfigError
from pekael.core.chatbot_manager import ChatbotManager
from pekael.models.embeddings import EmbeddingError
from pekael.models.gemini_model import LLMError


def show(manager: ChatbotManager, question: str) -> None:
    started = time.perf_counter()
    response = manager.generate_response(question)
    elapsed = time.perf_counter() - started
    print(f"\nT: {question}")
    print(f"J: {response.answer}")
    for source in response.sources:
        section = f", {source.section}" if source.section else ""
        print(f"   - {source.source_file}, halaman PDF {source.page}{section}")
    distances = ", ".join(f"{d:.3f}" for d in response.distances) or "-"
    print(f"   [status {response.status.value}, jarak {distances}, {elapsed:.2f} s]")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("questions", nargs="*", help="questions; none = interactive mode")
    args = parser.parse_args()

    try:
        config = AppConfigurator.read_config()
        configure_logging("WARNING", config.secret_values())
        manager = AppConfigurator.create_manager_from_config(config)
    except (ConfigError, EmbeddingError, LLMError) as exc:
        print(exc)
        return 2
    gate = config.retrieval_max_l2_distance
    print(f"Model {config.gemini_chat_model}, k = {config.retrieval_k}, batas jarak {gate if gate is not None else 'belum diatur'}")

    if args.questions:
        for question in args.questions:
            show(manager, question)
        return 0
    while True:
        question = input("\nPertanyaan (kosong untuk keluar): ").strip()
        if not question:
            return 0
        show(manager, question)


if __name__ == "__main__":
    sys.exit(main())
