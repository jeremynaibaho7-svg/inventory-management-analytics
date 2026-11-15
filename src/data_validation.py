
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "inventory.db"

conn = sqlite3.connect(DB_PATH)

checks = []

def add_check(name, passed, detail):
    checks.append({
        "validation_check": name,
        "status": "PASS" if passed else "FAIL",
        "details": detail
    })

# 1. Duplicate product IDs
duplicate_products = pd.read_sql_query("""
    SELECT product_id, COUNT(*) AS total
    FROM products
    GROUP BY product_id
    HAVING COUNT(*) > 1
""", conn)

add_check(
    "Duplicate Product IDs",
    duplicate_products.empty,
    f"{len(duplicate_products)} duplicate records"
)

# 2. Missing product data
missing_products = pd.read_sql_query("""
    SELECT COUNT(*) AS total
    FROM products
    WHERE product_id IS NULL
       OR product_name IS NULL
       OR category IS NULL
       OR supplier_id IS NULL
""", conn)["total"][0]

add_check(
    "Missing Product Data",
    missing_products == 0,
    f"{missing_products} incomplete records"
)

# 3. Invalid prices
invalid_prices = pd.read_sql_query("""
    SELECT COUNT(*) AS total
    FROM products
    WHERE cost_price <= 0
       OR selling_price <= 0
""", conn)["total"][0]

add_check(
    "Invalid Product Prices",
    invalid_prices == 0,
    f"{invalid_prices} invalid price records"
)

# 4. Invalid transaction quantities
invalid_quantities = pd.read_sql_query("""
    SELECT COUNT(*) AS total
    FROM stock_transactions
    WHERE quantity <= 0
""", conn)["total"][0]

add_check(
    "Invalid Transaction Quantity",
    invalid_quantities == 0,
    f"{invalid_quantities} invalid transactions"
)

# 5. Unknown product references
orphan_transactions = pd.read_sql_query("""
    SELECT COUNT(*) AS total
    FROM stock_transactions t
    LEFT JOIN products p
        ON t.product_id = p.product_id
    WHERE p.product_id IS NULL
""", conn)["total"][0]

add_check(
    "Transaction Product References",
    orphan_transactions == 0,
    f"{orphan_transactions} invalid references"
)

# 6. Foreign key integrity
foreign_key_errors = pd.read_sql_query(
    "PRAGMA foreign_key_check",
    conn
)

add_check(
    "Database Foreign Key Integrity",
    foreign_key_errors.empty,
    f"{len(foreign_key_errors)} foreign key violations"
)

# Display report
report = pd.DataFrame(checks)

print("=" * 55)
print("DATA QUALITY & VALIDATION REPORT")
print("=" * 55)

print(report.to_string(index=False))

passed = (report["status"] == "PASS").sum()
failed = (report["status"] == "FAIL").sum()

print("\nVALIDATION SUMMARY")
print(f"Total Checks : {len(report)}")
print(f"Passed       : {passed}")
print(f"Failed       : {failed}")

# Save validation report
output_path = BASE_DIR / "output" / "data_validation_report.csv"
report.to_csv(output_path, index=False)

conn.close()

print("\nValidation report saved:", output_path)
print("DATA VALIDATION COMPLETED")
