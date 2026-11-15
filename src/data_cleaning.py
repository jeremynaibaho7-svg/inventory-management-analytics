
import pandas as pd
from pathlib import Path

# Define project directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Load datasets
products = pd.read_csv(DATA_DIR / "products.csv")
suppliers = pd.read_csv(DATA_DIR / "suppliers.csv")

# Data inspection
print("===== PRODUCT DATA =====")
print(products.head())

print("\n===== DATA INFORMATION =====")
print(products.info())

print("\n===== MISSING VALUES =====")
print(products.isnull().sum())

# Merge products with suppliers
inventory = pd.merge(
    products,
    suppliers,
    on="supplier_id",
    how="left"
)

# Data validation
inventory = inventory.drop_duplicates(
    subset=["product_id"]
)

inventory["cost_price"] = pd.to_numeric(
    inventory["cost_price"],
    errors="coerce"
)

inventory["selling_price"] = pd.to_numeric(
    inventory["selling_price"],
    errors="coerce"
)

# Calculate product profit
inventory["profit_per_unit"] = (
    inventory["selling_price"] -
    inventory["cost_price"]
)

# Export cleaned dataset
output_path = DATA_DIR / "cleaned_inventory.csv"
inventory.to_csv(output_path, index=False)

print("\n===== DATA CLEANING COMPLETED =====")
print(f"Total products: {len(inventory)}")
print(f"Output saved: {output_path}")
