# mirrors the products table in the database.
# used by the product_search tool to validate rows coming back from sql.

from pydantic import BaseModel
from typing import Literal


class Product(BaseModel):
    id: int
    name: str
    brand: str
    category: str
    description: str
    pack_size: str
    price: float
    supplier: str
    review_stars: Literal[1, 2, 3, 4, 5]
    ingredients: str
    calories_per_serving: int
    sodium_mg_per_serving: int
    dietary_flags: str
