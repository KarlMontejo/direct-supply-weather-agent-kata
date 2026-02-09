# spins up an in-memory sqlite database and seeds it with our mock data.
# the db lives for the lifetime of the process — no disk, no persistence,
# just fast reads for the agent's tool calls.

import json
import sqlite3
from pathlib import Path

_APP_ROOT = Path(__file__).resolve().parent.parent      # backend/app/
_BACKEND_ROOT = _APP_ROOT.parent                        # backend/

SCHEMA_PATH = _BACKEND_ROOT / "db" / "schema.sql"
PRODUCTS_PATH = _APP_ROOT / "data" / "products.jsonl"
CONTRACTS_PATH = _APP_ROOT / "data" / "contracts.jsonl"
INVENTORY_PATH = _APP_ROOT / "data" / "inventory.jsonl"


def _load_jsonl(conn: sqlite3.Connection, table: str, path: Path) -> None:
    # reads a jsonl file line by line and inserts each row into the table
    with open(path) as f:
        for line in f:
            row = json.loads(line)
            cols = ", ".join(row.keys())
            vals = ", ".join(f":{k}" for k in row.keys())
            conn.execute(
                f"INSERT INTO {table} ({cols}) VALUES ({vals})", row
            )


def init_db() -> sqlite3.Connection:
    # creates the in-memory db, applies the schema, and loads seed data
    conn = sqlite3.connect(":memory:", check_same_thread=False)

    conn.executescript(SCHEMA_PATH.read_text())

    _load_jsonl(conn, "products", PRODUCTS_PATH)
    _load_jsonl(conn, "contracts", CONTRACTS_PATH)
    _load_jsonl(conn, "inventory", INVENTORY_PATH)
    conn.commit()

    # Row factory lets us access columns by name instead of index
    conn.row_factory = sqlite3.Row
    return conn


# created once when the module is first imported, shared everywhere
db = init_db()
