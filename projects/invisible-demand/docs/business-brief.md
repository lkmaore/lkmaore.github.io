# See the demand. Test the decision.

## Experience and purpose
Inspired by Lesley Maore's Commercial Data Analyst & Sales Manager role at Unified Meat Packers (September 2019–January 2023). The current CV reports that Excel tracking tools and sales forecasting models supported a 35% increase in total revenue. This case is a separate, fictional learning exercise. The CV figure is not a simulation target, an independently verified result or an outcome of this portfolio work; its comparison period is unspecified.

Proposed audience: sales operations, purchasing and finance at a fictional meat distributor. These roles have not been interviewed. Decision: whether to introduce a lightweight unfilled-request log and how to evaluate its use in replenishment before changing purchasing rules.

## The problem in one example
A customer asks for 10 kg. Only 6 kg can be supplied. A sales-only report contains 6 kg; a request log records 10 requested, 6 fulfilled and 4 unfilled. A buyer using recorded sales as demand may miss that opportunity. But automatically increasing stock can create waste when goods have limited selling time.

## What the experiment establishes
In this chosen simulation, more complete request information slightly improves fulfilled demand but does not reliably improve modelled contribution under the unchanged buying rule. Results depend strongly on stock buffers and modelled shelf life. This supports testing the reporting process and purchasing rule separately, not promising a universal gain.

## Proposed workflow
Sales captures a request → record requested and fulfilled kg → identify the unfilled reason → purchasing reviews shortages alongside stock age and outstanding replenishment → finance checks fulfilment, waste and contribution together → approve or reject a bounded policy trial against an agreed service floor.

## Requirements and acceptance criteria
1. One request-product line per identifier. Store requested kg, fulfilled kg, unfilled kg, date, product and reason. Acceptance: 10 requested and 6 fulfilled reconciles to 4 unfilled. A later delivery must not be counted again as new demand; distinguish cancellation, substitution and backlog explicitly if used.
2. Missing is unknown. Acceptance: unanswered quantity fields do not become zero; unsupported reasons remain “unclassified”. Report completion coverage and audit a sample of entries.
3. Preserve the existing sales record. Acceptance: invoice totals remain unchanged when an unfilled request is logged. No fictional requested amount becomes recognised revenue.
4. Separate visibility from action. Acceptance: the request log creates a review item, not an automatic purchase order. Buyers see stock age, open purchase orders and the applicable service/waste comparison before deciding.
5. Keep a balanced scorecard. Acceptance: show requested and fulfilled kg, expired kg with denominator, average stock and contribution definition. No single KPI determines success. Logging effort and costs must be measured before claiming a positive business case.
6. Evaluate fairly. Acceptance: define the comparison period and service floor before the trial, preserve product and weekday mix, document supplier disruptions, and report adverse as well as favourable outcomes. Agree any service threshold with stakeholders rather than inventing one from this simulation.

## Open questions for a real business
Are requests logged before checking stock? What happens to unfilled demand? Can customers substitute? Can shelf age be tracked reliably? Which costs change with stock? What service level is commercially acceptable? How much staff time would logging take? Do account prices and delivery promises affect demand?

## Contribution
AI-assisted portfolio project. Lesley supplied the experience context and directed the business-analysis and storytelling goals. AI assisted research, simulation, calculations, validation and implementation. No actual stakeholder interviews, employer data, operational deployment or realised financial benefits are claimed.
