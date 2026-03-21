import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import items, users

origins = ["http://localhost:8080"]

app = FastAPI(
    title="APP-Shop",
    description="",
    version="0.1.0",
    on_startup=None,
    on_shutdown=None,
    lifespan=None,
    # contact="khoin2@yahoo.com"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router)
app.include_router(users.router)


@app.get("/", tags=["PathOperationTAG"])
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
