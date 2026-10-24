"""Logging setup that never writes secret values (NFR-01, spec §16)."""

import logging
from collections.abc import Iterable

LOGGER_NAME = "pekael"
REDACTED = "***"


class RedactingFormatter(logging.Formatter):
    """Formatter that replaces known secret values in the final message, including tracebacks."""

    def __init__(self, secrets: Iterable[str], fmt: str | None = None):
        super().__init__(fmt)
        # Longest first so a secret containing another secret is fully masked.
        self._secrets = sorted({s for s in secrets if s}, key=len, reverse=True)

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        for secret in self._secrets:
            message = message.replace(secret, REDACTED)
        return message


def configure_logging(level: str = "INFO", secrets: Iterable[str] = ()) -> logging.Logger:
    """Configure the ``pekael`` logger once; calling again replaces its handler."""
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    logger.propagate = False
    for handler in list(logger.handlers):
        logger.removeHandler(handler)

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(secrets, "%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logger.addHandler(handler)
    return logger
