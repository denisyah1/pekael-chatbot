import pytest
from langchain_core.runnables import Runnable

from pekael.core.chain import Chain
from pekael.core.schemas import ChainState, ChatbotResponse, ResponseStatus


def _append(label: str):
    def step(state: ChainState) -> ChainState:
        state.context += label
        return state

    step.__name__ = f"append_{label}"
    return step


def test_steps_run_in_order():
    chain = Chain().add(_append("a")).add(_append("b")).add(_append("c"))

    result = chain.invoke(ChainState(question="q"))

    assert result.context == "abc"
    assert chain.step_names == ["append_a", "append_b", "append_c"]


def test_build_returns_langchain_runnable():
    chain = Chain().add(_append("a")).add(_append("b"))

    assert isinstance(chain.build(), Runnable)


def test_single_step_chain_works():
    assert Chain().add(_append("x")).invoke(ChainState(question="q")).context == "x"


def test_step_setting_response_skips_remaining_steps():
    fallback = ChatbotResponse(answer="fallback", status=ResponseStatus.OUT_OF_SCOPE)

    def gate(state: ChainState) -> ChainState:
        state.response = fallback
        return state

    chain = Chain().add(_append("a")).add(gate).add(_append("never"))

    result = chain.invoke(ChainState(question="q"))

    assert result.response is fallback
    assert result.context == "a"


def test_build_without_steps_fails():
    with pytest.raises(ValueError):
        Chain().build()


def test_clear_removes_steps():
    chain = Chain().add(_append("a"))
    chain.clear()

    assert chain.step_names == []
    with pytest.raises(ValueError):
        chain.invoke(ChainState(question="q"))


def test_adding_step_after_build_rebuilds():
    chain = Chain().add(_append("a"))
    chain.build()
    chain.add(_append("b"))

    assert chain.invoke(ChainState(question="q")).context == "ab"
