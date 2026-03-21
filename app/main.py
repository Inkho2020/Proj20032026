import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.base import Base
from app.core.db_helper import db_helper
from app.routers import items, users
from app.api_v1 import router as router_v1

origins = ["http://localhost:8080"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="APP-Shop", description="", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
app.include_router(items.router)
app.include_router(users.router)


@app.get("/", tags=["PathOperationTAG"])
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
