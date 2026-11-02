import pytest
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from pekael.models.gemini_model import AUTH, EMPTY, OTHER, QUOTA, UNAVAILABLE, GeminiModel, LLMError, classify_error


class FakeChat:
    """Stands in for ChatGoogleGenerativeAI: records messages, fails as instructed, then answers."""

    def __init__(self, answer: str = "Waktu pelaksanaan PKL minimal 4 bulan.\nSUMBER: 1", failures=None):
        self.answer = answer
        self.failures = list(failures or [])
        self.calls: list[list] = []

    def invoke(self, messages):
        self.calls.append(messages)
        if self.failures:
            raise self.failures.pop(0)
        return AIMessage(content=self.answer)


def _model(client, **kwargs) -> GeminiModel:
    waits: list[float] = []
    model = GeminiModel("gemini-3.5-flash-lite", None, client=client, sleep=waits.append, **kwargs)
    model.waits = waits
    return model


def test_system_and_user_messages_are_sent():
    client = FakeChat()

    answer = _model(client).generate_response("pertanyaan", system_prompt="aturan")

    assert answer.startswith("Waktu pelaksanaan PKL")
    (messages,) = client.calls
    assert isinstance(messages[0], SystemMessage) and messages[0].content == "aturan"
    assert isinstance(messages[1], HumanMessage) and messages[1].content == "pertanyaan"


def test_without_system_prompt_only_user_message_is_sent():
    client = FakeChat()
    _model(client).generate_response("pertanyaan")

    assert len(client.calls[0]) == 1


def test_temporary_unavailability_is_retried_once():
    client = FakeChat(failures=[RuntimeError("503 UNAVAILABLE")])
    model = _model(client, retry_wait_seconds=2)

    assert model.generate_response("x")
    assert model.waits == [2]
    assert len(client.calls) == 2


@pytest.mark.parametrize(
    ("error", "kind"),
    [
        (RuntimeError("429 RESOURCE_EXHAUSTED quota exceeded"), QUOTA),
        (RuntimeError("400 API key not valid. API_KEY_INVALID"), AUTH),
        (RuntimeError("503 UNAVAILABLE"), UNAVAILABLE),
        (TimeoutError("Request timed out"), UNAVAILABLE),
        (ValueError("something else"), OTHER),
    ],
)
def test_errors_are_classified(error, kind):
    assert classify_error(error) == kind


def test_quota_error_is_not_retried():
    client = FakeChat(failures=[RuntimeError("429 RESOURCE_EXHAUSTED")])
    model = _model(client)

    with pytest.raises(LLMError) as info:
        model.generate_response("x")
    assert info.value.kind == QUOTA
    assert model.waits == []


def test_unavailable_after_retries_raises_llm_error():
    client = FakeChat(failures=[RuntimeError("503 UNAVAILABLE")] * 2)

    with pytest.raises(LLMError) as info:
        _model(client, max_retries=1).generate_response("x")
    assert info.value.kind == UNAVAILABLE


def test_empty_answer_is_an_error():
    with pytest.raises(LLMError) as info:
        _model(FakeChat(answer="   ")).generate_response("x")
    assert info.value.kind == EMPTY


def test_error_message_does_not_contain_provider_details():
    client = FakeChat(failures=[RuntimeError("401 key=AIzaSECRETVALUE")])

    with pytest.raises(LLMError) as info:
        _model(client).generate_response("x")
    assert "AIzaSECRETVALUE" not in str(info.value)


def test_missing_api_key_without_client_is_reported():
    with pytest.raises(LLMError) as info:
        GeminiModel("gemini-3.5-flash-lite", None)
    assert info.value.kind == AUTH


def test_model_name_is_required():
    with pytest.raises(ValueError):
        GeminiModel("", None, client=FakeChat())
