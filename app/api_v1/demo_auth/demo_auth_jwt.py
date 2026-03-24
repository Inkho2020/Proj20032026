from app.api_v1.demo_auth.create_token import (
    create_access_token,
    create_refresh_token,
)
from app.api_v1.demo_auth.validator import (
    get_current_auth_user_jwt,
    get_current_auth_user_for_refresh,
    validate_user,
    http_bearer,
    Token,
)
from app.schemas.schema_users import UserSchema


from fastapi import APIRouter, Depends

router = APIRouter(prefix="/jwt", tags=["JWT"], dependencies=[Depends(http_bearer)])


@router.post("/login/", response_model=Token)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_user),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/users/me/")
def get_user_by_access_jwt(
    user: UserSchema = Depends(get_current_auth_user_jwt),
):
    return {
        "username": user.username,
        "email": user.email,
    }


@router.post(
    "/refresh",
    response_model=Token,
    response_model_exclude_none=True,
)
def auth_user_refresh_jwt(
    user: UserSchema = Depends(get_current_auth_user_for_refresh),
):
    access_token = create_access_token(user)
    return Token(
        access_token=access_token,
    )
