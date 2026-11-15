
from pathlib import Path
import sqlite3
import pandas as pd

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "inventory.db"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH)

# Query: Product inventory analytics
query = """
WITH stock_summary AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        p.cost_price,
        p.selling_price,
        p.min_stock,

        SUM(
            CASE
                WHEN t.transaction_type = 'IN'
                    THEN t.quantity
                WHEN t.transaction_type = 'OUT'
                    THEN -t.quantity
                ELSE 0
            END
        ) AS current_stock,

        SUM(
            CASE
                WHEN t.transaction_type = 'OUT'
                    THEN t.quantity
                ELSE 0
            END
        ) AS total_stock_out

    FROM products p
    LEFT JOIN stock_transactions t
        ON p.product_id = t.product_id

    GROUP BY
        p.product_id,
        p.product_name,
        p.category,
        p.cost_price,
        p.selling_price,
        p.min_stock
)

SELECT
    *,
    current_stock * cost_price AS inventory_value,
    CASE
        WHEN current_stock <= min_stock
            THEN 'LOW STOCK'
        ELSE 'NORMAL'
    END AS stock_status
FROM stock_summary
"""

df = pd.read_sql_query(query, conn)

# Calculate business metrics
total_products = len(df)
total_stock = df["current_stock"].sum()
total_inventory_value = df["inventory_value"].sum()
total_stock_out = df["total_stock_out"].sum()

lowest_stock_product = df.loc[
    df["current_stock"].idxmin()
]

top_product = df.loc[
    df["total_stock_out"].idxmax()
]

# Display analytics report
print("=" * 50)
print("INVENTORY MANAGEMENT ANALYTICS REPORT")
print("=" * 50)

print(f"Total Products        : {total_products}")
print(f"Total Current Stock   : {total_stock}")
print(f"Total Stock Out       : {total_stock_out}")
print(f"Inventory Value       : Rp {total_inventory_value:,.0f}")

print("\nLOWEST STOCK PRODUCT")
print(lowest_stock_product[
    ["product_name", "current_stock", "min_stock"]
].to_string())

print("\nTOP STOCK OUT PRODUCT")
print(top_product[
    ["product_name", "total_stock_out"]
].to_string())

# Category analysis
category_analysis = (
    df.groupby("category")
    .agg(
        total_products=("product_id", "count"),
        total_stock=("current_stock", "sum"),
        total_stock_out=("total_stock_out", "sum"),
        inventory_value=("inventory_value", "sum")
    )
    .reset_index()
)

print("\nCATEGORY PERFORMANCE")
print(category_analysis.to_string(index=False))

# Export results
df.to_csv(
    OUTPUT_DIR / "product_analytics.csv",
    index=False
)

category_analysis.to_csv(
    OUTPUT_DIR / "category_analysis.csv",
    index=False
)

conn.close()

print("\nAnalytics completed successfully.")
print("Output files saved in the output folder.")
