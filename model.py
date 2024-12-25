from pydantic import BaseModel
from typing import List, Optional


class Menu(BaseModel):
    name: str
    description: str
    price: int


class ResultExpandedItem(BaseModel):
    name: str
    calories: int
    price: int
    count: int
    category: str
    type: str


class Items(BaseModel):
    total_calories: int
    total_price: int
    result_expanded: List[ResultExpandedItem]


class ResponseModel(BaseModel):
    items: Optional[Items] = None
    menu: Optional[Menu] = None
    annotated_image_path: Optional[str] = None
    error: Optional[str] = None
