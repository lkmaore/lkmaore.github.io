"""Reproduce the published synthetic case study. Python 3 standard library only."""
import csv
import json
import math
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
con = sqlite3.connect(':memory:')
con.row_factory = sqlite3.Row
for path in sorted((ROOT / 'data').glob('*.csv')):
    with path.open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        con.execute('CREATE TABLE "' + path.stem + '" (' + ','.join('"'+x+'"' for x in fields) + ')')
        con.executemany('INSERT INTO "'+path.stem+'" VALUES ('+','.join('?' for _ in fields)+')', ([row[x] for x in fields] for row in reader))

def scalar(sql): return con.execute(sql).fetchone()[0]
def assert_close(actual, expected):
    assert math.isclose(actual, expected, abs_tol=0.015), (actual, expected)

for table, key in [('dim_customer','customer_id'),('dim_product','product_id'),('dim_date','date'),('dim_salesperson','salesperson_id'),('fact_sales','line_id')]:
    assert scalar(f'SELECT COUNT(*) - COUNT(DISTINCT "{key}") FROM "{table}"') == 0
for table, key in [('dim_customer','customer_id'),('dim_product','product_id'),('dim_salesperson','salesperson_id')]:
    assert scalar(f'SELECT COUNT(*) FROM fact_sales f LEFT JOIN {table} d ON f.{key}=d.{key} WHERE d.{key} IS NULL') == 0
assert scalar('SELECT COUNT(*) FROM fact_sales f LEFT JOIN dim_date d ON f.order_date=d.date WHERE d.date IS NULL') == 0
assert scalar('SELECT COUNT(*) FROM (SELECT year_month,region,category,COUNT(*) n FROM budget_monthly GROUP BY 1,2,3 HAVING n>1)') == 0
assert scalar('SELECT COUNT(*) FROM fact_sales') == 19190
assert scalar('SELECT COUNT(DISTINCT order_id) FROM fact_sales') == 9820
periods = {r['year']:dict(r) for r in con.execute("SELECT substr(order_date,1,4) year,SUM(net_sales) revenue,SUM(gross_profit) gp FROM fact_sales WHERE substr(order_date,6,2)<='08' GROUP BY 1")}
r26,r25=periods['2026'],periods['2025']
budget=scalar("SELECT SUM(revenue_budget) FROM budget_monthly WHERE year_month BETWEEN '2026-01' AND '2026-08'")
assert_close(r26['revenue'],24023981.09)
assert_close(r26['gp'],4523770.17)
assert_close(r25['revenue'],19703777.51)
assert_close(r25['gp'],4184950.56)
assert_close(budget,26127093.03)
hh=scalar("SELECT SUM(f.net_sales) FROM fact_sales f JOIN dim_product p ON p.product_id=f.product_id WHERE f.order_date BETWEEN '2026-01-01' AND '2026-08-31' AND p.category='Household'")
hh_budget=scalar("SELECT SUM(revenue_budget) FROM budget_monthly WHERE year_month BETWEEN '2026-01' AND '2026-08' AND category='Household'")
reviewed=json.loads((ROOT/'data/analysis.json').read_text())
for group,table,key,label in [('category','dim_product','product_id','category'),('region','dim_customer','customer_id','region'),('channel','dim_customer','customer_id','channel')]:
    values={(r['segment'],r['year']):r for r in reviewed[group]}
    for row in con.execute(f"SELECT d.{label} segment, substr(f.order_date,1,4) year, SUM(f.net_sales) revenue,SUM(f.gross_profit) gp FROM fact_sales f JOIN {table} d ON f.{key}=d.{key} WHERE substr(f.order_date,6,2)<='08' AND substr(f.order_date,1,4) IN ('2025','2026') GROUP BY 1,2"):
        expected=values[(row['segment'],row['year'])]
        assert_close(row['revenue'],expected['revenue']);assert_close(row['gp'],expected['gp'])
    assert_close(sum(r['revenue'] for r in reviewed[group] if r['year']=='2026'),r26['revenue'])
for row in reviewed['monthly']:
    assert_close(scalar(f"SELECT SUM(net_sales) FROM fact_sales WHERE substr(order_date,1,7)='{row['month']}'"),row['revenue'])
for row in reviewed['budget']:
    assert_close(scalar(f"SELECT SUM(revenue_budget) FROM budget_monthly WHERE year_month='{row['month']}'"),row['budget'])
print('All source, key, relationship, grain, headline and segment checks passed.')
print(json.dumps({'period':'Jan–Aug 2026 vs Jan–Aug 2025','currency':'KES','revenue':round(r26['revenue'],2),'gross_profit':round(r26['gp'],2),'revenue_growth_pct':round((r26['revenue']/r25['revenue']-1)*100,4),'gross_profit_growth_pct':round((r26['gp']/r25['gp']-1)*100,4),'gross_margin_pct':round(r26['gp']/r26['revenue']*100,4),'budget':round(budget,2),'budget_variance_pct':round((r26['revenue']/budget-1)*100,4),'household_share_net_shortfall_pct':round((hh_budget-hh)/(budget-r26['revenue'])*100,4)},indent=2))
