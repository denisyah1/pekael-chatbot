import logging

from pekael.config.logging_config import REDACTED, RedactingFormatter, configure_logging


def _record(message: str, exc_info=None) -> logging.LogRecord:
    return logging.LogRecord("pekael", logging.ERROR, __file__, 1, message, None, exc_info)


def test_secret_is_redacted_from_message():
    formatter = RedactingFormatter(["sk-secret-value"])

    output = formatter.format(_record("calling API with key sk-secret-value"))

    assert "sk-secret-value" not in output
    assert REDACTED in output


def test_secret_is_redacted_from_traceback():
    formatter = RedactingFormatter(["sk-secret-value"])
    try:
        raise RuntimeError("auth failed for sk-secret-value")
    except RuntimeError:
        import sys

        output = formatter.format(_record("request failed", sys.exc_info()))

    assert "sk-secret-value" not in output


def test_configure_logging_replaces_handler():
    configure_logging("INFO", ["a-secret"])
    logger = configure_logging("DEBUG", ["a-secret"])

    assert len(logger.handlers) == 1
    assert logger.level == logging.DEBUG
