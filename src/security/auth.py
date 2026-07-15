"""
FloraGuard — JWT Kimlik Doğrulama
Kullanıcı adı/şifre doğrulama ve JWT üretim/çözümleme fonksiyonları.
RBAC kararları (rol kontrolü) bilerek burada değil `rbac.py`'de — bu modül
SADECE "bu kullanıcı kim ve token'ı geçerli mi" sorusuna cevap verir.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from jwt import InvalidTokenError

from src.data.schemas import Role, TokenPayload
from src.security.users_db import get_user, verify_password


def authenticate_user(db_path: Path, username: str, password: str) -> dict | None:
    user = get_user(db_path, username)
    if user is None or not verify_password(password, user["hashed_password"]):
        return None
    return user


def create_access_token(
    username: str, role: Role, secret_key: str, algorithm: str, expire_minutes: int,
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    payload = {"sub": username, "role": role.value, "exp": expire}
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode_access_token(token: str, secret_key: str, algorithm: str) -> TokenPayload:
    try:
        raw = jwt.decode(token, secret_key, algorithms=[algorithm])
    except InvalidTokenError as exc:
        raise ValueError("Geçersiz veya süresi dolmuş token.") from exc
    return TokenPayload(sub=raw["sub"], role=Role(raw["role"]), exp=raw["exp"])
