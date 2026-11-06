# Live agent methods audit — 2026-11-05

Scope: read-only inspection of actual local frozen artifacts and saved comparison manifests. No fit, download, prediction generation, new outcome scoring, certification or promotion. Historical outcome counts below are summaries of already exposed training labels; comparison predictions were read only for membership and cutoff fields. This is an agent review, not independent human/source adjudication.

## Results

The existing `python3 -m scripts.paper_readiness_audit` audit function completed successfully against the local runtime corpus, including frozen model identities, candidate self-hash, final-training hash and saved result hashes. The survivor's separate training-list digest also matches its artifact's `training_hash`.

| Check | Observed result |
| --- | --- |
| Survivor training | 49 rows, 1 positive, Congresses 114 and 116; no duplicate bill or stored family IDs |
| Challenger final training | 11,871 rows, 281 positives; no duplicate bill or stored family IDs |
| Training by Congress | 113: 2,721; 114: 2,185; 115: 2,127; 116: 2,268; 117: 2,570 |
| Core/calibration | 9,496 / 2,375; zero shared bill IDs and zero shared stored family IDs; union exactly equals final training |
| Latest training label | 2023-04-13T23:59:59Z; equals candidate metadata |
| Training checkpoint | Zero departures from introduction + exactly 180 days; zero checkpoints at/after Congress horizon |
| Label boundaries | Zero labels available at/before checkpoint; zero negative-label availability times before horizon; all 281 positive enactment dates strictly between checkpoint day and terminal day |
| Eligible publication versions | 12,749; zero availability or issue timestamps after the associated checkpoint |
| Human introduction review | All 12,749 eligible versions lack a satisfied human introduction-audit flag |
| Actual source observation | All 11,871 BILLSTATUS retrieval timestamps are after their historical checkpoints |
| Survivor versus challenger training | Zero shared bill IDs, but eight shared stored family IDs |
| Saved exposed 118 comparison | 2,315 rows; zero bill-ID or stored-family intersections with either training set; first checkpoint 2023-07-08T23:59:59Z, after latest challenger label |

Sharing families between the two models' training populations is not a train/evaluation violation: the procedures are comparators, not independent replications. Stored family IDs are heuristic graph labels; zero intersections do not certify that all cross-period relationships were discovered.

All four saved chronological folds have zero direct training/evaluation bill-ID overlap and their recorded latest training-label time precedes first evaluation checkpoint:

| Fold | Train / evaluation rows | Latest label → first checkpoint | Evaluation IDs reused in final candidate training |
| --- | --- | --- | --- |
| 114 | 2,302 / 2,788 | 2015-04-19 → 2015-07-05 | 2,185 |
| 115 | 4,462 / 2,717 | 2017-03-25 → 2017-07-02 | 2,127 |
| 116 | 6,591 / 2,792 | 2019-06-12 → 2019-07-02 | 2,268 |
| 117 | 8,812 / 3,059 | 2021-05-08 → 2021-07-03 | 2,570 |

Fold timing here checks saved boundary summaries, not a new full source audit of each historical fold's training set. Reuse in the final candidate is consistent with development followed by final fitting, but those folds cannot serve as independent final validation. The exposed 118 comparison likewise does not become independent because its stored memberships do not intersect training.

## Gate findings and required follow-up

1. `paper_evaluation.prepare` checks evaluation families against model/baseline training, but has no registered exposed-development identity/family manifest. Protocol section 6 additionally excludes evaluation families intersecting exposed development. A reviewed global exposure/family manifest and corresponding gate are required before real readiness can be claimed. This is not currently a scoring bypass: `evaluate` unconditionally rejects prospective scoring after its custodian checks.
2. Survivor legacy rows have no `label_available_at` field. The evidence adapter must require source-supported label-availability review; it must not invent this field from enactment date or transplant challenger metadata.
3. `case` validates aggregate feature availability/effectiveness and a signed-by-name review envelope, not the historical semantics of every publication constituent. `reviewed` checks reviewer text, subject digest and evidence byte hashes, not reviewer qualifications or independent custody. A packet exporter must leave reviews pending and distinguish automated checks from human attestations.
4. Actual retrieval after cutoff is accurately recorded. Historical publication availability bounds do not establish byte-identical historical renditions. Passing date checks is therefore insufficient source certification.
5. A candidate locked in November 2026 cannot turn a 2023 checkpoint replay into prospective issuance. The current work must remain source-review preparation. No certified future census, paired issuance ledger, external timestamp or protected outcome custody exists in this audit.

Do not repair/refit frozen training populations silently if review finds an invalid member. Protocol v1 requires blocking that version and separately freezing a successor study.

## Reproduction

Run from repository root with the existing ignored research corpus. A fresh clone intentionally lacks these runtime files. This command reads only existing artifacts and reports membership/boundary checks; it neither recomputes model scores nor writes runtime artifacts.

```sh
python3 - <<'PY'
import json
from pathlib import Path
from collections import Counter
from datetime import datetime, timedelta
from engine.store import digest, congress_end
from scripts.paper_readiness_audit import audit
b = Path('data/research-runs')
read = lambda p: json.loads((b / p).read_text())
t = read('cross-congress-scale-20261105/final-training.json')
s = read('survivor1000-20261105/training.json')
a = read('survivor1000-20261105/artifact.json')
c = read('convergence-einsum-20261105/candidate-lock.json')
ids = lambda rows: {r['bill_id'] for r in rows}
fam = lambda rows: {r['family_id'] for r in rows}
lookup = {r['bill_id']: r for r in t}
parse = lambda x: datetime.fromisoformat(x.replace('Z', '+00:00'))
print('audit:', audit()['training'])
assert digest(s) == a['training_hash']
assert len(ids(t)) == len(fam(t)) == len(t)
assert len(ids(s)) == len(fam(s)) == len(s)
assert set(c['core_ids']) | set(c['calibration_ids']) == ids(t)
assert not set(c['core_ids']) & set(c['calibration_ids'])
assert not fam([lookup[i] for i in c['core_ids']]) & fam([lookup[i] for i in c['calibration_ids']])
assert c['latest_training_label'] == max(r['label_available_at'] for r in t)
assert all(parse(r['cutoff']) == parse(r['introduced_at']) + timedelta(days=180) for r in t)
assert all(r['cutoff'] < congress_end(r['congress']) for r in t)
assert all(r['label_available_at'] > r['cutoff'] for r in t)
assert all(r['label_available_at'] >= congress_end(r['congress']) for r in t if not r['y'])
assert all(r['cutoff'][:10] < r['law']['enacted'] < congress_end(r['congress'])[:10] for r in t if r['y'])
print('survivor:', len(s), sum(r['y'] for r in s), sorted({r['congress'] for r in s}))
print('training by Congress:', sorted(Counter(r['congress'] for r in t).items()))
print('survivor/final intersections:', len(ids(s) & ids(t)), len(fam(s) & fam(t)))
eligible = [(r, v) for r in t for v in r['versions'] if v['package'] in r['eligible_packages']]
assert all(v['available_at'] <= r['cutoff'] and v['issued_at'] <= r['cutoff'] for r, v in eligible)
print('eligible versions / human review pending:', len(eligible), sum(v.get('introduction_validation', {}).get('human_audit_satisfied') is not True for r, v in eligible))
print('retrieved after cutoff:', sum(r['source']['retrieved_at'] > r['cutoff'] for r in t))
for n in range(114, 118):
    f = read(f'cross-congress-scale-20261105/fold-{n}.json')
    p = f['predictions']
    assert not set(f['training_ids']) & ids(p)
    assert f['latest_training_label'] < f['first_test_checkpoint']
    print('fold:', n, len(f['training_ids']), len(p), f['latest_training_label'], f['first_test_checkpoint'], len(ids(t) & ids(p)))
p = read('cross-congress-confirmation-20261105/result.json')['predictions']
assert max(r['label_available_at'] for r in t) < min(r['cutoff'] for r in p)
print('118:', len(p), min(r['cutoff'] for r in p), len(ids(t) & ids(p)), len(fam(t) & fam(p)), len(ids(s) & ids(p)), len(fam(s) & fam(p)))
PY
```

## Same-batch exposure-gate fix review

The numbered finding 1 above records the pre-fix state. A separate implementing agent subsequently added the exposure-registry gate. Independent inspection of the actual diff confirms that `register` now requires an exposure registry, unique nonempty string entries in its bill/family lists, scope and a review envelope. `prepare` verifies the review subject digest and evidence hashes through the existing review mechanism and rejects selected evaluation bills or stored families intersecting the registered exposure lists. The original finding's missing software gate is addressed.

Validation independently executed: `python3 -m unittest tests.test_paper_evaluation -v` — **16 tests passed**. The added regression test exercises an absent registry, direct identity intersection, family intersection and a changed scope with stale review digest. Existing temporal, source, pairing, replay and real-scoring rejection tests also passed. These are synthetic regression checks, not new real-data evaluation.

Registry completeness, the correctness of family links and the qualifications/independence of reviewers remain unverified. An empty list is structurally permitted (necessary for the synthetic fixture); the code cannot infer that a supplied real exposure registry is complete. A truthy review field at registration is only a preliminary structural requirement: actual subject/source validation occurs in `prepare`. Review attestations remain externally supplied evidence, not automatic human certification. No real exposure registry was certified by this methods audit, and prospective scoring remains blocked.
