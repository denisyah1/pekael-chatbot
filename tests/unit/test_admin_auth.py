import pytest
from pydantic import SecretStr

from pekael.services.admin_auth import AdminAuthenticator


@pytest.fixture
def auth() -> AdminAuthenticator:
    return AdminAuthenticator("admin", SecretStr("s3cret-Pass"))


def test_correct_credentials_accepted(auth):
    assert auth.verify("admin", "s3cret-Pass")


@pytest.mark.parametrize(
    ("username", "password"),
    [("admin", "wrong"), ("other", "s3cret-Pass"), ("", ""), ("admin", "s3cret-pass"), ("admin", "kata sandi é")],
)
def test_wrong_credentials_rejected(auth, username, password):
    assert not auth.verify(username, password)


@pytest.mark.parametrize(("username", "password"), [(None, None), ("admin", None), ("admin", SecretStr("")), (None, SecretStr("x"))])
def test_login_disabled_when_not_configured(username, password):
    auth = AdminAuthenticator(username, password)

    assert not auth.is_configured
    assert not auth.verify(username or "", "")
