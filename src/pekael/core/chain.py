"""Deterministic RAG workflow built from explicit steps (class diagram: Chain).

Steps run in the order they were added. This is a fixed workflow, not an agent:
no step chooses which step runs next, except that a step may finish the chain early
by setting ``ChainState.response``.
"""

import operator
from collections.abc import Callable
from functools import reduce

from langchain_core.runnables import Runnable, RunnableLambda

from pekael.core.schemas import ChainState

Step = Callable[[ChainState], ChainState]


def _skip_when_answered(step: Step) -> Step:
    def run(state: ChainState) -> ChainState:
        if state.response is not None:
            return state
        return step(state)

    return run


class Chain:
    def __init__(self) -> None:
        self._steps: list[tuple[str, Step]] = []
        self._runnable: Runnable | None = None

    @property
    def step_names(self) -> list[str]:
        return [name for name, _ in self._steps]

    def add(self, step: Step, name: str | None = None) -> "Chain":
        self._steps.append((name or step.__name__, step))
        self._runnable = None
        return self

    def clear(self) -> None:
        self._steps.clear()
        self._runnable = None

    def build(self) -> Runnable:
        """Compose the steps into a LangChain RunnableSequence."""
        if not self._steps:
            raise ValueError("Chain has no steps; add at least one before build()")
        runnables = [RunnableLambda(_skip_when_answered(step), name=name) for name, step in self._steps]
        self._runnable = reduce(operator.or_, runnables)
        return self._runnable

    def invoke(self, input_data: ChainState) -> ChainState:
        if self._runnable is None:
            self.build()
        return self._runnable.invoke(input_data)
