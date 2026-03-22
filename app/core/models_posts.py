from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, ForeignKey
from app.core.base import Base
from app.core.models_mixins import UserRalationMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.models_users import User


class Post(UserRalationMixin, Base):
    # _user_id_nullable: bool
    # _user_id_unique: bool
    _user_back_populates = "posts"
    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    # import from app.core.models_mixins UserRelationMixin
    # user_id: Mapped[int] = mapped_column(
    #     ForeignKey("users.id"),
    # )

    # TYPE_CHECKING: USER from models_users
    # user: Mapped["User"] = relationship(back_populates="posts")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title!r})"

    def __repr__(self):
        return str(self)
