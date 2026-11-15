
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "inventory.db"
OUTPUT_DIR = BASE_DIR / "output"

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

# Business metrics
total_inventory_value = df["inventory_value"].sum()
total_stock = df["current_stock"].sum()

low_stock = df[
    df["stock_status"] == "LOW STOCK"
]

top_stock_out = df.loc[
    df["total_stock_out"].idxmax()
]

top_inventory_category = (
    df.groupby("category")["inventory_value"]
    .sum()
    .idxmax()
)

category_values = (
    df.groupby("category")["inventory_value"]
    .sum()
    .sort_values(ascending=False)
)

# Generate insights
insights = []

insights.append(
    "INVENTORY MANAGEMENT - BUSINESS INSIGHTS"
)
insights.append("=" * 55)

insights.append(
    f"Total inventory units: {total_stock}"
)

insights.append(
    f"Total inventory value: Rp {total_inventory_value:,.0f}"
)

insights.append("")
insights.append("1. STOCK MONITORING")

if low_stock.empty:
    insights.append(
        "No products are currently at or below minimum stock."
    )
else:
    for _, row in low_stock.iterrows():
        insights.append(
            f"{row['product_name']}: "
            f"{row['current_stock']} units "
            f"(minimum: {row['min_stock']}). "
            "Review replenishment needs."
        )

insights.append("")
insights.append("2. PRODUCT MOVEMENT")

insights.append(
    f"{top_stock_out['product_name']} has the highest "
    f"stock-out quantity: "
    f"{top_stock_out['total_stock_out']} units."
)

insights.append(
    "Review its demand pattern and replenishment frequency."
)

insights.append("")
insights.append("3. INVENTORY VALUE")

insights.append(
    f"{top_inventory_category} has the largest "
    "inventory value among all categories."
)

for category, value in category_values.items():
    insights.append(
        f"- {category}: Rp {value:,.0f}"
    )

insights.append("")
insights.append("4. BUSINESS RECOMMENDATIONS")

insights.append(
    "- Monitor products at or below minimum stock."
)

insights.append(
    "- Review replenishment frequency for high stock-out products."
)

insights.append(
    "- Monitor capital allocation in high-value categories."
)

insights.append(
    "- Review inventory movement regularly to reduce stock imbalance."
)

# Print report
report_text = "\n".join(insights)

print(report_text)

# Export report
output_file = OUTPUT_DIR / "business_insights.txt"
output_file.write_text(report_text, encoding="utf-8")

print("\nBusiness insights saved:", output_file)
