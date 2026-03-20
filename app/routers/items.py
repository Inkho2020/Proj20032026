from fastapi import APIRouter, Path
from typing import Annotated
from app.schemas import schema_itemes

router = APIRouter(
    tags=["ITEMS"],
    prefix='/items'
)


@router.post("/")
async def create_item(item: schema_itemes.Item):
    return {
        "item_id": item.phone_number
    }


@router.get("/{item_id}")
# через Path можно передать условие, например ">=1" и "<1000..." / import Annotated from typing
async def get_item_by_id(item_id: Annotated[int, Path(ge=1, lt=1_000_000)]):
    return {
        "item": {
            "id": f"{item_id}"
        }
    }
