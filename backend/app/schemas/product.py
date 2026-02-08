from pydantic import BaseModel
from typing import Literal

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock_quantity: int
    supplier: str
    review_stars: Literal[1,2,3,4,5]