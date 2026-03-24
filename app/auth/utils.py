from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from app.core.config import settings
import bcrypt


# создать токен, передать данные пользователя, ключи, алгоритм, время жизни токена и время продления
# токен возвращает данные пользователя, срок токена, и его jti - уникальный номер
def encode_jwt(
    payload: dict,
    private_key: str = settings.authJWT.private_key_path.read_text(),
    algorithm: str = settings.authJWT.algorithm,
    token_life_time: int = settings.authJWT.access_token_expire_min,
    refresh_time: int | None = None,
):
    to_encode = payload.copy()
    if refresh_time:
        expire = datetime.now() + timedelta(refresh_time)
    else:
        expire = datetime.now() + timedelta(token_life_time)
    to_encode.update(
        exp=expire,
        jti=uuid4().hex,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.authJWT.public_key_path.read_text(),
    algorithm: str = settings.authJWT.algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_pass(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode("utf-8")
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode("utf-8"),
        hashed_password=hashed_password,
    )
