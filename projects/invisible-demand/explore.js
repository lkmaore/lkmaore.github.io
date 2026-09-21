const labels={sales_only:'Sales only',half_logged:'Half of unmet kg logged',all_logged:'All unmet kg logged'};
fetch('data/analysis.json').then(r=>{if(!r.ok)throw Error('data');return r.json()}).then(data=>{
 const select=document.getElementById('scenario'),out=document.getElementById('scenario-results');
 function render(){out.replaceChildren();const grid=document.createElement('div');grid.className='scenario-grid';
 data.summary.filter(r=>r.scenario===select.value).forEach(r=>{const card=document.createElement('article');const h=document.createElement('h3');h.textContent=labels[r.policy];card.append(h);
 [['Demand fulfilled',r.fill_rate_pct.toFixed(2)+'%'],['Waste / available kg',r.waste_rate_pct.toFixed(2)+'%'],['Average closing stock',r.average_closing_kg.toFixed(1)+' kg'],['Modelled contribution','KES '+Math.round(r.modelled_contribution_kes).toLocaleString()]].forEach(([label,value])=>{const p=document.createElement('p');p.textContent=label;const s=document.createElement('strong');s.textContent=value;p.append(s);card.append(p);});
 const note=document.createElement('small');note.textContent='Fill rate across runs: '+r.min_fill_rate_pct.toFixed(2)+'–'+r.max_fill_rate_pct.toFixed(2)+'%. Range, not a confidence interval.';card.append(note);grid.append(card);});out.append(grid);}
 select.addEventListener('change',render);render();
}).catch(()=>{document.getElementById('scenario-results').textContent='Interactive results could not load. The fixed tables above contain the reviewed comparisons.';});