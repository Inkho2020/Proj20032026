from fastapi import HTTPException, Depends, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_helper import db_helper
from . import crud
from typing import Annotated
from app.core.models_products import Product


async def product_by_id(
    product_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Product:
    product = await crud.get_product_by_id(
        product_id=product_id,
        session=session,
    )
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product
