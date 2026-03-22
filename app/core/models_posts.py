from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, ForeignKey
from app.core.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.models_users import User


class Post(Base):
    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(
        Text,
        default="",
        server_defaul="",
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )

    # TYPE_CHECKING: USER from models_users
    user: Mapped["User"] = relationship(back_populates="posts")
