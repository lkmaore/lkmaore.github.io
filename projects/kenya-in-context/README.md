# Kenya, in context.

**How does a public headline change when its denominator, scope and stage become visible?**

[Read the case](https://lkmaore.github.io/projects/kenya-in-context/) · [Read the notebook](notebook.html)

A historical civic-data study for readers without political background. It covers the 2022 presidential election, FY 2023/24 county budgets and parliamentary activity. It is not a current political tracker or a ranking of leaders.

## What it shows

- National presidential turnout of 64.77% uses the declared registered electorate, not the whole population.
- Development expenditure is 57.5% of its approved budget but 24.4% of all county spending. The numerator is the same; the denominators answer different questions.
- The National Assembly's 128 bills processed cannot be relabelled as 128 laws enacted. The two Houses' activity counts cannot safely be added as unique items.

The interactive explorer covers all 47 counties, with an accessible table fallback. Elections and budgets are shown for convenience, without causal linkage or a composite political score.

## Reproduce

Python 3.10+, standard library:

```sh
python3 analyze.py
```

This rebuilds `data/analysis.json` and checks coverage, joins, published totals, budget arithmetic and known source discrepancies. `analysis.ipynb` adds a readable, executed explanation of the calculations and figures. It requires nbformat/Jupyter and matplotlib to rerun.

## Evidence and contribution

See [methods and quality](docs/methodology.md), [research review](docs/research-review.md), and [source manifest](data/sources.json). Election CSV totals credit Paul-Oti's Kenya Election Data, with its MIT licence preserved. Primary evidence is IEBC's declaration reproduced in Carter Center Appendix A, Controller of Budget Table 2.3 and Parliamentary Service Commission Tables 5.2 and 5.10. Original PDFs are linked, not republished.

Lesley selected the civic-understanding purpose and accessible storytelling direction. AI assisted the source research, extraction, computations, verification, writing and implementation. No interviews, usability results, professional commission, independent audit or realised public impact is claimed.
