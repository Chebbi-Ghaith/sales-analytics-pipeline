-- Dimension Tables
CREATE TABLE dim_customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255) UNIQUE NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    territory VARCHAR(50),
    region VARCHAR(100)
);

CREATE TABLE dim_products (
    product_id SERIAL PRIMARY KEY,
    product_code VARCHAR(50) UNIQUE NOT NULL,
    product_line VARCHAR(100),
    manufacturer_price DECIMAL(10, 2)
);

CREATE TABLE dim_dates (
    date_id SERIAL PRIMARY KEY,
    order_date DATE UNIQUE NOT NULL,
    day INT,
    day_of_week VARCHAR(20),
    week INT,
    month INT,
    month_name VARCHAR(20),
    quarter INT,
    year INT,
    year_month VARCHAR(10)
);

-- Fact Table
CREATE TABLE fact_transactions (
    transaction_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    quantity INT,
    unit_price DECIMAL(10, 2),
    total_sales DECIMAL(10, 2),
    revenue_per_item DECIMAL(10, 2),
    discount_pct DECIMAL(5, 2),
    order_status VARCHAR(50),
    deal_size VARCHAR(20),
    is_discounted BOOLEAN,
    is_sales_outlier BOOLEAN,
    is_negative_qty BOOLEAN,
    is_high_value_order BOOLEAN,
    is_bulk_order BOOLEAN
);

-- Indexes for performance
CREATE INDEX idx_transactions_order ON fact_transactions(order_id);