from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.models_orders import Order
    from app.core.models_products import Product


class OrderProductAssociation(Base):
    __tablename__ = "order_product_association_table"
    __table_args__ = (
        UniqueConstraint(
            "order_id",
            "product_id",
            name="idx_unique_order_product",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    count: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    unit_price: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    # Association betwee Association -> Order
    order: Mapped["Order"] = relationship(back_populates="product_details")
    # Association betwee Association -> Product
    product: Mapped["Product"] = relationship(back_populates="orders_details")

    # order_product_association_table = Table(
    #     # "order_product_association_table",
    #     # Base.metadata,
    #     Column("id", Integer, primary_key=True),
    #     Column("order_id", ForeignKey("orders.id"), nullable=False),
    #     Column("product_id", ForeignKey("products.id"), nullable=False),
    #     UniqueConstraint("order_id", "product_id", name="idx_unique_order_product"),
    # )
