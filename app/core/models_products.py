from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer
from app.core.base import Base
from app.core.models_orders_products import OrderProductAssociation

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.models_orders import Order


class Product(Base):
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer)

    # связка многие ко многоим через ТАБЛИЦУ "order_product_association_table"
    # orders: Mapped[list["Order"]] = relationship(
    #     secondary="order_product_association_table",
    #     back_populates="products",
    # )

    # связка через ассоциативную МОДЕЛЬ
    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product"
    )
