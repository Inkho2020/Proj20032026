from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer
from app.core.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.models_posts import Post
    from app.core.models_users_profile import Profile


class User(Base):
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str]
    email: Mapped[str]

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.name!r})"

    def __repr__(self):
        return str(self)
