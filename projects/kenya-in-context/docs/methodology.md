# Methods and quality record

Reviewed 11 October 2026. Historical snapshot: election 2022; county budgets and parliamentary activity July 2023 to June 2024. These were selected to form a fixed, inspectable study, not because they are the latest releases. No synthetic values.

## Sources and extraction

`data/sources.json` records exact URLs, PDF pages, source hashes and the upstream election CSV commit. The primary IEBC host did not return the evaluation PDF after a normal and escalated connection attempt. The results declaration was inspected as reproduced in Carter Center Appendix A, PDF pages 50-52, dated 15 August 2022.

Paul-Oti's county valid-vote and rejected-ballot columns were used, with county rows checked against the reproduced declaration. Registered-voter values were transcribed directly from that declaration. The pre-election county register was used for names and to investigate coverage, not as a turnout denominator. Do not assume all register differences have been explained.

Budget Table 2.3 was extracted from PDF text and visually checked on PDF pages 28-29. Published amounts are KES million to two decimal places. Parliamentary counts were transcribed and visually checked on PDF pages 81 and 89. PDF copies remain outside the public repository; download the linked originals to inspect extraction against them.

## Definitions

- Presidential ballots recorded = published valid votes + rejected ballots.
- Turnout = ballots recorded / registered voters in the same declaration, multiplied by 100.
- Registered voters not recorded voting = registered minus ballots recorded. This is a descriptive residual, not an explanation of abstention.
- Development absorption = development expenditure / approved development budget, multiplied by 100.
- Development share of expenditure = development expenditure / all expenditure, multiplied by 100.
- Parliamentary processed counts are activity measures defined by the annual report. They do not establish final resolution or unique cross-House items.

County names are joined with two explicit aliases: Elgeyo/Marakwet to Elgeyo-Marakwet and Tharaka - Nithi to Tharaka-Nithi. Diaspora is separate. No unmatched county is discarded. All 47 county matches are required.

## Preserved source discrepancies

1. Geographic registered-voter rows including diaspora sum to 22,119,458, while the declaration's national row is 22,120,458. Preserve the 1,000 difference. National turnout uses the national row; county calculations use their own rows. Do not derive a national rate by averaging county rates.
2. Kilifi's published valid votes exceed the candidate-column sum by 10; West Pokot's by 100. All published valid totals sum to the declared national valid total. Preserve and flag the differences instead of inventing corrections. No fraud, intent or outcome implication is drawn.
3. Budget narrative says 79.5% total absorption, while Table 2.3 and its rounded inputs support 79.4%. Use the table calculation.
4. The Senate sitting narrative implies 124, whereas Table 5.9 says 120. Sittings are excluded, not silently reconciled.
5. Rounded budget components may differ from published totals by KES 0.01 million. Validation allows up to 0.021 million per row and 0.15 million across all counties. Rates may differ by at most 0.11 percentage points from printed one-decimal values. These tolerances are for published rounding, not missing data.

## What cannot be concluded

No turnout cause, demographic voting behaviour, party preference, electoral prediction, corruption allegation, service completion, legislator quality or electoral impact is estimated. Spending is reported financial activity, not verified quality. Counts do not establish outcomes. No statistical relationship between turnout and budget performance is estimated.

## Acceptance criteria

Every displayed metric includes period, unit, denominator or stage and a source. All county selections must match the exported results. A proposed reader test should check whether a person can restate a metric and identify one unsupported conclusion. No reader test has yet occurred.
