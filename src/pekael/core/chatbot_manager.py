"""Orchestrator of ingestion and question answering (class diagram: ChatbotManager).

There is deliberately no conversation memory: every question is answered independently.
"""

from pathlib import Path

from pekael.core.chain import Chain
from pekael.core.schemas import ChatbotResponse, IngestionReport
from pekael.loaders.base import BaseLoader
from pekael.models.gemini_model import GeminiModel
from pekael.splitters.base import BaseSplitter
from pekael.vectorstores.base import BaseVectorStore


class ChatbotManager:
    def __init__(
        self,
        system_prompt: str,
        loader: BaseLoader,
        splitter: BaseSplitter,
        vector_store: BaseVectorStore,
        llm: GeminiModel,
        chain: Chain | None = None,
    ) -> None:
        self.system_prompt = system_prompt
        self.loader = loader
        self.splitter = splitter
        self.vector_store = vector_store
        self.llm = llm
        self.chain = chain or Chain()

    def initialize_knowledge_base(self, source_path: str | Path) -> IngestionReport:
        raise NotImplementedError("ChatbotManager.initialize_knowledge_base is implemented in Sprint 3")

    def generate_response(self, message: str) -> ChatbotResponse:
        raise NotImplementedError("ChatbotManager.generate_response is implemented in Sprint 3")
