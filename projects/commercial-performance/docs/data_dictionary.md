# Data Dictionary

## fact_sales
Grain: one product line within a customer order.

- line_id: unique sales line
- order_id: customer order
- order_date: transaction date
- customer_id: customer foreign key
- product_id: product foreign key
- salesperson_id: salesperson foreign key
- quantity: units sold
- unit_price: list price before discount
- discount_pct: line discount
- gross_sales: quantity x unit price
- net_sales: gross sales after discount
- cogs: cost of goods sold
- gross_profit: net sales minus COGS

## Dimensions
`dim_product`: SKU, product, category, brand and base economics.

`dim_customer`: customer, channel, region, city and account segment.

`dim_salesperson`: representative and assigned region.

`dim_date`: calendar attributes for time intelligence.

`budget_monthly`: monthly revenue target at YearMonth x Region x Category grain.

## Limitation
Every company, customer, product, transaction and result in this project is synthetic.
