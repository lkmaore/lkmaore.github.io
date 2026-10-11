"""Rebuild the public historical snapshot from the included source extracts. Python standard library only."""
from pathlib import Path
import csv,json,math
P=Path(__file__).resolve().parent

def read_data():
    elections=[]
    for row in csv.DictReader((P/'data/elections-2022.csv').open()):
        r={k:(v if k=='county' else int(v)) for k,v in row.items()}
        r['ballots']=r['valid_votes']+r['rejected_ballots']
        r['not_recorded_voting']=r['registered']-r['ballots']
        r['turnout_pct']=100*r['ballots']/r['registered']
        elections.append(r)
    budgets=[]
    for row in csv.DictReader((P/'data/county-budgets-2023-24.csv').open()):
        r={k:(v if k=='county' else float(v)) for k,v in row.items()}
        for kind in ['recurrent','development','total']:
            r[kind+'_pct']=100*r[kind+'_spent_m']/r[kind+'_budget_m']
        r['development_share_of_spending_pct']=100*r['development_spent_m']/r['total_spent_m']
        budgets.append(r)
    return elections,budgets

def analyze():
    e,b=read_data()
    assert len(e)==48 and len({r['code'] for r in e})==48
    assert len(b)==48 and len({r['county'] for r in b})==48
    assert all(0<=r['ballots']<=r['registered'] for r in e)
    assert sum(r['valid_votes'] for r in e)==14213137
    assert sum(r['rejected_ballots'] for r in e)==113614
    # Preserve discrepancies in the published declaration, not silently corrected guesses.
    assert sum(r['registered'] for r in e)==22119458
    assert sum(r['declared_valid_minus_candidate_sum'] for r in e)==110
    for r in b:
        for suffix in ['budget_m','spent_m']:
            assert abs(r['recurrent_'+suffix]+r['development_'+suffix]-r['total_'+suffix])<=.021
        for kind in ['recurrent','development','total']:
            assert abs(r[kind+'_pct']-r['reported_'+kind+'_pct'])<.11
    total=b[-1];assert total['county']=='Total'
    for k in ['recurrent_budget_m','development_budget_m','total_budget_m','recurrent_spent_m','development_spent_m','total_spent_m']:
        assert abs(sum(r[k] for r in b[:-1])-total[k])<.15
    aliases={'Elgeyo/Marakwet':'Elgeyo-Marakwet','Tharaka - Nithi':'Tharaka-Nithi'}
    lookup={r['county']:r for r in b[:-1]};counties=[]
    for r in e[:-1]:
        name=aliases.get(r['county'],r['county']);assert name in lookup,name
        counties.append({'county':name,'election':r,'budget':lookup[name]})
    national={'registered':22120458,'valid_votes':14213137,'rejected_ballots':113614}
    national['ballots']=national['valid_votes']+national['rejected_ballots']
    national['turnout_pct']=100*national['ballots']/national['registered']
    national['not_recorded_voting']=national['registered']-national['ballots']
    return {'scope':'Historical: presidential election 2022; budgets and parliamentary activity FY 2023/24. Not a current performance scorecard.', 'counties':counties,'national_election':national,'diaspora':e[-1],'national_budget':total,'parliament':json.loads((P/'data/parliament-2023-24.json').read_text()),'quality':{'declared_minus_sum_registered':1000,'declared_valid_minus_candidate_sum':110,'senate_sittings_excluded':'Narrative implies 124; Table 5.9 gives 120. Not used in comparisons.','overall_absorption':'Budget narrative gives 79.5%; Table 2.3 gives 79.4%. Recalculation from table values rounds to 79.4%.'}}

if __name__=='__main__':
    x=analyze();(P/'data/analysis.json').write_text(json.dumps(x,indent=2)+'\n')
    print('PASS: 47 county joins; 48 election geographies; published election totals; known source differences retained; budget arithmetic and national totals within published rounding.')
    print('Turnout:',round(x['national_election']['turnout_pct'],2),'Development budget spent:',round(x['national_budget']['development_pct'],1),'Development share of expenditure:',round(x['national_budget']['development_share_of_spending_pct'],1))
