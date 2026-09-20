# Source, definitions and analytical limits

## Source and attribution
Olist, Brazilian E-Commerce Public Dataset by Olist: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
Official download: https://www.kaggle.com/api/v1/datasets/download/olistbr/brazilian-ecommerce
Retrieved 20 September 2026. Source metadata reports CC BY-NC-SA 4.0 and last update 1 October 2021. The download's CSV fingerprints are retained in data/analysis.json. The metadata contains inconsistent historical version numbering, so fingerprints identify these exact inputs more reliably than a version label.

This is real anonymised historical data, not a synthetic simulation. The source describes transactions from 2016–2018. All source orders have purchase timestamps from 4 September 2016 to 17 October 2018. Eligible delivered orders were purchased September 2016–August 2018. Neither period is a complete calendar-year comparison or a current service assessment.

Derived aggregates and analytical adaptation in this case are shared under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Changes: joining, filtering, order-level grouping, metric calculations and narrative interpretation. Raw identifiers, review text and precise coordinates are not republished. Attribution does not imply Olist endorsement.

## Grain and joins
Primary unit: one order. Orders join to customers on customer_id; customer, order, seller and product keys are unique. Order items are grouped to order-level category and seller counts before use. Orders with several categories get a separate multiple_categories label, rather than being counted once per category. Multi-seller orders get their own route group. State refers to customer destination, not seller origin.

Reviews are not unique per order: 547 source orders have multiple review rows. The main review comparison uses the latest answer timestamp, then creation timestamp, ID and score as deterministic tie-breakers. A sensitivity check restricts to orders with exactly one review; the low-rating contrast remains 62.4% versus 9.2%. This does not eliminate review-response bias or establish causality.

## Primary cohort
Start with 99,441 orders. Exclude 2,963 whose status is not delivered and 8 delivered orders missing core dates. Require nonempty purchase, delivery and estimated-delivery timestamps; delivery must not precede purchase, and the promise calendar date must not precede the purchase date. Result: 96,470 orders. No remaining records fail that core chronology rule.

Late = customer-delivery DATE strictly after estimated-delivery DATE. Same-day arrivals count on time. Estimated timestamps commonly represent midnight; comparing full timestamps would misclassify delivery during the promised day. Use source calendar dates without timezone conversion because timestamps have no timezone offset. This is an explicit analytical convention, not an independently confirmed Olist SLA.

Late rate = late orders / eligible delivered orders. Cancelled, shipped and other non-delivered statuses are separately reported in analysis.json; this cohort cannot measure the eventual outcomes of all purchased orders. Recent cohorts may be less mature, and delivered-only selection can make performance look better. Do not use the monthly data to claim a sustained improvement.

## Stage comparison
Durations use elapsed hours divided by 24, including weekends. Stage subset additionally requires purchase ≤ approval ≤ handover ≤ delivery. Exclude 15 with missing stage dates and 1,373 out-of-sequence records, leaving 95,082 (88,573 on time; 6,509 late). Averages use the same subset across all three stages, so they add to average end-to-end time. Most stage exclusions are on-time orders; this subset should not be treated as perfectly representative.

“After handover” means the interval between recorded carrier handover and delivery; it can contain transport, sorting, waiting and failed attempts. It is not a measured carrier fault. Comparing groups defined by lateness describes their elapsed-time profiles; it does not explain a causal mechanism. Promise lengths, geography, seasonality, product and seller mix may differ.

## Review comparison
Low rating = 1 or 2 stars out of 5. Review population: 95,824 eligible orders (646 have no review). On time: 8,289 / 89,443 low reviews; late: 3,983 / 6,381. Survey timing can differ, and ratings cover the whole purchase experience. No causal effect, lost revenue, churn or savings is estimated.

## Quality and validation
Key uniqueness and relevant foreign-key checks pass. Customer-state totals reconcile to the primary cohort. SQL in verify.sql independently recomputes the primary denominator and late count directly from the raw order rows. A separate SQL implementation in verify_analysis.py also confirms both review populations, all three stage means and all destination counts. Fingerprints, exclusions, status counts, review sensitivity, stage denominators and all published aggregates are retained in data/analysis.json. No stockout, inventory, warehouse or carrier-level claims are supported by this dataset.
