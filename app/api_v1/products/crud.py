"""
CREATE
READ
UPDATE
DELETE
"""

from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models_products import Product
from .schemas import ProductCreate, ProductUpdate, ProductUpdatePartial


async def get_all_products(
    session: AsyncSession,
) -> list[Product]:
    query = select(Product).order_by(Product.id)
    result: Result = await session.execute(query)
    products = result.scalars().all()
    return list(products)


async def get_product_by_id(
    product_id: int,
    session: AsyncSession,
) -> Product | None:
    return await session.get(Product, product_id)


async def create_new_product(
    session: AsyncSession,
    product: ProductCreate,
) -> Product:
    new_product = Product(**product.model_dump())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product


# model_dump может принимать параметры exclude_none, exclude_unset, exclude_default = bool
async def update_product(
    session: AsyncSession,
    product: Product,
    product_update: ProductUpdate | ProductUpdatePartial,
    partial: bool = False,
) -> Product:
    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)
    await session.commit()
    await session.refresh(product)
    return product


async def update_products_partial(
    session: AsyncSession,
    product: Product,
    product_update: ProductUpdatePartial,
) -> Product:
    for name, value in product_update.model_dump(exclude_unset=True).items():
        setattr(product, name, value)
    await session.commit()
    await session.refresh(product)
    return product


# async def update_product_partial_by_id(
#     product_id: int,
#     session: AsyncSession,
#     product_update: ProductUpdatePartial,
# ) -> Product | None:
#     return await session.get(Product, product_id)


async def delete_product(
    session: AsyncSession,
    product: Product,
) -> None:
    await session.delete(product)
    await session.commit()
