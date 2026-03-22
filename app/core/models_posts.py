from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer, ForeignKey
from app.core.base import Base


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
