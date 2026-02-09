# represents a proposed order that gets passed to the compliance checker.

from pydantic import BaseModel
from typing import List


class LineItem(BaseModel):
    product_id: int
    quantity: int


class ProductOrder(BaseModel):
    line_items: List[LineItem]
