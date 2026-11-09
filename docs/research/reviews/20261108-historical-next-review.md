# Historical-source next-route review — 2026-11-08

**Decision: historical eligibility remains unresolved for all eight cases.** A separately bounded Internet Archive CDX metadata lookup returned no indexed successful capture for any of the eight exact current GovInfo XML URLs at or before its cutoff. This does not establish absence of historical copies. No archived bill body, outcome, predictive fit or performance score was acquired.

## Question, selection and scope

Can a third-party web-archive index supply a dated capture lead beyond the already-tested current PREMIS/package ZIP routes? This is a metadata feasibility check on the same eight fixed audit cases, not a representative sample, a new predictive experiment or an amendment to the old source study. Each exact current XML URL and cutoff was copied from the prior sealed audit. The first plan used no replacement cases or URL aliases. The separately sealed alias follow-up below was selected after the first results.

The [Internet Archive CDX documentation](https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md) documents exact URL queries, time bounds, field selection and result limits. Queries requested JSON, exact URL match, capture timestamps through the cutoff, HTTP-200 captures, six metadata fields and at most the first result. An index hit would still require separately bounded archived-byte retrieval, identity checks and independent review; none appeared.

## Pre-request bounds and execution

The plan and script hash were sealed before the first request: eight maximum requests, no retries or redirects, eight-second socket timeout, one-million-byte response budget, no new requests after 120 seconds, stop on the first HTTP/transport/parse error. The socket timeout is not a hard wall-clock deadline. Every request has a sealed prior intent, retained raw response and sealed receipt including URL, timestamps, HTTP status, headers, bytes and digest. The checked query limit is one metadata record, not an archive-body download.

| Metric | Result |
| --- | ---: |
| HTTP successes / attempts | 8/8 |
| JSON responses parsed / attempts | 8/8 |
| Exact URLs returning capture leads / queried URLs | 0/8 |
| Empty index responses / queried URLs | 8/8 |
| Historical eligibility before → after | 0/8 → 0/8 |
| Response bytes retained | 24 |
| HTTP/transport/parse failures | 0 |
| Archived content bodies fetched | 0 |
| Predictive/model/calibration fits | 0 |

## Every case

| Bill | Historical cutoff | HTTP | Response bytes | Returned leads | Decision |
| --- | --- | ---: | ---: | ---: | --- |
| 113-hr3884 | 2014-07-14T23:59:59Z | 200 | 3 | 0 | Unresolved |
| 113-hr4267 | 2014-09-10T23:59:59Z | 200 | 3 | 0 | Unresolved |
| 114-hr2776 | 2015-12-12T23:59:59Z | 200 | 3 | 0 | Unresolved |
| 114-hr2447 | 2015-11-15T23:59:59Z | 200 | 3 | 0 | Unresolved |
| 115-hr4997 | 2018-08-12T23:59:59Z | 200 | 3 | 0 | Unresolved |
| 115-s2712 | 2018-10-16T23:59:59Z | 200 | 3 | 0 | Unresolved |
| 116-s2862 | 2020-05-12T23:59:59Z | 200 | 3 | 0 | Unresolved |
| 116-s843 | 2019-09-10T23:59:59Z | 200 | 3 | 0 | Unresolved |

All responses contain an empty JSON array plus newline and share SHA-256 `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570`. Request-by-request receipt seals and exact query URLs are retained in the result.

## Immutable local evidence and reproduction

- [Pre-request plan](../../../data/research-runs/historical-archive-metadata-v1-20261108/plan.json): `be0326c83b3e29545e051f03218bc3554c7a26725174812cf9f794337782edae`.
- [Full result with every request](../../../data/research-runs/historical-archive-metadata-v1-20261108/result.json): `70cad1d668e4c10de6750d8eeb9396f3b4c4861fc71672031fe758786463d7b7`.
- [Executed lookup script](../../../data/research-runs/historical-archive-metadata-v1-20261108/lookup.py), frozen SHA-256 `99a1a1f3b34ad2d6a9a29dd3f834a1805db440cd14ceda6c3d93ab895742a923`.
- Prior audit raw-file SHA-256: `e7bd7fcd118471f610fbc4dacaf3163e5ca60e14be762bf3968388e1f58b1bd5`.

The executed command was `python3 data/research-runs/historical-archive-metadata-v1-20261108/lookup.py`. The script uses exclusive-create files and deliberately refuses to overwrite an existing plan. Inspect saved artifacts for reproduction; any fresh network run needs a new version and bounded plan rather than reusing or replacing these records. Raw metadata and headers remain ignored runtime artifacts. No automated test suite was introduced for this bounded exploratory script; independent replay should inspect the retained bytes and seals without network calls.

## Limitations and next dependency

The first phase covers exact current GovInfo XML addresses only. It did not search legacy FDsys addresses, bulk-data aliases, Congress.gov renditions or alternate archives; the later FDsys phase is recorded separately below. Canonicalization, archive indexing gaps, access restrictions and missing captures may affect what the public index returns. A zero result is therefore neither proof that no historical copy exists nor a confidence interval for source coverage. This narrow result must not be extrapolated to the corpus.

The prior custody packet remains a concrete route to the missing old-object bytes/digests and public-access records. It is local and unsent. No external contact was made. Broader alias work, if pursued, should first derive exact historical addresses from authoritative records and freeze a finite acquisition plan; speculative endpoint expansion is not evidence of progress toward predictive validity. Prospective capture can create future dated inputs, but cannot backdate eligibility or immediately yield matured predictive evaluation.

No existing registered source status, preprocessing implementation, model or protocol was modified. This is a negative retrieval-lead result, not a negative model result. Independent review is recorded separately by the next-gate audit agent.

## Separately bounded FDsys-alias follow-up

The current-host limitation prompted a separately sealed follow-up before any alias requests. [GovInfo’s official transition reference](https://www.govinfo.gov/about/index.html) supplies old FDsys and new GovInfo package-path examples; the [GPO developer transition guide](https://github.com/usgpo/api/wiki/Transition-Guide) explains the two interfaces share a repository. We inferred predecessor XML addresses by replacing the current content-package prefix with `http://www.gpo.gov/fdsys/pkg/` and retaining the exact package/XML suffix. This is a documented-pattern inference, not case-specific proof those URLs were served. GovInfo began in February 2016, making predecessor coverage particularly relevant to earlier cutoffs.

Same eight cases, same cutoffs, eight maximum requests, zero retries/redirects, same response/time/stopping bounds. No bulk alias, alternative archive, extra bill or content body was added. All eight queries again returned HTTP 200 with empty JSON arrays, three bytes each. There were no retrieval/parse failures and no historical-eligibility changes.

| Bill | Inferred FDsys target | HTTP | Leads |
| --- | --- | ---: | ---: |
| 113-hr3884 | `http://www.gpo.gov/fdsys/pkg/BILLS-113hr3884ih/xml/BILLS-113hr3884ih.xml` | 200 | 0 |
| 113-hr4267 | `http://www.gpo.gov/fdsys/pkg/BILLS-113hr4267ih/xml/BILLS-113hr4267ih.xml` | 200 | 0 |
| 114-hr2776 | `http://www.gpo.gov/fdsys/pkg/BILLS-114hr2776ih/xml/BILLS-114hr2776ih.xml` | 200 | 0 |
| 114-hr2447 | `http://www.gpo.gov/fdsys/pkg/BILLS-114hr2447ih/xml/BILLS-114hr2447ih.xml` | 200 | 0 |
| 115-hr4997 | `http://www.gpo.gov/fdsys/pkg/BILLS-115hr4997ih/xml/BILLS-115hr4997ih.xml` | 200 | 0 |
| 115-s2712 | `http://www.gpo.gov/fdsys/pkg/BILLS-115s2712is/xml/BILLS-115s2712is.xml` | 200 | 0 |
| 116-s2862 | `http://www.gpo.gov/fdsys/pkg/BILLS-116s2862is/xml/BILLS-116s2862is.xml` | 200 | 0 |
| 116-s843 | `http://www.gpo.gov/fdsys/pkg/BILLS-116s843is/xml/BILLS-116s843is.xml` | 200 | 0 |

- [Alias pre-request plan](../../../data/research-runs/historical-archive-alias-metadata-v1-20261108/plan.json): `56ec2966a47c2585e87a559f17e6b7ac960cda0b9d2adba79d14d9cfc85f68d5`.
- [Alias full result](../../../data/research-runs/historical-archive-alias-metadata-v1-20261108/result.json): `8d14f381d6ad6bf7f13cc430457c9d84316b46dacaf40d678c67a29aa07f434d`.
- [Alias executed script](../../../data/research-runs/historical-archive-alias-metadata-v1-20261108/lookup.py), frozen SHA-256 `78f1e503fdd4ab6fe628f744a99a66fe850ddec0b3abb0cc9d982ae08abc0418`.

Executed command: `python3 data/research-runs/historical-archive-alias-metadata-v1-20261108/lookup.py`. Each immutable result retains exact query strings, timestamps, headers and receipt seals. Both lookups combined made 16 requests, all HTTP 200, with 48 response bytes and zero returned capture leads. These are 16 URL queries across eight identities, not 16 independent bills. Response-body hash is the same empty-array hash given above.

The remaining limitation is broader than these two URL forms: index gaps, alternate bulk/Congress.gov addresses, other archives and restricted or unindexed preservation records remain possible. No route exhaustion beyond these particular queries is claimed. Historical eligibility stays 0/8 before and after both lookups. Independent audit also notes that the ad hoc runner relies on the frozen eight-record input rather than enforcing an explicit loop-count cap; observed executions complied with eight requests each. It must not be generalized to arbitrary inputs without a new reviewed implementation.
