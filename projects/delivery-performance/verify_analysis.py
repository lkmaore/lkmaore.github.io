import sqlite3,csv,json,math
from pathlib import Path
import argparse
ap=argparse.ArgumentParser(description='Independently verify published aggregates with SQL.');ap.add_argument('source');args=ap.parse_args()
s=Path(args.source);x=json.loads((Path(__file__).parent/'data/analysis.json').read_text());db=sqlite3.connect(':memory:')
for table,file in [('orders','olist_orders_dataset.csv'),('reviews','olist_order_reviews_dataset.csv'),('customers','olist_customers_dataset.csv')]:
 with (s/file).open() as f:
  r=csv.DictReader(f);columns=r.fieldnames;db.execute(f'CREATE TABLE {table} ({",".join(columns)})');db.executemany(f'INSERT INTO {table} VALUES ({",".join("?" for _ in columns)})',([row[k] for k in columns] for row in r))
db.execute('''CREATE VIEW cohort AS SELECT *, date(order_delivered_customer_date)>date(order_estimated_delivery_date) AS late FROM orders WHERE order_status='delivered' AND order_purchase_timestamp<>'' AND order_delivered_customer_date<>'' AND order_estimated_delivery_date<>'' AND julianday(order_delivered_customer_date)>=julianday(order_purchase_timestamp) AND date(order_estimated_delivery_date)>=date(order_purchase_timestamp)''')
rows=db.execute('''WITH ranked AS (SELECT *,row_number() OVER (PARTITION BY order_id ORDER BY review_answer_timestamp DESC,review_creation_date DESC,review_id DESC,review_score DESC) AS rank FROM reviews) SELECT c.late,count(*),sum(CAST(r.review_score AS INTEGER)<=2) FROM cohort c JOIN ranked r USING(order_id) WHERE r.rank=1 GROUP BY c.late''').fetchall()
for row,expected in zip(rows,x['delivery_groups']):assert row[1:]==(expected['reviewed_orders'],expected['low_reviews']),row
rows=db.execute('''SELECT late,count(*),avg(julianday(order_approved_at)-julianday(order_purchase_timestamp)),avg(julianday(order_delivered_carrier_date)-julianday(order_approved_at)),avg(julianday(order_delivered_customer_date)-julianday(order_delivered_carrier_date)) FROM cohort WHERE order_approved_at<>'' AND order_delivered_carrier_date<>'' AND order_purchase_timestamp<=order_approved_at AND order_approved_at<=order_delivered_carrier_date AND order_delivered_carrier_date<=order_delivered_customer_date GROUP BY late''').fetchall()
for row,expected in zip(rows,x['stages']):
 assert row[1]==expected['orders']
 for a,b in zip(row[2:],(expected[k] for k in ['approval_days','handover_days','transit_days'])):assert math.isclose(a,b,abs_tol=1e-8)
rows=db.execute('SELECT customer_state,count(*),sum(late) FROM cohort JOIN customers USING(customer_id) GROUP BY customer_state').fetchall()
for row,expected in zip(rows,x['states']):assert row==(expected['group'],expected['orders'],expected['late_orders'])
print('Independent SQL confirms review numerators/denominators, all stage means and counts, and all destination totals.')
