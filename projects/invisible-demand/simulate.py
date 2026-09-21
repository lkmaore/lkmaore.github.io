"""Fictional perishable-distributor experiment. Standard-library Python 3.10+.
No employer records, no estimated historical impact, no food-safety guidance.
Run: python3 simulate.py. Writes reproducible CSVs and reviewed aggregate JSON.
"""
from pathlib import Path
import csv,json,random,math,statistics
PRODUCTS=[dict(sku='BEEF-A',label='Beef packs',base_kg=45,cost=430,price=590,life=6),dict(sku='CHICKEN-B',label='Chicken packs',base_kg=38,cost=290,price=410,life=5),dict(sku='SAUSAGE-C',label='Sausage packs',base_kg=20,cost=310,price=450,life=8),dict(sku='SPECIAL-D',label='Specialty packs',base_kg=8,cost=560,price=720,life=4)]
DAYS=240;WARMUP=60;SEEDS=list(range(20));MAIN_SEED=0
POLICIES={'sales_only':0.0,'half_logged':0.5,'all_logged':1.0}
SCENARIOS={'base':dict(buffer=1,life_change=0,late_prob=.15),'lean_buffer':dict(buffer=0,life_change=0,late_prob=.15),'larger_buffer':dict(buffer=2,life_change=0,late_prob=.15),'shorter_life':dict(buffer=1,life_change=-2,late_prob=.15),'less_reliable_supply':dict(buffer=1,life_change=0,late_prob=.4)}

def inputs(seed,late_prob):
    # Separate fixed random streams keep each policy's demand and supplier shocks identical.
    rng=random.Random(9100+seed);lead_rng=random.Random(1900+seed);rows=[]
    for day in range(DAYS):
        for p in PRODUCTS:
            weekday=[.85,.9,1,1,1.2,1.3,.75][day%7]
            growth=1 if day<120 else 1.25
            spike=1.8 if rng.random()<.08 else 1
            demand=max(0,round(p['base_kg']*weekday*growth*spike*rng.lognormvariate(-.5*.35**2,.35)))
            lead=3 if lead_rng.random()<late_prob else 1
            rows.append(dict(day=day,sku=p['sku'],requested_kg=demand,supplier_lead_days=lead))
    return rows

def run(seed,policy,scenario='base',capture_override=None):
    cfg=SCENARIOS[scenario];capture=POLICIES[policy] if capture_override is None else capture_override
    rows=inputs(seed,cfg['late_prob']);by_sku={p['sku']:[] for p in PRODUCTS}
    for r in rows:by_sku[r['sku']].append(r)
    ledger=[];batches_out=[]
    for p in PRODUCTS:
        life=max(2,p['life']+cfg['life_change']);initial=round(p['base_kg']*3)
        batches=[dict(qty=initial,expiry=life,batch='OPEN')];pipeline=[];history=[];opening_evaluation=None
        for r in by_sku[p['sku']]:
            d=r['day'];opening=sum(b['qty'] for b in batches)
            if d==WARMUP:opening_evaluation=opening
            expired=sum(b['qty'] for b in batches if b['expiry']<=d)
            batches=[b for b in batches if b['expiry']>d]
            arrivals=[o for o in pipeline if o['arrival']==d];received=sum(o['qty'] for o in arrivals)
            for o in arrivals:
                batches.append(dict(qty=o['qty'],expiry=d+life,batch=str(o['placed'])))
                batches_out.append(dict(seed=seed,scenario=scenario,policy=policy,sku=p['sku'],placed_day=o['placed'],arrival_day=d,expiry_day=d+life,received_kg=o['qty']))
            pipeline=[o for o in pipeline if o['arrival']>d]
            requested=r['requested_kg'];remaining=requested;sold=0
            for batch in sorted(batches,key=lambda b:b['expiry']):
                amount=min(batch['qty'],remaining);batch['qty']-=amount;sold+=amount;remaining-=amount
            batches=[b for b in batches if b['qty']>0];closing=sum(b['qty'] for b in batches)
            lost=requested-sold;recorded_lost=round(lost*capture)
            # Today's outcome becomes known before the order; future demand never enters the forecast.
            observed=sold+recorded_lost;history.append(observed)
            forecast=statistics.mean(history[-28:])
            # All policies share a fixed 2-day planning lead assumption, one review day and same buffer.
            target=math.ceil(forecast*(2+1+cfg['buffer']))
            on_order=sum(o['qty'] for o in pipeline)
            order=max(0,target-closing-on_order)
            if order:pipeline.append(dict(qty=order,placed=d,arrival=d+r['supplier_lead_days']))
            assert opening+received==sold+expired+closing
            assert sold+lost==requested and min(sold,lost,closing,order)>=0
            ledger.append(dict(seed=seed,scenario=scenario,policy=policy,day=d,sku=p['sku'],opening_kg=opening,received_kg=received,requested_kg=requested,sold_kg=sold,unfilled_kg=lost,recorded_unfilled_kg=recorded_lost,expired_kg=expired,closing_kg=closing,ordered_kg=order,forecast_kg=round(forecast,6),revenue_kes=sold*p['price'],gross_margin_kes=sold*(p['price']-p['cost']),waste_cost_kes=expired*p['cost'],holding_cost_kes=closing*.8))
    return ledger,batches_out,rows

def metrics(rows):
    rows=[r for r in rows if r['day']>=WARMUP];req=sum(r['requested_kg'] for r in rows);sold=sum(r['sold_kg'] for r in rows);expired=sum(r['expired_kg'] for r in rows)
    supply=sum(r['received_kg'] for r in rows)+sum(r['opening_kg'] for r in rows if r['day']==WARMUP)
    closing=sum(r['closing_kg'] for r in rows if r['day']==DAYS-1)
    assert supply==sold+expired+closing
    margin=sum(r['gross_margin_kes']-r['waste_cost_kes']-r['holding_cost_kes'] for r in rows)
    return dict(requested_kg=req,sold_kg=sold,unfilled_kg=req-sold,fill_rate_pct=100*sold/req,expired_kg=expired,supply_kg=supply,waste_rate_pct=100*expired/supply,closing_kg=closing,average_closing_kg=sum(r['closing_kg'] for r in rows)/(DAYS-WARMUP),revenue_kes=sum(r['revenue_kes'] for r in rows),modelled_contribution_kes=round(margin,2))

def build(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True);all_results=[];main_ledger=[];main_batches=[]
    for scenario in SCENARIOS:
        for seed in SEEDS:
            for policy in POLICIES:
                rows,batches,demand=run(seed,policy,scenario);m=metrics(rows)
                all_results.append(dict(scenario=scenario,seed=seed,policy=policy,**m))
                if scenario=='base' and seed==MAIN_SEED:main_ledger.extend(rows);main_batches.extend(batches)
    main=[r for r in all_results if r['scenario']=='base' and r['seed']==MAIN_SEED]
    summaries=[]
    for scenario in SCENARIOS:
        baseline={r['seed']:r for r in all_results if r['scenario']==scenario and r['policy']=='sales_only'}
        for policy in POLICIES:
            group=[r for r in all_results if r['scenario']==scenario and r['policy']==policy]
            fields=['fill_rate_pct','waste_rate_pct','modelled_contribution_kes','average_closing_kg']
            summaries.append(dict(scenario=scenario,policy=policy,seeds=len(group),**{k:statistics.mean(r[k] for r in group) for k in fields},min_fill_rate_pct=min(r['fill_rate_pct'] for r in group),max_fill_rate_pct=max(r['fill_rate_pct'] for r in group),contribution_wins_vs_sales_only=sum(r['modelled_contribution_kes']>baseline[r['seed']]['modelled_contribution_kes'] for r in group)))
    products=[dict(policy=policy,sku=p['sku'],**metrics([r for r in main_ledger if r['policy']==policy and r['sku']==p['sku']])) for policy in POLICIES for p in PRODUCTS]
    result=dict(classification='Entirely synthetic simulation; not Unified Meat Packers records or outcomes',days=DAYS,warmup_days=WARMUP,evaluation_days=DAYS-WARMUP,seeds=SEEDS,main_seed=MAIN_SEED,products=PRODUCTS,policies=POLICIES,scenarios=SCENARIOS,main=main,summary=summaries,by_product=products)
    (output/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
    def write(name,rows):
        with (output/name).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    write('daily_ledger.csv',main_ledger);write('batch_receipts.csv',main_batches);write('synthetic_demand.csv',inputs(MAIN_SEED,SCENARIOS['base']['late_prob']));write('sensitivity.csv',all_results)
    print(json.dumps(main,indent=2));return result

if __name__=='__main__':build(Path(__file__).parent/'data')
