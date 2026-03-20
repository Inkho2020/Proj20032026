from pydantic import BaseModel
from typing import Union


class ItemBase(BaseModel):
    phone_number: Union[int, str]


class Item(ItemBase):
    pass

