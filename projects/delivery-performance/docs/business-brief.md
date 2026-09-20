# Delivery reliability: business analysis brief

## Decision and audience
A proposed operations review for a marketplace logistics lead and customer-support lead: where should they investigate late deliveries first, and what exception information would help them act? These are proposed stakeholder roles, not interviews or a consulting engagement.

## Business context
Olist's source description explains that merchants fulfil orders through logistics partners. One order can contain multiple products and sellers. Customers receive a survey after delivery or when the estimated delivery date is due. This case uses historical, anonymised Brazilian transactions. It does not describe current Olist performance or Lesley's employers.

## Process represented by the available timestamps
Purchase → approval → carrier handover → customer delivery. Compare the delivered calendar date with the estimated delivery calendar date. A late delivery means the promise was missed, not merely that a journey was long.

Missing from this process: warehouse scans, failed delivery attempts, carrier identity, incident reasons, inventory availability, staffing and customer-contact history. The observed stages locate elapsed time; they do not establish responsibility.

## Findings and proposed decisions
- 6,534 of 96,470 eligible delivered orders arrived after the promised calendar date (6.8%). Keep the 2,963 non-delivered records visible as a separate status population; they are not counted as successful deliveries.
- Among reviewed orders, 62.4% of late deliveries received 1–2 stars, versus 9.3% of on-time deliveries. Consider a proactive support pilot for overdue orders. This association is not an estimate of the improvement that a pilot would achieve.
- In 95,082 orders with valid stage sequences, late orders averaged 27.9 days after carrier handover, versus 8.0 days for on-time orders. Examine tracking events and route conditions before changing partners or assigning blame.
- São Paulo has the most late orders (1,820), but a 4.5% late rate. Rio de Janeiro has 1,495 late orders and a 12.1% rate; its 12.8% share of eligible orders accounts for 22.9% of late orders. Start a diagnostic sample in Rio, while retaining São Paulo on the volume watchlist. Neither figure is adjusted for seller, route, category or purchase-month mix.

## Proposed requirements and acceptance criteria
These are design proposals, not a system delivered to Olist.

1. **One order, one exception.** An operations analyst should see one row per undelivered order whose promised calendar date has passed. Multiple items must not multiply the queue. Acceptance: an order with three items produces one exception; a delivered, cancelled or unavailable order is not in this operational queue. Missing promise dates appear in a separate data-quality queue.
2. **Explain the stage.** Show purchase, approval, handover and promise dates, destination and latest verified status. Acceptance: missing timestamps read “unknown”, never zero days; an impossible timestamp sequence is flagged and excluded from stage averages.
3. **Prioritise visibly.** Sort by days overdue and allow destination filtering. Display both exception counts and eligible-order denominators. Acceptance: changing destination updates numerator and denominator together; empty groups show “no eligible orders”. Overdue age is based on the local business calendar, which must be agreed before implementation.
4. **Support handoff.** Propose an owner and contact status for each exception, subject to validation with operations and support. Acceptance: ownership changes are recorded; automated customer messages require an approved communication policy. The historical dataset cannot test these fields.
5. **Measure a pilot honestly.** Compare customer contacts, eventual delivery, review outcomes and handling time with an appropriate comparison group. Agree targets after establishing a baseline. Do not promise a percentage reduction from this descriptive study.

## Questions for a real stakeholder workshop
Which timestamp defines an actual carrier handover? Can orders ship in multiple parcels? How is the customer promise set and changed? What incidents and tracking events can be joined? Who owns overdue communication? How do we avoid labelling an incomplete recent order as a final outcome?

## Contribution and limits
AI-assisted portfolio learning project. Lesley directs the business-analysis framing and storytelling; AI assisted data preparation, calculations, validation and implementation. No stakeholder interviews, employer endorsement, operational deployment or realised savings are claimed.
