from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from annotated_types import MaxLen, MinLen


class UserBase(BaseModel):
    name: Annotated[str, MinLen(3), MaxLen(50)]  # modern version
    surname: str = Field(..., min_length=2, max_length=20)  # old version
    email: EmailStr


class UserCreate(UserBase):
    pass

