from fastapi import APIRouter
from .products.views import router as products_router

router = APIRouter(
    tags=["PRODUCTS"],
)

router.include_router(
    products_router,
    prefix="/products",
)
