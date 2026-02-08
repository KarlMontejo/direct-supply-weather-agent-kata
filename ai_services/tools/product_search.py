"""
Product search tool — queries the in-memory product database via SQL.
"""

from langchain.tools import tool

from backend.app.schemas.product import Product
from ai_services.data_access.loader import db


@tool
def product_search(sql_query: str) -> list[Product]:
    """
    Search for products in the database using SQL.

    Database schema:
    - Table: products
    - Columns: id (INTEGER), name (TEXT), description (TEXT), price (REAL),
      stock_quantity (INTEGER), supplier (TEXT), review_stars (INTEGER 1-5)

    Examples:
    - SELECT * FROM products WHERE name LIKE '%bread%'
    - SELECT * FROM products WHERE price < 10 AND stock_quantity > 0
    - SELECT * FROM products WHERE name LIKE '%bacon%' OR name LIKE '%lettuce%' OR name LIKE '%tomato%'

    Always use LIKE with % wildcards for name searches. Quote string literals properly.
    """
    cursor = db.execute(sql_query)
    rows = cursor.fetchall()
    return [Product(**row) for row in rows]
