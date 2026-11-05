# Exploratory macro context comparison

Run November 3, 2026. Same frozen publication-v2 cohort, original exclusions and fixed model settings. This reuses previously inspected evaluation outcomes and is not a new holdout or causal test.

| Model | Brier (lower is better) | Log loss |
|---|---:|---:|
| Historical-rate baseline | 0.002975207 | 0.056089467 |
| Publication history | 0.006058988 | 0.043972731 |
| Publication + unemployment + inflation | 0.004287519 | 0.035823861 |

Macro features reduced Brier error relative to publication history, but did not beat the historical-rate baseline on the specified primary Brier measure. Log loss favors the macro candidate; metric disagreement is retained, not used to change the primary criterion.

Training: 53 bills, 2 enactments. Evaluation: 33 bills, **zero enactments**. Thus this cannot establish ability to identify bills that pass, discrimination, calibration or out-of-period generalization. No model was promoted.

## Evidence and method

- ALFRED UNRATE and CPIAUCSL, 80 source downloads across 40 previous-month-end vintage dates. Returned vintage headers must match the requested date; no future observations or silent imputation accepted.
- Unemployment is the latest available monthly value. Inflation is year-over-year CPI change computed within the same vintage. Latest component observations must be at most 100 days old.
- Economic vintage date strictly precedes each bill cutoff. Historical data versions, not today's revised values, are used. Original release bytes are not independently timestamp-attested.
- Original publication model reproduced to numerical tolerance before comparison. Same L2, iterations, training population and training-only scaling. No feature selection or tuning on evaluation outcomes.
- National economic conditions are shared across bills; these are not 33 independent macro environments.
- The initial v1 acquisition timed out before receiving data or producing scores. v2 changes HTTP transport only; its protocol records the amendment.

## Reproduction

`python3 -m engine.macro_pilot --offline`

Offline reproduction matched `54af68292894b98262b81f7d5b7085622dd2838259048fc6a9329af3696df717`. Raw CSVs, source URLs/retrieval timestamps/hashes, protocol, joined feature rows and full results are retained in `data/cohorts/macro-pilot-v2/`. The original publication study remains unchanged.

Saved in the local app under Research → Saved study reports → Macro context · fixed exploratory comparison. Verify offline reproduction reuses the same report; it does not train another model or count as independent evidence.

Next: prespecify a larger independently evaluated temporal cohort with sufficient naturally occurring enactments and controls for Congress-level changes. Do not tune or promote based on this pilot.
