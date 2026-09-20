"""Reproduce order-level delivery analysis from the official Olist CSV directory.
Usage: python3 analyze.py /path/to/official/csv --output data/analysis.json
Python standard library only. Raw rows are never written to the public output.
"""
import argparse, csv, json, statistics, hashlib, sqlite3
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

def analyze(source):
    source=Path(source)
    def read(name):
        with (source/name).open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
    names={'orders':'olist_orders_dataset.csv','customers':'olist_customers_dataset.csv','items':'olist_order_items_dataset.csv','reviews':'olist_order_reviews_dataset.csv','products':'olist_products_dataset.csv','sellers':'olist_sellers_dataset.csv','translation':'product_category_name_translation.csv'}
    tables={k:read(v) for k,v in names.items()}
    orders=tables['orders']; customers={r['customer_id']:r for r in tables['customers']};products={r['product_id']:r for r in tables['products']}; sellers={r['seller_id']:r for r in tables['sellers']};translations={r['product_category_name']:r['product_category_name_english'] for r in tables['translation']}
    ids={r['order_id'] for r in orders}
    quality={'rows':{k:len(v) for k,v in tables.items()},'duplicate_order_ids':len(orders)-len(ids),'duplicate_customer_ids':len(tables['customers'])-len(customers),'duplicate_product_ids':len(tables['products'])-len(products),'duplicate_seller_ids':len(tables['sellers'])-len(sellers),'orphan_order_customers':sum(r['customer_id'] not in customers for r in orders),'orphan_item_orders':sum(r['order_id'] not in ids for r in tables['items']),'orphan_item_products':sum(r['product_id'] not in products for r in tables['items']),'orphan_item_sellers':sum(r['seller_id'] not in sellers for r in tables['items']),'orphan_review_orders':sum(r['order_id'] not in ids for r in tables['reviews'])}
    assert not any(quality[k] for k in quality if k.startswith(('duplicate','orphan'))),quality
    items=defaultdict(list);reviews=defaultdict(list)
    for r in tables['items']: items[r['order_id']].append(r)
    for r in tables['reviews']: reviews[r['order_id']].append(r)
    quality['orders_multiple_reviews']=sum(len(v)>1 for v in reviews.values())
    quality['orders_multiple_sellers']=sum(len({r['seller_id'] for r in v})>1 for v in items.values())
    dt=lambda s: datetime.fromisoformat(s) if s else None
    days=lambda a,b:(b-a).total_seconds()/86400
    cohort=[];exclusions=Counter();stage_exclusions=Counter()
    for o in orders:
        if o['order_status']!='delivered': exclusions['not_delivered_status']+=1;continue
        p,a,c,d,e=[dt(o[k]) for k in ('order_purchase_timestamp','order_approved_at','order_delivered_carrier_date','order_delivered_customer_date','order_estimated_delivery_date')]
        if not all((p,d,e)):exclusions['missing_core_dates']+=1;continue
        if d<p or e.date()<p.date():exclusions['invalid_core_chronology']+=1;continue
        item=items[o['order_id']]; seller_ids={r['seller_id'] for r in item}
        cats={translations.get(products[r['product_id']]['product_category_name'],'unknown') for r in item}
        rev=reviews.get(o['order_id'],[])
        # Latest answered review per order; deterministic ties, no item join duplication.
        review=max(rev,key=lambda r:(r['review_answer_timestamp'],r['review_creation_date'],r['review_id'],r['review_score'])) if rev else None
        row={'order_id':o['order_id'],'month':p.strftime('%Y-%m'),'state':customers[o['customer_id']]['customer_state'],'late':int(d.date()>e.date()),'lateness_days':max(0,(d.date()-e.date()).days),'total_days':days(p,d),'promise_days':days(p,e),'review':int(review['review_score']) if review else None,'single_review':len(rev)==1,'category':next(iter(cats)) if len(cats)==1 else 'multiple_categories' if cats else 'unknown','seller_count':len(seller_ids),'route':'unknown'}
        if len(seller_ids)==1:
            origin=sellers[next(iter(seller_ids))]['seller_state'];row['route']='same_state' if origin==row['state'] else 'cross_state'
        else:row['route']='multiple_sellers' if seller_ids else 'unknown'
        if not a or not c:stage_exclusions['missing_stage_dates']+=1
        elif not p<=a<=c<=d:stage_exclusions['out_of_sequence_stage_dates']+=1
        else:row.update(approval_days=days(p,a),handover_days=days(a,c),transit_days=days(c,d))
        cohort.append(row)
    def summary(rows):
        n=len(rows);late=sum(r['late'] for r in rows);rr=[r for r in rows if r['review'] is not None]
        return {'orders':n,'late_orders':late,'late_rate':100*late/n if n else None,'median_delivery_days':statistics.median(r['total_days'] for r in rows) if n else None,'reviewed_orders':len(rr),'low_reviews':sum(r['review']<=2 for r in rr),'low_review_rate':100*sum(r['review']<=2 for r in rr)/len(rr) if rr else None}
    def group(field):
        groups=defaultdict(list)
        for r in cohort:groups[r[field]].append(r)
        return [{'group':k,**summary(v)} for k,v in sorted(groups.items())]
    stage=[r for r in cohort if 'transit_days' in r]
    stage_groups=[]
    for late in (0,1):
        rs=[r for r in stage if r['late']==late]
        stage_groups.append({'group':'late' if late else 'on_time','orders':len(rs),**{k:statistics.mean(r[k] for r in rs) for k in ('approval_days','handover_days','transit_days','total_days','promise_days')}})
    # Independent SQL calculation of the primary count/rate directly from source rows.
    con=sqlite3.connect(':memory:');con.execute('CREATE TABLE orders (order_id, status, purchase, delivered, estimated)')
    con.executemany('INSERT INTO orders VALUES (?,?,?,?,?)',[(r['order_id'],r['order_status'],r['order_purchase_timestamp'],r['order_delivered_customer_date'],r['order_estimated_delivery_date']) for r in orders])
    sql=(Path(__file__).parent/'verify.sql').read_text();sql_result=con.execute(sql).fetchone();main=summary(cohort)
    assert sql_result==(main['orders'],main['late_orders']), (sql_result,main)
    assert sum(r['orders'] for r in group('state'))==len(cohort)
    quality.update(exclusions=dict(exclusions),stage_exclusions=dict(stage_exclusions),eligible_stage_orders=len(stage),eligible_orders_without_reviews=sum(r['review'] is None for r in cohort),eligible_orders_multiple_reviews=sum(not r['single_review'] and r['review'] is not None for r in cohort),eligible_orders_missing_items=sum(r['seller_count']==0 for r in cohort),independent_sql_primary_counts=list(sql_result))
    return {'source':{'title':'Brazilian E-Commerce Public Dataset by Olist','url':'https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce','license':'CC BY-NC-SA 4.0','classification':'real anonymised historical commercial data','files_sha256':{v:hashlib.sha256((source/v).read_bytes()).hexdigest() for v in names.values()}},'scope':{'purchase_min':min(r['order_purchase_timestamp'] for r in orders),'purchase_max':max(r['order_purchase_timestamp'] for r in orders),'cohort_purchase_min':min(r['month'] for r in cohort),'cohort_purchase_max':max(r['month'] for r in cohort),'late_definition':'Delivered calendar date later than estimated calendar date; same-day arrivals count on time. Naive source timestamps; no timezone conversion.'},'quality':quality,'statuses':dict(Counter(r['order_status'] for r in orders)),'overall':main,'states':group('state'),'months':group('month'),'categories':group('category'),'routes':group('route'),'delivery_groups':[{'group':'late' if late else 'on_time',**summary([r for r in cohort if r['late']==late])} for late in (0,1)],'single_review_sensitivity':[{'group':'late' if late else 'on_time',**summary([r for r in cohort if r['late']==late and r['single_review']])} for late in (0,1)],'stages':stage_groups}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('--output',default='data/analysis.json');args=ap.parse_args();result=analyze(args.source);out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('overall','quality','delivery_groups','stages')},indent=2))
