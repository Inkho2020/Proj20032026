from fastapi import APIRouter, HTTPException
from app.schemas import schema_users

router = APIRouter(tags=["USERS"], prefix="/users")


user_list = []


@router.post("/")
async def create_new_user(user: schema_users.UserCreate):
    new_user = user.model_dump()  # передает в schema словарь
    user_list.append(new_user)
    return {"user_created": new_user}


@router.get("/{user_id}")
async def get_users_by_id(user_id: int):
    return user_list[user_id]
