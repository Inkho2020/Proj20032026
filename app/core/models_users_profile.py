from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, ForeignKey
from app.core.base import Base
from app.core.models_mixins import UserRalationMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.models_users import User


class Profile(Base, UserRalationMixin):
    _user_id_unique = True
    _user_back_populates = "profile"
    name: Mapped[str | None] = mapped_column(String(50))
    surname: Mapped[str | None] = mapped_column(String(50))
    bio: Mapped[str | None] = mapped_column(Text)

    # user_id: Mapped[int] = mapped_column(
    #     ForeignKey("users.id"),
    #     unique=True,
    # )
