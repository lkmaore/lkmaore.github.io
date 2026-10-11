const fmt=n=>Math.round(n).toLocaleString('en-KE');
const money=n=>(n/1000).toFixed(2);
fetch('data/analysis.json').then(r=>{if(!r.ok)throw Error('load');return r.json()}).then(data=>{
 const select=document.getElementById('county'),out=document.getElementById('county-results');
 data.counties.forEach((r,i)=>{const o=document.createElement('option');o.value=i;o.textContent=r.county;select.append(o)});
 function render(){const r=data.counties[Number(select.value)],e=r.election,b=r.budget;
 const panel=(title,metric,body,note,value)=>{const a=document.createElement('article');a.className='county-panel';const h=document.createElement('h3');h.textContent=title;const m=document.createElement('p');m.className='metric';m.textContent=metric;const p=document.createElement('p');p.textContent=body;const bar=document.createElement('div');bar.className='bar';bar.setAttribute('aria-hidden','true');const fill=document.createElement('span');fill.style.width=value+'%';bar.append(fill);const scale=document.createElement('div');scale.className='scale';scale.innerHTML='<span>0%</span><span>Share of stated denominator</span><span>100%</span>';const n=document.createElement('p');n.textContent=note;a.append(h,m,p,bar,scale,n);return a;};
 const grid=document.createElement('div');grid.className='county-grid';
 const vote=panel('Presidential turnout · 2022',e.turnout_pct.toFixed(2)+'%',fmt(e.ballots)+' ballots recorded out of '+fmt(e.registered)+' registered voters.',fmt(e.valid_votes)+' published valid votes and '+fmt(e.rejected_ballots)+' rejected ballots. '+fmt(e.not_recorded_voting)+' registered voters are not recorded voting in these totals. The reason is not observed.',e.turnout_pct);
 if(e.declared_valid_minus_candidate_sum){const f=document.createElement('p');f.className='flag';f.textContent='Source note: the published valid total is '+e.declared_valid_minus_candidate_sum+' above the sum of candidate columns. We retain the published total; see the quality notes.';vote.append(f)}
 const budget=panel('Development budget · FY 2023/24',b.development_pct.toFixed(1)+'% spent','KES '+money(b.development_spent_m)+' billion spent / KES '+money(b.development_budget_m)+' billion approved.','Development was '+b.development_share_of_spending_pct.toFixed(1)+'% of all county expenditure. Spending records alone do not establish completed services.',b.development_pct);
 grid.append(vote,budget);out.replaceChildren(grid);
 }
 select.addEventListener('change',render);render();
}).catch(()=>{document.getElementById('county-results').textContent='The explorer could not load. Read the complete county table under Evidence or download the source extracts.'});
