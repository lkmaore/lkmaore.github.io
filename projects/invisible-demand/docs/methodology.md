# Simulation design and limits

All data is fictional. The model represents an illustrative distributor, not Unified Meat Packers. Quantities are kg; currency is KES. Prices, costs, storage charge, lead times and shelf lives are assumptions, not market quotes, employer facts or food-safety advice. No actual sales uplift, waste reduction or savings is claimed.

## Question and comparisons
Does recording unfilled customer requests improve replenishment outcomes under a simple sales-based buying rule? The three information policies record 0%, approximately 50% (rounded whole kg daily) or 100% of unmet demand. All use the same replenishment rule. Full logging is an idealised information condition; silent walkaways are not assumed observable in practice.

Five scenarios compare the baseline with one change at a time: zero extra buffer, a two-day extra buffer, shelf lives shortened by two days, or less reliable supply. No policy is selected after searching for an optimal parameter. There is no proof of optimality. Results are descriptive outputs of this chosen mechanism, not estimates of real-world causal effects.

## Inputs and chronology
Four fictional products. Simulate 240 days; exclude the first 60 as warm-up, then score days 60–239 (180 days). Seeds 0–19 are all reported without selecting favourable runs. The main ledger is seed 0, chosen before inspecting outcomes. Demand has weekday variation, lognormal noise (sigma 0.35), an 8% chance of a demand spike and a 25% level increase from day 120. The 25% is a simulation assumption unrelated to the CV's 35% revenue claim. No real dates, customer identities or sales records are reconstructed.

Supplier arrivals take one day or three days: 15% probability of three days in baseline, 40% under less reliable supply. Demand and supplier random streams are generated independently, and each policy sees exactly the same underlying scenario/seed path. Quantities do not affect lead time; suppliers have unlimited capacity. The planning assumption remains two days in every scenario. Lead-time outcomes determine arrivals but are not forecast inputs.

Each day: record opening stock; discard batches reaching the model expiry day; receive scheduled orders; fulfil demand from the earliest-expiring batch; record fulfilled and unfilled kg; calculate closing stock; place replenishment for a future arrival. Unfilled demand is lost, not backlogged, substituted or recovered later. Shelf life starts at receipt; supplier transit ageing and quality rejection are excluded. Opening inventory is three base-demand days with a full model lifetime.

Forecast = mean of the last 28 observed daily quantities (all available history initially). Observed quantity = sold kg + captured unfilled kg. Today's observation can inform the order placed at the end of today. Future demand is not used. Order-up-to target = ceiling(forecast × (two planned lead days + one review day + buffer days)). Order quantity = max(0, target − closing stock − outstanding order quantity). Baseline buffer is one day. Orders in transit are counted; future expiry is not forecast. That limitation is a reason to test the rule, not to recommend it as an optimal solution.

## Metrics
- Fill rate = fulfilled kg / requested kg over the scored window. This is volume fulfilment, not the share of complete orders or customer retention.
- Waste rate = expired kg / (stock at start of day 60 + receipts during scored window). Denominator counts each available unit once. End-of-window stock is reported; stock remaining or still in transit is not assumed to expire.
- Average stock = sum of product closing kg over scored days / 180.
- Modelled contribution = fulfilled kg × (price − unit cost), less expired kg × unit cost, less closing kg × assumed KES 0.80 per kg-day. This is not net profit, cash flow or ROI. Labour, logging cost, transport, tax, fixed expenses, discounts and customer lifetime value are excluded. Closing inventory is neither charged as sold nor credited as income.
- Sensitivity summaries average per-run rates across 20 equal-weight seeds. Ranges describe simulated variation, not confidence intervals. Contribution wins compare each policy with sales-only on the identical seed and scenario. Seeds are not real businesses or independent empirical evidence.

## Fairness and limits
The logging rule mechanically supplies more demand to the buying rule. Extra information cannot by itself require extra purchases; the chosen rule makes that link. Better decision logic could ignore or use the information differently. Therefore the negative result concerns this rule and these assumptions, not the intrinsic value of information.

The baseline's high availability leaves little room for additional fulfilment. Shelf-life and buffer choices materially change the outcome. Capture is an exact fraction of quantity with no entry errors or reporting cost—an optimistic simplification. In practice, use requested, fulfilled and unfilled quantities from actual enquiries/orders and track unknowns separately. Do not treat a missing request record as zero demand.

## Validation
Every daily product-policy record checks opening + receipts = sold + expired + closing and requested = sold + unfilled. Scored-window totals also reconcile. verify.py independently recomputes headline metrics with SQL, verifies unique grain and identical demand paths, checks paired sensitivity coverage and confirms zero captured requests reproduces the sales-only metrics. Source code and generated data are supplied. The notebook checks the saved result bindings; it does not independently establish the realism of assumptions.
