-- Commercial Performance Intelligence
-- All data is synthetic.

CREATE TABLE dim_product (
    product_id TEXT PRIMARY KEY, sku TEXT, product_name TEXT, category TEXT, brand TEXT,
    base_price NUMERIC(12,2), base_unit_cost NUMERIC(12,2)
);
CREATE TABLE dim_customer (
    customer_id TEXT PRIMARY KEY, customer_name TEXT, channel TEXT, region TEXT, city TEXT, segment TEXT
);
CREATE TABLE dim_salesperson (
    salesperson_id TEXT PRIMARY KEY, salesperson_name TEXT, region TEXT
);
CREATE TABLE dim_date (
    date DATE PRIMARY KEY, year INTEGER, quarter TEXT, month_number INTEGER,
    month_name TEXT, year_month TEXT, year_month_sort INTEGER
);
CREATE TABLE fact_sales (
    line_id TEXT PRIMARY KEY, order_id TEXT, order_date DATE,
    customer_id TEXT REFERENCES dim_customer(customer_id),
    product_id TEXT REFERENCES dim_product(product_id),
    salesperson_id TEXT REFERENCES dim_salesperson(salesperson_id),
    quantity INTEGER, unit_price NUMERIC(12,2), discount_pct NUMERIC(8,4),
    gross_sales NUMERIC(14,2), net_sales NUMERIC(14,2), cogs NUMERIC(14,2), gross_profit NUMERIC(14,2)
);
CREATE TABLE budget_monthly (
    year_month TEXT, region TEXT, category TEXT, revenue_budget NUMERIC(14,2)
);
