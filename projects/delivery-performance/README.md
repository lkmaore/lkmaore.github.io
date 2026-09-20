# When delivery breaks the promise

**A public-data supply-chain and business-analysis case study by Lesley Maore.**

[Read the case study](https://lkmaore.github.io/projects/delivery-performance/) · [Read the executed notebook](https://lkmaore.github.io/projects/delivery-performance/notebook.html)

## The business question
Where are orders losing time, and what should the business investigate to make delivery more reliable?

Olist's anonymised Brazilian e-commerce records let us connect a delivery promise with the actual customer experience. This project explains the process to a reader with no logistics background, uses fair denominators and turns observations into proposed requirements.

## What the evidence says
- 6,534 / 96,470 eligible delivered orders arrived late: **6.8%**.
- **62.4%** of reviewed late orders received 1–2 stars, compared with **9.3%** of reviewed on-time orders. Association is not causation.
- On a common valid-stage subset, late orders averaged **27.9 days after carrier handover**, versus **8.0 days** for on-time orders. The interval does not establish carrier fault.
- Rio de Janeiro has a **12.1%** late rate; São Paulo has **4.5%** but more late orders in absolute terms. Both rate and volume matter when choosing an investigation.

## What I built
- A plain-language, purple-and-coral portfolio case study with a process map and interactive destination comparison.
- A reproducible Python analysis and an independent SQL reconciliation of the main cohort.
- An executed learning notebook with charts, exclusions and a sensitivity check.
- A [business brief](docs/business-brief.md) with proposed stakeholder roles, an overdue-order queue concept, requirements and acceptance criteria.
- A [methodology record](docs/methodology.md) with definitions, provenance and limitations.

## Reproduce
Download the original [Olist dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and extract its CSV files locally. Do not commit raw_data/ to this public repository.

From this project directory, with Python 3.10 or newer:

```sh
python3 analyze.py /path/to/extracted/csv --output data/recomputed.json
python3 verify_analysis.py /path/to/extracted/csv
```

The main analysis needs only Python's standard library. It checks key uniqueness, relevant joins and SQL/Python agreement. The published `data/analysis.json` contains reviewed aggregates and SHA-256 fingerprints of the input files.

For the notebook, install `jupyter`, `nbclient`, `nbformat` and `matplotlib` in a virtual environment. Put the CSVs in `raw_data/`, or set `OLIST_DATA_DIR` to their directory. Run `analysis.ipynb` from top to bottom. It checks the complete recomputation against the published snapshot before plotting. Saved outputs are included, and `notebook.html` is a readable export.

## Scope and honesty
Historical orders from 2016–2018, not current operational performance. The main rate is delivered-only, so incomplete and non-delivered orders need separate monitoring. No inventory, stockout, causal, carrier-fault or realised-savings claims are made. Recommendations are proposals, not a deployed solution.

AI-assisted learning project: Lesley directed the business-analysis framing and storytelling; AI assisted preparation, calculations, validation and implementation. No stakeholder interviews or work commissioned by Olist are claimed.

## Attribution and licence
Source: **Olist, Brazilian E-Commerce Public Dataset by Olist**, distributed through Kaggle under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Retrieved 20 September 2026. This analytical adaptation and its derived aggregates retain that licence. Changes include cleaning rules, joins, aggregation, charts and interpretation. No endorsement is implied. Raw identifiers, review text and precise coordinates are not republished.
