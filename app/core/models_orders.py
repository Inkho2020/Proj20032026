from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, func, DateTime
from app.core.base import Base
from app.core.models_orders_products import OrderProductAssociation
from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.models_products import Product


class Order(Base):
    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        default=datetime.now,
    )

    # связка многие ко многоим через ТАБЛИЦУ "order_product_association_table"
    # products: Mapped[list["Product"]] = relationship(
    #     secondary="order_product_association_table",
    #     back_populates="orders",
    # )

    # связка через ассоциативную МОДЕЛЬ
    product_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order"
    )
