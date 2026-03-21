from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_helper import db_helper

from . import crud
from .schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial
from .dependencies import product_by_id

router = APIRouter()


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product: ProductCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_new_product(
        session=session,
        product=product,
    )


@router.get("/", response_model=list[Product])
async def get_products(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_all_products(session=session)


@router.get("/{product_id}", response_model=Product)
async def get_product_by_id(
    product: Product = Depends(product_by_id),
):
    # Depends(product_by_id form dependency.py!!!!!
    return product


# AAAAAAAAAA!!!!!!!!! Deptends(product_by_id) - сразу возвращает Prodcut, id берет из Пути('/{product_id}')!!!!!
@router.put(
    "/{product_id}",
    status_code=status.HTTP_201_CREATED,
)
async def update_product_by_id(
    product_update: ProductUpdate,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
    )


@router.patch(
    "/{product_id}",
    status_code=status.HTTP_201_CREATED,
)
async def update_product_partial_by_id(
    product_update: ProductUpdatePartial,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_products_partial(
        session=session,
        product=product,
        product_update=product_update,
    )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def product_delete(
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.delete_product(
        product=product,
        session=session,
    )
