"""Single admin account check (FR-06). Credentials come from configuration only."""

import hmac

from pydantic import SecretStr


class AdminAuthenticator:
    def __init__(self, username: str | None, password: SecretStr | None) -> None:
        self._username = username or ""
        self._password = password.get_secret_value() if password else ""

    @property
    def is_configured(self) -> bool:
        return bool(self._username and self._password)

    def verify(self, username: str, password: str) -> bool:
        if not self.is_configured:
            return False
        # Compare both fields in constant time and without short-circuiting.
        username_ok = hmac.compare_digest(username.encode("utf-8"), self._username.encode("utf-8"))
        password_ok = hmac.compare_digest(password.encode("utf-8"), self._password.encode("utf-8"))
        return username_ok & password_ok
