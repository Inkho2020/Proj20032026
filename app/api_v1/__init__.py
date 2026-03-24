from fastapi import APIRouter
from .products.views import router as products_router
from .demo_auth.demo_auth_views import router as demo_auth_router
from .demo_auth.demo_auth_jwt import router as demo_jwt

router = APIRouter(
    tags=["PRODUCTS"],
)

router.include_router(
    products_router,
    prefix="/products",
)
router.include_router(
    demo_auth_router,
)

router.include_router(
    demo_jwt
)

