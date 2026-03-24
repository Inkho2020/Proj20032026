from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_helper
from app.core.models_users import User
from app.schemas import schema_users
from sqlalchemy import select

router = APIRouter(tags=["USERS"], prefix="/users")


user_list = []


@router.post("/")
async def create_new_user(user: schema_users.UserCreate):
    new_user = user.model_dump()  # передает в schema словарь
    user_list.append(new_user)
    return {"user_created": new_user}


@router.get("/{user_id}")
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(db_helper.session_dependency),):
    query = select(User).where(User.id == user_id)
    user = await session.scalar(query)
    return user
