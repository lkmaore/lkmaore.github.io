-- Independent primary cohort reconciliation from raw orders, one row per order.
SELECT COUNT(*) AS eligible_orders,
       SUM(CASE WHEN date(delivered) > date(estimated) THEN 1 ELSE 0 END) AS late_orders
FROM orders
WHERE status = 'delivered'
  AND purchase <> '' AND delivered <> '' AND estimated <> ''
  AND julianday(delivered) >= julianday(purchase)
  AND date(estimated) >= date(purchase);
