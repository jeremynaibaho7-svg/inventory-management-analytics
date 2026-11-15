# Inventory Management & Analytics

A Python and SQL-based inventory analytics project designed to monitor stock movements, evaluate inventory value, identify low-stock products, and generate actionable business insights.

## 1. Project Overview

Inventory management plays an important role in maintaining operational efficiency and controlling business costs.

This project develops a simple inventory analytics system using Python, SQL, Pandas, and SQLite. It transforms raw inventory data into structured information that supports inventory monitoring and operational decision-making.

## 2. Business Objectives

- Monitor current inventory levels.
- Identify products requiring stock replenishment.
- Calculate total inventory valuation.
- Analyze stock-in and stock-out movements.
- Rank products based on stock-out quantity.
- Generate business insights from inventory data.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data processing and analytics |
| SQL | Database querying and analysis |
| SQLite | Relational database management |
| Pandas | Data manipulation and aggregation |
| Matplotlib | Data visualization |
| VS Code | Development environment |

## 4. Project Structure

```text
inventory-management-analytics/
│
├── data/
│   ├── products.csv
│   ├── suppliers.csv
│   ├── transactions.csv
│   └── cleaned_inventory.csv
│
├── database/
│   └── inventory.db
│
├── sql/
│   └── 02_inventory_analysis.sql
│
├── src/
│   ├── data_cleaning.py
│   ├── create_database.py
│   ├── analytics.py
│   ├── visualization.py
│   ├── data_validation.py
│   └── business_insights.py
│
├── output/
│   ├── charts/
│   ├── product_analytics.csv
│   ├── category_analysis.csv
│   ├── data_validation_report.csv
│   └── business_insights.txt
│
├── README.md
└── requirements.txt
```

## 5. Database Design

The project uses three relational tables:

- **products** — stores product information, categories, prices, and minimum stock levels.
- **suppliers** — stores supplier information.
- **stock_transactions** — records inventory movements, including stock-in (IN) and stock-out (OUT).

Primary keys and foreign key relationships are used to maintain relational integrity.

## 6. Data Processing Workflow

1. Import raw CSV datasets.
2. Clean and transform product data using Python and Pandas.
3. Create the SQLite database.
4. Load suppliers, products, and transaction records.
5. Perform SQL-based inventory analysis.
6. Process analytical results using Python.
7. Validate data quality and database integrity.
8. Generate visualizations and business insights.

## 7. SQL Analysis

The project implements four analytical queries:

**Query A — Inventory Stock Analysis**
- Calculates total stock-in.
- Calculates total stock-out.
- Determines current inventory levels.
- Joins products with supplier information.

**Query B — Stock Status Classification**
- Uses Common Table Expressions (CTEs).
- Applies CASE WHEN conditions.
- Identifies products at or below minimum stock levels.

**Query C — Inventory Valuation**
- Calculates inventory value using current stock multiplied by cost price.
- Evaluates inventory value at product level.

**Query D — Product Performance Ranking**
- Ranks products by stock-out quantity.
- Implements SQL window functions using RANK().

## 8. Python Analytics

Python and Pandas are used to:

- Retrieve data directly from SQLite.
- Calculate inventory metrics.
- Aggregate inventory performance by category.
- Identify products with the lowest stock.
- Identify products with the highest stock-out quantity.
- Export analytical results into CSV files.

## 9. Data Visualization

Four visualizations are generated:

1. Current Stock Level by Product.
2. Inventory Value by Category.
3. Top 10 Products by Stock Out.
4. Stock Status Distribution.

All charts are generated using Matplotlib.

## 10. Key Findings

Based on the sample dataset:

| Metric | Result |
|---|---:|
| Total Products | 12 |
| Total Current Stock | 403 units |
| Total Stock Out | 462 units |
| Total Inventory Value | Rp250,600,000 |
| Lowest Stock Product | Printer Epson L3210 |
| Highest Stock-Out Product | LAN Cable 10m |

### Category Inventory Value

| Category | Inventory Value |
|---|---:|
| Electronics | Rp156,200,000 |
| Accessories | Rp45,125,000 |
| Storage | Rp43,400,000 |
| Networking | Rp5,875,000 |

## 11. Business Recommendations

- Monitor products that reach or fall below minimum stock levels.
- Review replenishment frequency for products with high stock-out quantities.
- Pay attention to capital allocation in high-value inventory categories.
- Establish regular inventory monitoring to reduce stock imbalance.

## 12. How to Run the Project

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate to the project directory:

```bash
cd inventory-management-analytics
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the data processing workflow:

```bash
python src/data_cleaning.py
python src/create_database.py
python src/analytics.py
python src/visualization.py
python src/data_validation.py
python src/business_insights.py
```

**Note:** The database creation script rebuilds the SQLite database. Run it before executing the analytics scripts when setting up the project from scratch.

## 13. Project Scope and Limitations

- The project uses a sample inventory dataset containing 12 products, 4 suppliers, and 24 stock transactions.
- Stock-out quantities represent inventory movements, not verified customer sales.
- Inventory valuation is calculated using cost price and current stock.
- The project does not implement a live inventory management interface.

## 14. Skills Demonstrated

- Python programming
- SQL querying and relational database design
- Data cleaning and preprocessing
- SQLite database management
- Data aggregation and analysis
- SQL CTEs and window functions
- Data validation
- Data visualization
- Business reporting and analytical thinking

---

**Project:** Inventory Management & Analytics  
**Tools:** Python, SQL, SQLite, Pandas, Matplotlib  
**Category:** Data Analytics / Inventory Analytics