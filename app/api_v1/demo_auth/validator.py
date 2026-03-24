from fastapi import Depends, HTTPException, Form

# HTTPBear поозволяет вытащить ТОКЕН в ручную через token=credentials.credentials
# OAuth2PasswordBearer записывает ТОКЕН в загаловок, и все работает автоматически.
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import BaseModel
from starlette import status

from app.api_v1.demo_auth.create_token import (
    TOKEN_TYPE_KEY,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from app.auth import utils as auth_utils
from app.schemas.schema_users import UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/demo-auth/jwt/login/")
# тут http_bearer нужен, чтобы получить дополнительный refresh токен
# по умолчанию выкидывает ошибку если вставить в роутер
http_bearer = HTTPBearer(auto_error=False)

john = UserSchema(
    username="john",
    password=auth_utils.hash_pass("pass"),
    email="123@i.ua",
)
ann = UserSchema(
    username="ann",
    password=auth_utils.hash_pass("1234"),
    email="456@i.ua",
)
users_db: dict[str, UserSchema] = {
    john.username: john,
    ann.username: ann,
}


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


def validate_user(
    username: str = Form(),
    password: str = Form(),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid user or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    if not (user := users_db.get(username)):
        raise credentials_exception

    if not auth_utils.validate_password(
        password=password, hashed_password=user.password
    ):
        raise credentials_exception

    if not user.is_active:
        raise credentials_exception

    return user


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    if payload.get(TOKEN_TYPE_KEY) == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid token type",
    )


def get_user_by_token_name(payload: dict) -> UserSchema:
    username: str | None = payload.get("username")
    if not (user := users_db.get(username)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No such user",
        )
    return user


def get_token_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme),
) -> UserSchema:
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}"
        )
    return payload


def get_current_user_access_jwt(
    payload: dict = Depends(get_token_payload),
) -> UserSchema:
    validate_token_type(payload, ACCESS_TOKEN_TYPE)
    return get_user_by_token_name(payload)


def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_token_payload),
) -> UserSchema:
    validate_token_type(payload, REFRESH_TOKEN_TYPE)
    return get_user_by_token_name(payload)


def get_current_auth_user_jwt(
    user: UserSchema = Depends(get_current_user_access_jwt),
) -> UserSchema:
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )
