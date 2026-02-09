-- ============================================================
-- Products — enriched catalog with nutrition, ingredients, and
-- dietary flags for compliance validation
-- ============================================================
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    pack_size TEXT NOT NULL,
    price REAL NOT NULL,
    supplier TEXT NOT NULL,
    review_stars INTEGER NOT NULL CHECK(review_stars BETWEEN 1 AND 5),
    ingredients TEXT NOT NULL,
    calories_per_serving INTEGER NOT NULL,
    sodium_mg_per_serving INTEGER NOT NULL,
    dietary_flags TEXT NOT NULL DEFAULT ''
);

-- ============================================================
-- Contracts — procurement rules per category per facility.
-- Comma-separated fields encode approved lists.
-- Facility 'all' = default; named facilities override.
-- ============================================================
CREATE TABLE contracts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    approved_brands TEXT NOT NULL,
    approved_pack_sizes TEXT NOT NULL,
    approved_suppliers TEXT NOT NULL,
    required_dietary_flags TEXT NOT NULL DEFAULT '',
    prohibited_ingredients TEXT NOT NULL DEFAULT '',
    max_sodium_mg_per_serving INTEGER,
    max_price_per_unit REAL,
    facility TEXT NOT NULL DEFAULT 'all',
    effective_start TEXT NOT NULL,
    effective_end TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);

-- ============================================================
-- Inventory — per-distribution-center availability.
-- stock_status: 'in_stock', 'low_stock', 'out_of_stock'
-- ============================================================
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES products(id),
    distribution_center TEXT NOT NULL,
    quantity_available INTEGER NOT NULL,
    stock_status TEXT NOT NULL CHECK(stock_status IN ('in_stock', 'low_stock', 'out_of_stock')),
    last_updated TEXT NOT NULL,
    lead_time_days INTEGER NOT NULL DEFAULT 1
);
