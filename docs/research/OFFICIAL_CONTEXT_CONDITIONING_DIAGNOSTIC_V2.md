# Post-failure conditioning diagnostic v2: identity adapter correction

Preserve registered v1 and its failure. V1 failed at zero-based case4972, hr11-117: this source uses legacy billNumber/billType fields while v1's duplicate identity checker expected only modern number/type. The original frozen source audit already supports both schemas. This was an adapter error, not evidence of incorrect source identity. Earlier4972 cases were inspected in memory before failure; no cases/result artifact was persisted. Thus widened outcome-metadata exposure had already begun. Root recorded an immutable failure receipt.

V2 changes only identity validation to reuse the existing frozen official source auditor: exact unique scalar Congress/number/type or billNumber/billType; mixed or duplicate aliases are rejected; whitespace is handled as originally declared; introduction date validation remains strict. The diagnostic then performs precisely v1's own-public-law assertion/feature-exclusion/edition-date cross-tab on the same12,000 saved sources and frozen features. Assertions are not new training labels. Descriptive edition URL/code parsing is not source eligibility certification.

Register v1 registration/failure/code, v2 code/tests/protocol, reused identity-auditor code and all previously declared source/feature/failed-fit bindings before replay. No new network, cohort changes, feature/label/exclusion rule changes, fit or score. V1 remains negative evidence of a diagnostic implementation failure. Any scientific successor requires separate disclosure and review of this adaptive outcome exposure.

```sh
python3 -m unittest tests.test_official_context_conditioning_v2
python3 -m scripts.official_context_conditioning_diagnostic_v2 --output data/research-runs/official-context-conditioning-diagnostic-v2-NEW
```
