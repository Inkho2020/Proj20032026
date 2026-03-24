from datetime import timedelta

from app.auth import utils as auth_utils
from app.core import settings
from app.schemas.schema_users import UserSchema

TOKEN_TYPE_KEY = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(
    token_type: str,
    payload: dict,
    token_life_time: int = settings.authJWT.access_token_expire_min,
    refresh_time: int | None = None,
) -> str:  # payload = token_data
    jwt_payload = {TOKEN_TYPE_KEY: token_type}
    jwt_payload.update(payload)
    return auth_utils.encode_jwt(
        payload=jwt_payload,
        token_life_time=token_life_time,
        refresh_time=refresh_time,
    )


def create_access_token(user: UserSchema):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        payload=jwt_payload,
        token_life_time=settings.authJWT.access_token_expire_min,
    )


def create_refresh_token(user: UserSchema):
    jwt_payload = {"username": user.username}
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        payload=jwt_payload,
        refresh_time=settings.authJWT.refresh_token_expire_time,
    )
