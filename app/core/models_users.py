from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer
from app.core.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.models_posts import Post


class User(Base):
    name: Mapped[str] = mapped_column(String(50))

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
