# lets the agent query the procurement database using raw sql.
# the docstring doubles as the tool description the llm reads to
# know what tables exist and how to write queries against them.

import json
from langchain.tools import tool
from backend.app.data_access.loader import db


@tool
def product_search(sql_query: str) -> str:
    """
    Query the procurement database using SQL. Returns results as JSON.

    DATABASE SCHEMA
    ===============

    Table: products
    ---------------
    Columns: id (INTEGER PK), name (TEXT), brand (TEXT), category (TEXT),
      description (TEXT), pack_size (TEXT), price (REAL), supplier (TEXT),
      review_stars (INTEGER 1-5), ingredients (TEXT), calories_per_serving (INTEGER),
      sodium_mg_per_serving (INTEGER), dietary_flags (TEXT — comma-separated,
      e.g. "vegan,gluten_free,low_sodium,heart_healthy,diabetic_friendly,nut_free")

    Categories: protein, dairy, grains_bread, pasta, pantry, produce,
      beverage, breakfast, prepared_meals

    Table: contracts
    ----------------
    Columns: id (INTEGER PK), category (TEXT), approved_brands (TEXT — comma-separated),
      approved_pack_sizes (TEXT — comma-separated), approved_suppliers (TEXT — comma-separated),
      required_dietary_flags (TEXT — comma-separated), prohibited_ingredients (TEXT — comma-separated),
      max_sodium_mg_per_serving (INTEGER or NULL), max_price_per_unit (REAL or NULL),
      facility (TEXT — always 'karls_senior_living_dallas'),
      effective_start (TEXT — ISO date), effective_end (TEXT — ISO date),
      is_active (INTEGER — 1=active, 0=expired)

    Table: inventory
    ----------------
    Columns: id (INTEGER PK), product_id (INTEGER FK→products.id),
      distribution_center (TEXT — 'midwest_dc', 'southeast_dc', 'northeast_dc'),
      quantity_available (INTEGER), stock_status (TEXT — 'in_stock', 'low_stock', 'out_of_stock'),
      last_updated (TEXT — ISO timestamp), lead_time_days (INTEGER)

    QUERY TIPS
    ==========
    - Use LIKE with % wildcards for text searches: WHERE name LIKE '%chicken%'
    - Check contract compliance: WHERE approved_brands LIKE '%Prime Poultry%'
    - Join products to inventory: SELECT p.*, i.quantity_available, i.stock_status
        FROM products p JOIN inventory i ON p.id = i.product_id
    - Filter active contracts: WHERE is_active = 1
    - All contracts apply to Karl's Senior Living of Dallas: WHERE facility = 'karls_senior_living_dallas'
    """
    cursor = db.execute(sql_query)
    rows = cursor.fetchall()
    return json.dumps([dict(row) for row in rows], default=str)
