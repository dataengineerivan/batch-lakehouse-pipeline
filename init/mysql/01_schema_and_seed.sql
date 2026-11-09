-- Source system: a small online store
USE shop;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    first_name  VARCHAR(50),
    last_name   VARCHAR(50),
    email       VARCHAR(100),
    state       CHAR(2),
    created_at  DATETIME NOT NULL,
    updated_at  DATETIME NOT NULL
);

CREATE TABLE orders (
    order_id    INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date  DATETIME NOT NULL,
    status      VARCHAR(20) NOT NULL,
    amount      DECIMAL(10,2) NOT NULL,
    updated_at  DATETIME NOT NULL,
    INDEX idx_orders_updated (updated_at)
);

SET SESSION cte_max_recursion_depth = 10000;

-- 500 customers created over the last year
INSERT INTO customers
WITH RECURSIVE n AS (SELECT 1 AS i UNION ALL SELECT i + 1 FROM n WHERE i < 500)
SELECT
    i,
    ELT(1 + (i % 10), 'James','Maria','Robert','Linda','Michael','Ana','David','Keisha','Carlos','Emily'),
    ELT(1 + (i % 8), 'Smith','Johnson','Williams','Brown','Jones','Garcia','Davis','Jackson'),
    -- a few emails come in messy on purpose so the silver layer has cleanup to do
    CASE WHEN i % 25 = 0 THEN CONCAT('  Customer', i, '@Example.COM ') ELSE CONCAT('customer', i, '@example.com') END,
    ELT(1 + (i % 6), 'FL','TX','GA','NY','CA','NC'),
    NOW() - INTERVAL (365 - (i % 365)) DAY,
    NOW() - INTERVAL (365 - (i % 365)) DAY
FROM n;

-- 5,000 orders over the last 90 days
INSERT INTO orders (customer_id, order_date, status, amount, updated_at)
WITH RECURSIVE n AS (SELECT 1 AS i UNION ALL SELECT i + 1 FROM n WHERE i < 5000)
SELECT
    1 + FLOOR(RAND(i) * 500),
    NOW() - INTERVAL FLOOR(RAND(i * 7) * 90) DAY - INTERVAL FLOOR(RAND(i * 3) * 1440) MINUTE,
    ELT(1 + FLOOR(RAND(i * 11) * 10), 'completed','completed','completed','completed','completed',
        'completed','shipped','shipped','pending','cancelled'),
    ROUND(10 + RAND(i * 13) * 240, 2),
    NOW()
FROM n;

-- an order's last update starts at the time it was placed
UPDATE orders SET updated_at = order_date;
