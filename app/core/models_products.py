from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer
from core.base import Base


class Product(Base):
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer)
