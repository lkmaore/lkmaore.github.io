# See the demand. Test the decision.

A fictional meat-distribution experiment by Lesley Maore: **does recording unfilled requests improve a buying decision, or simply create more stock?**

[Read the case study](https://lkmaore.github.io/projects/invisible-demand/) · [Executed learning notebook](notebook.html)

## Experience connection
Inspired by the sales and inventory work described in Lesley's current CV: Commercial Data Analyst & Sales Manager, Unified Meat Packers, September 2019–January 2023. The CV reports Excel tracking tools and forecasting models supported a 35% increase in total revenue; its comparison period is unspecified. That is a CV-reported historical claim. This fictional project neither reconstructs nor verifies it.

## The experiment
Three information policies—sales only, half of unfilled kg logged, all unfilled kg logged—use the same simple buying rule. Test four fictional products for 240 days, score the last 180, and repeat on 20 seeds in five operating scenarios. All 300 policy runs are retained.

The baseline result challenges the initial expectation: full logging slightly improves fulfilment but lowers modelled contribution in all 20 baseline runs. With one less buffer day, the contribution difference becomes slightly positive on average and positive in 13 of 20 runs. Better information does not automatically justify buying more under the existing rule.

No real-world savings, inventory performance or optimal policy is claimed. Review [methodology](docs/methodology.md), [business brief](docs/business-brief.md) and [research attribution](docs/research-and-attribution.md).

## Reproduce
Python 3.10+; simulation and validation require only the standard library:

```sh
python3 simulate.py
python3 verify.py
```

Outputs:
- `data/synthetic_demand.csv`: 960 fictional product-day requests and supplier lead outcomes for seed 0.
- `data/daily_ledger.csv`: 2,880 product-day-policy records for baseline seed 0; opening, receipts, sold, expired and closing kg reconcile.
- `data/batch_receipts.csv`: received replenishment batches for baseline seed 0. Orders still in transit at the end are not received stock.
- `data/sensitivity.csv`: all 300 scenario-seed-policy metric rows.
- `data/analysis.json`: reviewed aggregates, policy assumptions and parameter values.

`analysis.ipynb` reruns the simulation, checks it against the published snapshot, runs the independent SQL checks and charts the comparisons. Notebook rendering uses Jupyter and Matplotlib. Saved outputs and a readable HTML export are included.

## What makes the treatment useful
The project asks what information to collect and what decision it should change. It separates a reporting improvement from a purchasing-policy improvement, keeps adverse results visible and translates the findings into proposed acceptance criteria. Censored demand is an established research topic; this is an educational application, not a claim of academic novelty.

## Contribution and disclosure
AI-assisted learning project. Lesley supplied experience context and directed the business-analysis and storytelling goals; AI assisted research, simulation, calculations, validation and implementation. No employer records, interviews, implemented workflow or realised benefits are claimed. Quantities, prices, costs, shelf lives and supplier behaviour are fictional assumptions. Shelf-life settings are not food-safety guidance.
