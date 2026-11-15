SELECT
    p.product_id,
    p.product_name,
    p.category,
    s.supplier_name,
    SUM(CASE
        WHEN t.transaction_type = 'IN'
        THEN t.quantity ELSE 0
    END) AS total_stock_in,
    SUM(CASE
        WHEN t.transaction_type = 'OUT'
        THEN t.quantity ELSE 0
    END) AS total_stock_out,
    SUM(CASE
        WHEN t.transaction_type = 'IN'
        THEN t.quantity
        WHEN t.transaction_type = 'OUT'
        THEN -t.quantity
        ELSE 0
    END) AS current_stock
FROM products p
LEFT JOIN suppliers s
    ON p.supplier_id = s.supplier_id
LEFT JOIN stock_transactions t
    ON p.product_id = t.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    s.supplier_name
ORDER BY current_stock ASC;


-- QUERY B: STOCK STATUS CLASSIFICATION

WITH stock_summary AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        p.min_stock,
        SUM(
            CASE
                WHEN t.transaction_type = 'IN'
                    THEN t.quantity
                WHEN t.transaction_type = 'OUT'
                    THEN -t.quantity
                ELSE 0
            END
        ) AS current_stock
    FROM products p
    LEFT JOIN stock_transactions t
        ON p.product_id = t.product_id
    GROUP BY
        p.product_id,
        p.product_name,
        p.category,
        p.min_stock
)

SELECT
    product_id,
    product_name,
    category,
    current_stock,
    min_stock,
    CASE
        WHEN current_stock <= min_stock
            THEN 'LOW STOCK'
        ELSE 'NORMAL'
    END AS stock_status
FROM stock_summary
ORDER BY current_stock ASC;


-- QUERY C: INVENTORY VALUATION ANALYSIS

WITH stock_summary AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        p.cost_price,
        SUM(
            CASE
                WHEN t.transaction_type = 'IN'
                    THEN t.quantity
                WHEN t.transaction_type = 'OUT'
                    THEN -t.quantity
                ELSE 0
            END
        ) AS current_stock
    FROM products p
    LEFT JOIN stock_transactions t
        ON p.product_id = t.product_id
    GROUP BY
        p.product_id,
        p.product_name,
        p.category,
        p.cost_price
)

SELECT
    product_id,
    product_name,
    category,
    current_stock,
    cost_price,
    current_stock * cost_price AS inventory_value
FROM stock_summary
ORDER BY inventory_value DESC;



-- QUERY D: PRODUCT PERFORMANCE RANKING

WITH product_sales AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        COALESCE(
            SUM(
                CASE
                    WHEN t.transaction_type = 'OUT'
                    THEN t.quantity
                    ELSE 0
                END
            ), 0
        ) AS total_stock_out
    FROM products p
    LEFT JOIN stock_transactions t
        ON p.product_id = t.product_id
    GROUP BY
        p.product_id,
        p.product_name,
        p.category
)

SELECT
    product_id,
    product_name,
    category,
    total_stock_out,
    RANK() OVER (
        ORDER BY total_stock_out DESC
    ) AS product_rank
FROM product_sales
ORDER BY product_rank ASC;
