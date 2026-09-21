"""Independent aggregate and stock-flow checks. Run after simulate.py."""
import csv,json,sqlite3,math
from pathlib import Path
from simulate import run,metrics
p=Path(__file__).parent;x=json.loads((p/'data/analysis.json').read_text())
db=sqlite3.connect(':memory:')
with (p/'data/daily_ledger.csv').open() as f:
    reader=csv.DictReader(f);cols=reader.fieldnames
    db.execute('CREATE TABLE ledger ('+','.join(c+(' TEXT' if c in ('policy','scenario','sku') else ' REAL') for c in cols)+')')
    db.executemany('INSERT INTO ledger VALUES ('+','.join('?' for _ in cols)+')',([r[k] for k in cols] for r in reader))
assert db.execute('SELECT count(*) FROM ledger').fetchone()[0]==240*4*3
assert db.execute('SELECT count(*) FROM (SELECT policy,day,sku,count(*) n FROM ledger GROUP BY policy,day,sku HAVING n<>1)').fetchone()[0]==0
assert db.execute('SELECT count(*) FROM ledger WHERE opening_kg+received_kg<>sold_kg+expired_kg+closing_kg OR sold_kg+unfilled_kg<>requested_kg').fetchone()[0]==0
assert db.execute('SELECT count(*) FROM (SELECT day,sku,count(DISTINCT requested_kg) n FROM ledger GROUP BY day,sku HAVING n<>1)').fetchone()[0]==0
for expected in x['main']:
    row=db.execute('''SELECT sum(requested_kg),sum(sold_kg),sum(expired_kg),sum(received_kg)+sum(CASE WHEN day=60 THEN opening_kg ELSE 0 END),sum(gross_margin_kes-waste_cost_kes-holding_cost_kes),sum(closing_kg)/180.0 FROM ledger WHERE policy=? AND CAST(day AS INTEGER)>=60''',(expected['policy'],)).fetchone()
    for value,key in zip(row,['requested_kg','sold_kg','expired_kg','supply_kg','modelled_contribution_kes','average_closing_kg']):assert math.isclose(value,expected[key],abs_tol=.001),key
# Removing the new information reproduces the baseline exactly, not a different process.
baseline,_,_=run(0,'sales_only');zero_capture,_,_=run(0,'all_logged',capture_override=0)
assert metrics(baseline)==metrics(zero_capture)
# Each sensitivity result retains the same demand denominator across policies.
with (p/'data/sensitivity.csv').open() as f: rows=list(csv.DictReader(f))
for scenario in x['scenarios']:
 for seed in x['seeds']:
    group=[r for r in rows if r['scenario']==scenario and int(r['seed'])==seed]
    assert len(group)==3 and len({r['requested_kg'] for r in group})==1
print('PASS: 2,880 ledger rows; unique grain; daily mass balance; identical policy demand; SQL aggregate reconciliation; zero-capture equivalence; all 100 paired scenario/seed comparisons.')
