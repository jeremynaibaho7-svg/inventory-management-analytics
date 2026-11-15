
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "database"

DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "inventory.db"

# Load datasets
suppliers = pd.read_csv(DATA_DIR / "suppliers.csv")
products = pd.read_csv(DATA_DIR / "cleaned_inventory.csv")
transactions = pd.read_csv(DATA_DIR / "transactions.csv")

# Connect to database
with sqlite3.connect(DB_PATH) as conn:

    conn.execute("PRAGMA foreign_keys = ON")

    # Drop old tables in dependency order
    conn.execute("DROP TABLE IF EXISTS stock_transactions")
    conn.execute("DROP TABLE IF EXISTS products")
    conn.execute("DROP TABLE IF EXISTS suppliers")

    # Create suppliers
    conn.execute("""
        CREATE TABLE suppliers (
            supplier_id TEXT PRIMARY KEY,
            supplier_name TEXT NOT NULL,
            city TEXT
        )
    """)

    # Create products
    conn.execute("""
        CREATE TABLE products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            supplier_id TEXT NOT NULL,
            cost_price REAL NOT NULL CHECK(cost_price >= 0),
            selling_price REAL NOT NULL CHECK(selling_price >= 0),
            min_stock INTEGER NOT NULL CHECK(min_stock >= 0),
            FOREIGN KEY (supplier_id)
                REFERENCES suppliers(supplier_id)
        )
    """)

    # Create stock transactions
    conn.execute("""
        CREATE TABLE stock_transactions (
            transaction_id TEXT PRIMARY KEY,
            product_id TEXT NOT NULL,
            transaction_type TEXT NOT NULL
                CHECK(transaction_type IN ('IN', 'OUT')),
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            transaction_date DATE NOT NULL,
            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
        )
    """)

    # Import data without replacing table structures
    suppliers.to_sql(
        "suppliers", conn, if_exists="append", index=False
    )

    products[[
        "product_id", "product_name", "category",
        "supplier_id", "cost_price", "selling_price", "min_stock"
    ]].to_sql(
        "products", conn, if_exists="append", index=False
    )

    transactions.to_sql(
        "stock_transactions", conn,
        if_exists="append", index=False
    )

    # Verify record counts
    print("DATABASE REBUILT SUCCESSFULLY")

    for table in ["suppliers", "products", "stock_transactions"]:
        count = conn.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]
        print(f"{table}: {count} records")

    # Verify foreign keys
    for table in ["products", "stock_transactions"]:
        violations = conn.execute(
            f"PRAGMA foreign_key_check({table})"
        ).fetchall()
        print(f"{table} foreign key violations: {len(violations)}")
