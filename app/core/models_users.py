from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer
from app.core.base import Base


class User(Base):
    name: Mapped[str] = mapped_column(String(50))
