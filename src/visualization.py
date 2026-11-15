
from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "inventory.db"
CHART_DIR = BASE_DIR / "output" / "charts"

CHART_DIR.mkdir(parents=True, exist_ok=True)

# Connect database
conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.cost_price,
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
    p.min_stock
"""

df = pd.read_sql_query(query, conn)
conn.close()

df["inventory_value"] = (
    df["current_stock"] * df["cost_price"]
)

df["stock_status"] = df.apply(
    lambda row: "LOW STOCK"
    if row["current_stock"] <= row["min_stock"]
    else "NORMAL",
    axis=1
)

# Chart 1: Stock Level by Product
stock_df = df.sort_values(
    "current_stock",
    ascending=True
)

plt.figure(figsize=(12, 7))
plt.barh(
    stock_df["product_name"],
    stock_df["current_stock"]
)
plt.title("Current Stock Level by Product")
plt.xlabel("Units in Stock")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(
    CHART_DIR / "stock_level_by_product.png",
    dpi=300
)
plt.close()

# Chart 2: Inventory Value by Category
category_value = (
    df.groupby("category")["inventory_value"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
plt.bar(
    category_value.index,
    category_value.values
)
plt.title("Inventory Value by Category")
plt.xlabel("Category")
plt.ylabel("Inventory Value (IDR)")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(
    CHART_DIR / "inventory_value_by_category.png",
    dpi=300
)
plt.close()

# Chart 3: Top 10 Products by Stock Out
top_products = df.nlargest(
    10,
    "total_stock_out"
).sort_values("total_stock_out")

plt.figure(figsize=(12, 7))
plt.barh(
    top_products["product_name"],
    top_products["total_stock_out"]
)
plt.title("Top 10 Products by Stock Out")
plt.xlabel("Total Quantity Out")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(
    CHART_DIR / "top_10_stock_out.png",
    dpi=300
)
plt.close()

# Chart 4: Stock Status Distribution
status_counts = df["stock_status"].value_counts()

plt.figure(figsize=(7, 7))
plt.pie(
    status_counts.values,
    labels=status_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Stock Status Distribution")
plt.tight_layout()
plt.savefig(
    CHART_DIR / "stock_status_distribution.png",
    dpi=300
)
plt.close()

print("=" * 45)
print("DATA VISUALIZATION COMPLETED")
print("=" * 45)

print(f"Total charts generated: 4")
print(f"Chart directory: {CHART_DIR}")

for chart in sorted(CHART_DIR.glob("*.png")):
    print(f"Created: {chart.name}")
