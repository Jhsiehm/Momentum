# Source-based review of candidate misses and suggestions

Date: 2026-11-08. This batch reviews the previous design-only extractor output, without modifying the extractor, its results or the corrected reference dataset. It also follows the documented public archival access routes. No protected quality evaluation or predictive experiment is claimed.

## Population and primary review

The packet deterministically contains every one of the 102 reference effect quotations lacking a same-mechanism trigger intersection, plus all five narrow suggestions. These span 34 of the forty design bills. The six other bills contribute no targeted review items; this is targeted error analysis, not a representative accuracy sample.

Two agents read the complete bound views for their assigned seventeen bills each, totaling 326,914 supplied characters. Agent A reviewed 52 misses and two suggestions; agent B reviewed 50 misses and three suggestions. Each disposition includes a rationale and exact source offsets, and each primary review is separately sealed. These are provisional agent judgments, not human reference certification.

| Primary miss diagnosis | Count |
| --- | ---: |
| Vocabulary gap | 49 |
| Implicit legal effect | 41 |
| Scope or quotation issue | 11 |
| Reference-label question | 1 |
| Total | 102 |

All five proposals were supported **as unvalidated suggestions** by their primary reviewer. Five selected simple clauses cannot establish extractor precision. The forty-bill extractor still emits 480 abstentions and zero accepted labels.

The distinction matters for the next implementation. Some direct constructions are missing from locator vocabulary: actor-specific “No … may” bars, conditional “only” limitations, information duties expressed as filing or furnishing, and recurring windows expressed as “on an annual basis.” Such phrases remain candidates requiring context, not automatic positive labels. Other effects derive from amendment instructions, rights preservation, an inherited mandatory lead-in or referenced law. Expanding a keyword list cannot settle these legal meanings.

Eleven primary scope findings identify quotations that omit governing parent clauses, amendment instructions or framework context. The source reading view still retains that context; the diagnostic's narrow quotation intersection can miss it. A future representation should bind multiple relevant spans with their structural relation instead of treating a detached list item as a self-contained effect.

The reference question concerns effect 37 in `117-hr1597`: the text imposes a duty to extend a plan/permit, while the provisional `require/expand` direction may confuse extension of the instrument with expansion of a preexisting duty. The reviewer requests consideration of `create` or uncertain direction. B’s primary rationales flag four deadline effects currently using `procedure` rather than `duration`: `114-s1259:15`, `115-s284:4`, `117-s825:6`, and `117-hr5229:16` (zero-based effect indices). A later self-audit identifies the same dimension concern in `116-s1076:9`, `116-s1076:13`, and `116-s1076:22`; these three supplemental findings were omitted from A’s primary rationale and are preserved separately. They are not additional independent errors or changes to the 102 primary diagnoses. These are proposed corrections requiring separate adjudication; no original annotation was overwritten.

## Reciprocal review and validation

Every one of the 107 primary items received a source-based reciprocal review. Both peers agreed with the diagnostic dispositions while preserving the reference questions. B reread all seventeen A views; A checked every B finding with surrounding source context and does not claim a fresh full-text reread of every B bill. These reviews are not blind, do not establish inter-rater reliability, and do not turn agreement into semantic accuracy.

Peer A receipt: `bb024a3a565d22fb064efdb7a7554bcabce0b536570ce633931c1d7c2e5a8092`. Peer B receipt: `0764236598a9ac6cb956e7a832b55901f794e0d35f3d78757bd8ff61a79a2776`. Complete integrity result: `c1ac17a3890c71e0334e9ad5efb8a5e095c3f1ab947f1d1e36dcebac5cf719b6`, reproduced normally and under Python optimization. Forty focused tests passed; no full-suite result is claimed.

All 120 inventoried prior extractor, annotation and source-view files remained unchanged, as did the frozen-model audit. Preservation receipt: `0396a4eb13544e29e506db7592f1f30ff176b9676a144ac9c3e717dc0ebf2b52`. Protected quality texts were not parsed, and there were no model fits, outcome scoring, accepted labels, promotion or scheduler changes.

## Integrity and reproducibility

`scripts/mechanism_candidate_review_audit.py` recreates the packet from the sealed forty-bill outputs and fixed corrected reference hash. It checks complete bill/item coverage, exact evidence text and offsets, packet and peer-review bindings, mechanism identity and false certification flags. Independent methods review caught a Python Boolean-versus-integer identity edge case; explicit type checks and a regression test now reject it. Contradictory optional source-view hashes are rejected too. Quote matching checks source integrity, not interpretive correctness.

```sh
python3 -m scripts.mechanism_candidate_review_audit --directory data/research-runs/mechanism-candidate-review-20261108-v1 --prepare
python3 -m scripts.mechanism_candidate_review_audit --directory data/research-runs/mechanism-candidate-review-20261108-v1
```

Packet hash: `6c7e9ffc63a6b7b6df8af9cf14e27a433cfc3f71afe9a3f719e28cc78290408b`. Agent A primary: `71b4c0904c1ddfa4ea13d5b32ea4ed33f4c99cd9bc493a380f9ddee8a626623e`. Agent B primary: `ec9a38ddcd888007e45eeaf2b991e7a18ff54cfa74647074e7de9f3a1c3ffaee`. Runtime review records remain ignored under `data/research-runs/mechanism-candidate-review-20261108-v1/`.

Supplemental self-review receipt: `5a3566a0704d020d5380b7b0b572f4e377218493584d3ef86e8dcf19f35bb59b`. Root verified all three evidence spans and primary binding; B independently checked and agreed with these questions. Supplement verification: `264ffa58cc37fa52a155a55593b36ba81ba2cc4eb00242f32ffca92cc419aebc`. The original primary/peer receipts remain unchanged. Shared research lease released.

## Historical-source investigation

The [follow-up report](../../research/reviews/20261108-historical-text-resolution-v2.md) preserves six actual official HTTP responses, including architecture documents, an API summary and the public ZIP for previously audited `113-hr3884`. The ZIP contains one current bill XML plus public formats and metadata; it does not contain the older XML objects. The architecture distinguishes authorized archival export from public access packages and independently maintained renditions. The tested public routes establish **zero of eight historical identities**; this is not proof that archival export is impossible.

Root independently verified all eleven receipt-file hashes, the ZIP's six entries and its bill XML checksum. Resolution receipt: `6f0a45f3cdafe6ca70202aa6790539ffd2dc796f432a717a7cbe6d2c26509976`; root verification: `71b62330cd28c3145c3410a1b15c37c6984a5d6340704c121ec83813935ed681`. No private credential, external message or archival-access authorization was used.

## Consequence for experiments

The next implementation should separately version context-span support and adjudicated reference corrections before expanding candidate rules. A graph of compatible semantic effects still needs explicit reviewed judgments; lexical overlap cannot supply it. Historical model testing still needs actual pre-cutoff source evidence or a separately designed prospective study. Neither this error analysis nor agreement between agents demonstrates the requested 60% predictive improvement or self-learning.
