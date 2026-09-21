# Lesley Maore — Business analysis & data storytelling

**I make data make sense.**

I’m building a career in business analysis with one ambition: give the data a voice everyone in the room can understand. If someone enters a meeting without the backstory, the analysis should still make sense.

[Visit the portfolio](https://lkmaore.github.io/) · [Connect on LinkedIn](https://www.linkedin.com/in/lesleymaore/)

## Featured case studies

### Growing sales. Shrinking margins.

A fictional consumer-goods distributor needs to know whether rising sales are translating into stronger profits and whether it is meeting revenue targets.

January–August 2026 revenue grew **21.9%**, but gross profit grew only **8.1%**. Revenue was **8.0% below budget**. The case study explains what this means, where management should focus, and what evidence is needed before acting.

[Read the story](https://lkmaore.github.io/projects/commercial-performance/) · [Inspect the project](projects/commercial-performance/README.md)

### When delivery breaks the promise.

A public-data supply-chain case study asks where delivery time accumulates and how operations should prioritise an investigation. It connects delivery reliability with customer experience, then proposes an exception queue and acceptance criteria.

[Read the story](https://lkmaore.github.io/projects/delivery-performance/) · [Inspect the project](projects/delivery-performance/README.md)

### See the demand. Test the decision.

A fictional meat-distribution experiment asks whether recording unmet demand improves replenishment decisions. Across 300 policy runs, better visibility helps under some assumptions but can increase waste under an unchanged buying rule. The story connects evidence to requirements for a proposed operational pilot.

[Read the story](https://lkmaore.github.io/projects/invisible-demand/) · [Inspect the project](projects/invisible-demand/README.md)

## How this portfolio is organised

- `index.html`: home, work, about, and contact.
- `projects/commercial-performance/`: standalone case study and supporting evidence.
- `projects/delivery-performance/`: public-data case study, Python/SQL analysis, notebook and proposed requirements.
- `projects/invisible-demand/`: synthetic inventory experiment, reproducible notebook, assumptions and proposed requirements.
- `assets/`: responsive styling and small navigation enhancement.

The site is static HTML and CSS with minimal optional JavaScript. Reading the case study does not require an account, JavaScript, or access to the private Power BI report.

## Run locally

From this directory:

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000`. GitHub Pages serves the repository root from `main`; `.nojekyll` keeps the static files unchanged. There is no custom domain or paid hosting dependency.

## Honest scope

These are AI-assisted learning case studies. Project 1 uses synthetic data; Project 2 uses real anonymised historical Olist data. The inventory case also uses fictional data and simulated outcomes; CV-reported achievements are separately attributed and are not validated by the simulation. These learning cases do not claim client work, stakeholder interviews, implemented recommendations or realised business benefits. Each case explains its source, limitations, contribution and assistance used.
