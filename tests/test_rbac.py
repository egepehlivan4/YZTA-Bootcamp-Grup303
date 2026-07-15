import pytest
from fastapi import HTTPException

from src.data.schemas import Role, TokenPayload
from src.security.auth import create_access_token, decode_access_token
from src.security.rbac import require_role

SECRET = "test-secret"
ALGORITHM = "HS256"


def test_token_roundtrip():
    token = create_access_token(
        username="ciftci1", role=Role.FARMER, secret_key=SECRET, algorithm=ALGORITHM, expire_minutes=5,
    )
    payload = decode_access_token(token, secret_key=SECRET, algorithm=ALGORITHM)

    assert payload.sub == "ciftci1"
    assert payload.role == Role.FARMER


def test_decode_rejects_tampered_token():
    token = create_access_token(
        username="ciftci1", role=Role.FARMER, secret_key=SECRET, algorithm=ALGORITHM, expire_minutes=5,
    )
    with pytest.raises(ValueError):
        decode_access_token(token, secret_key="wrong-secret", algorithm=ALGORITHM)


def test_require_role_allows_matching_role():
    checker = require_role(Role.ADVISOR, Role.ADMIN)
    user = TokenPayload(sub="danisman1", role=Role.ADVISOR, exp=9999999999)
    assert checker(current_user=user) == user


def test_require_role_blocks_mismatched_role():
    checker = require_role(Role.ADVISOR, Role.ADMIN)
    user = TokenPayload(sub="ciftci1", role=Role.FARMER, exp=9999999999)
    with pytest.raises(HTTPException) as exc_info:
        checker(current_user=user)
    assert exc_info.value.status_code == 403
