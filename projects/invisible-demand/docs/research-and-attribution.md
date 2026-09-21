# Research and attribution

Review date: 21 September 2026. This is a small framing review, not an exhaustive literature review or a claim of originality. No external code or data was copied. Synthetic records and simulation code were created for this portfolio with AI assistance.

## Research informing the question
- [Sachs & Minner (2014), The data-driven newsvendor with censored demand observations](https://www.sciencedirect.com/science/article/pii/S092552731300203X). Publisher-indexed abstract/introduction reviewed; direct page retrieval failed. Establishes that sales can conceal unsatisfied demand and describes an estimation approach using sales timing. We borrow the problem framing, not its estimator or results. Our simulation assumes some unmet requests can be recorded directly.
- [Demand Estimation and Ordering Under Censoring: Stock-Out Timing Is (Almost) All You Need — INSEAD publication summary](https://www.insead.edu/faculty-research/publications/journal-articles/demand-estimation-and-ordering-under-censoring-stock). Institutional summary retrieved through search; direct page retrieval failed. Motivates the distinction between sales observations and the information available about stockouts. We do not implement or claim its Bayesian method.
- [Replenishment strategies for lost sales inventory systems of perishables under demand and lead time uncertainty](https://doi.org/10.1016/j.ejor.2022.11.041). Publisher search excerpt reviewed, not full paper. Informs the need to examine uncertainty and issuing rules rather than treating stock as timeless. Our simple rule is not the paper's algorithm or an optimal policy.

## Portfolio examples reviewed
- [idowuemmao, Food & Beverage Supply Chain Analytics Dashboard](https://github.com/idowuemmao/Food-Beverage-Supply-Chain-Analytics-Dashboard-Power-BI): repository README reviewed. Broad coverage of delivery performance, inventory risk, waste, supplier reliability and profitability. We use it as an example of the wider dashboard scope, not as a source of calculations or design assets.
- [Ayushdash02, Food Waste Management Dashboard](https://github.com/Ayushdash02/Food-Waste-Management-Dashboard): repository overview reviewed. Focuses on food redistribution, operational indicators and exploration. No files or code reused.

## What differentiates this treatment
The central decision is whether collecting unmet requests should change an inventory-buying rule, and under which conditions. The case explicitly retains results in which extra captured demand worsens modelled contribution. It compares information capture separately from stock buffer, includes partial capture and makes proposed logging requirements part of the output. This is a distinctive emphasis for this portfolio, not a claim that censored demand or inventory simulation is new.

## Other source categories
The user's designated current CV supplies the role and 35% total-revenue achievement. That is a CV-reported historical claim, not verified with this fictional dataset. The public portfolio includes only the relevant professional context; the source CV and referee information remain private.
