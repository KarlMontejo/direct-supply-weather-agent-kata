CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NOT NULL,
    stock_quantity INTEGER NOT NULL,
    supplier TEXT NOT NULL,
    review_stars INTEGER NOT NULL CHECK(review_stars BETWEEN 1 AND 5)
);
