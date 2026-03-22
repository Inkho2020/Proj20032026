from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer, func, DateTime
from app.core.base import Base
from datetime import datetime


class Order(Base):
    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        default=datetime.now,
    )
