-- 1. Executive YTD KPIs
SELECT
    substr(order_date,1,4) AS year,
    ROUND(SUM(net_sales),2) AS revenue,
    ROUND(SUM(gross_profit),2) AS gross_profit,
    ROUND(100.0*SUM(gross_profit)/SUM(net_sales),2) AS gross_margin_pct,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(100.0*AVG(discount_pct),2) AS avg_discount_pct
FROM fact_sales
WHERE substr(order_date,6,2)<='08'
GROUP BY year
ORDER BY year;

-- 2. 2026 Actual vs Budget
WITH actual AS (
    SELECT substr(f.order_date,1,7) AS year_month,c.region,p.category,SUM(f.net_sales) AS revenue
    FROM fact_sales f
    JOIN dim_customer c ON f.customer_id=c.customer_id
    JOIN dim_product p ON f.product_id=p.product_id
    WHERE substr(f.order_date,1,4)='2026'
    GROUP BY 1,2,3
)
SELECT
    ROUND(SUM(a.revenue),2) AS actual_revenue,
    ROUND(SUM(b.revenue_budget),2) AS budget_revenue,
    ROUND(SUM(a.revenue)-SUM(b.revenue_budget),2) AS variance_kes,
    ROUND(100.0*(SUM(a.revenue)/SUM(b.revenue_budget)-1),2) AS variance_pct
FROM actual a
JOIN budget_monthly b
  ON a.year_month=b.year_month AND a.region=b.region AND a.category=b.category;

-- 3. Category Performance
SELECT
    p.category,
    ROUND(SUM(f.net_sales),2) AS revenue,
    ROUND(SUM(f.gross_profit),2) AS gross_profit,
    ROUND(100.0*SUM(f.gross_profit)/SUM(f.net_sales),2) AS gross_margin_pct,
    SUM(f.quantity) AS units
FROM fact_sales f
JOIN dim_product p ON f.product_id=p.product_id
WHERE substr(f.order_date,1,4)='2026'
GROUP BY p.category
ORDER BY revenue DESC;

-- 4. Region Performance
SELECT
    c.region,
    ROUND(SUM(f.net_sales),2) AS revenue,
    ROUND(SUM(f.gross_profit),2) AS gross_profit,
    ROUND(100.0*SUM(f.gross_profit)/SUM(f.net_sales),2) AS gross_margin_pct,
    ROUND(100.0*AVG(f.discount_pct),2) AS avg_discount_pct
FROM fact_sales f
JOIN dim_customer c ON f.customer_id=c.customer_id
WHERE substr(f.order_date,1,4)='2026'
GROUP BY c.region
ORDER BY revenue DESC;

-- 5. Channel Economics
SELECT
    c.channel,
    ROUND(SUM(f.net_sales),2) AS revenue,
    ROUND(SUM(f.gross_profit),2) AS gross_profit,
    ROUND(100.0*SUM(f.gross_profit)/SUM(f.net_sales),2) AS gross_margin_pct,
    ROUND(100.0*AVG(f.discount_pct),2) AS avg_discount_pct
FROM fact_sales f
JOIN dim_customer c ON f.customer_id=c.customer_id
WHERE substr(f.order_date,1,4)='2026'
GROUP BY c.channel
ORDER BY revenue DESC;

-- 6. Top Customers
SELECT
    c.customer_name,c.region,c.channel,ROUND(SUM(f.net_sales),2) AS revenue
FROM fact_sales f
JOIN dim_customer c ON f.customer_id=c.customer_id
WHERE substr(f.order_date,1,4)='2026'
GROUP BY c.customer_id,c.customer_name,c.region,c.channel
ORDER BY revenue DESC
LIMIT 10;
