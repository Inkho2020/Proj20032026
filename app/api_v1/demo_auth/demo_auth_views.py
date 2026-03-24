import secrets
import uuid
from datetime import time

from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie

# HTTPBasicCredentials - это pydantic BasicModel: username, password
# HTTPBasic - это готовое решение дла аутентификации (проверка пароля и юзера) oauth2+auth.py без возврата юзера
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated, Any, Optional

router = APIRouter(
    tags=["DEMO-Auth"],
    prefix="/demo-auth",
)
security = HTTPBasic()


@router.get("/basic-auth/")
async def demo_basic_auth(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message": "Authentication done",
        "username": credentials.username,
        "password": credentials.password,
    }


################# AUTHENTICATION BY USER AND PASSWORD ##############

username_to_password = {
    "admin": "admin",
    "john": "pass",
}


def demo_classic_get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid user or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = username_to_password.get(credentials.username)
    if correct_password is None:
        raise credentials_exception
    if credentials.username not in username_to_password:
        raise credentials_exception

    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise credentials_exception
    return credentials.username


@router.get("/basic-auth-username/")
async def demo_basic_auth_by_username_password(
    auth_user: str = Depends(demo_classic_get_current_user),
):
    return {"message": f"Hello, {auth_user}, password"}


############## AUTHENTICATE BY STATIC TOKEN ####################

static_auth_token_to_user = {
    "admin_secret_token": "admin",
    "john_secret_token": "john",
}


def demo_get_user_by_static_token(
    static_token: str = Header(alias="x-auth-token"),
) -> str:
    if token := static_auth_token_to_user.get(static_token):
        return token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
    )


@router.get("/some-http-header-auth/")
async def demo_auth_http_header_by_static_token(
    auth_user: str = Depends(demo_get_user_by_static_token),
):
    return {"message": f"Hello, {auth_user}"}


############## AUTHENTICATE BY COOKIES #######################

COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"


# generate uuid for session
def generate_session_id() -> str:
    return uuid.uuid4().hex


# check current COOKIE
def get_session_data(
    session_idd: Optional[str] = Cookie(alias=COOKIE_SESSION_ID_KEY),
) -> dict:
    if session_idd not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not found cookie",
        )
    return COOKIES[session_idd]


@router.post("/login-cookie/")
async def demo_auth_login_set_cookie(
    response: Response,
    auth_user: str = Depends(demo_get_user_by_static_token),
):
    session_idd = generate_session_id()  # генерируем случайный uuid для сессии
    # session_idd записываем в COOKIES словарь(в будущем в бд), ключ session_id, значения любые значения.
    COOKIES[session_idd] = {
        "username": auth_user,
        "login_time": time(),
    }
    # регистрируем session_idd в Response, чтобы потом получить данные пользователья по session_idd (get_session_data)
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_idd)
    return {"message": f"Result is ok"}


@router.get("/check-cookie")
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data["username"]
    return {
        "username": f"Current login: {username}",
        **user_session_data,
    }


@router.get("/logou-cookie", tags=["Logout"])
def demo_auth_logout_cookie(
    response: Response,
    session_idd: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_idd)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {
        "message": f"logout: {username}",
    }
