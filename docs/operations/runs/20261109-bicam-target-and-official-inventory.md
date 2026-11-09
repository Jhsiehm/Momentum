# Target inventory, official coverage and source transition — 9 November 2026

## Outcome and decisions

The separately registered offline BICAM target audit v3 applied five independently reviewed metadata sidecars and retained 38 outside-target missing-Congress records in quarantine. It did not release a sample: 116 further schema/date issues remain. This is a recorded negative result, not a revised success criterion.

A separate official GovInfo directory acquisition produced 75,605 exact XML identities. An offline comparison found 75,592 matching identities, 13 official-only and 30 accepted-candidate-only identities. The next source-readiness sample moves to the official directory in a new registration; it does not turn the failed BICAM sample into a success. No model fitting, scoring or historical-availability certification occurred.

Question: can the target archive population be internally validated after evidence-backed enrichment, and how does it compare with current official file enumeration? This is source readiness and coverage diagnostics, not a predictive experiment or comparison to an accuracy baseline.

## Fixed rules, versions and exposure

Target: Congresses113–118, H.R./S. Original bill bytes, reversible title-dialect assumptions and five-case reconciliation hash pinned. Scope validation precedes quarantine. No inferred dates, silent missing rows or outcome-based exclusions. Target dates must be within the conservative Congress interval; sample would be first100 by SHA-256 of version, newline and canonical ID only on an error-free population. The existing v1 date-only/midnight forms were retained after root preflight caught an unnecessarily narrower draft. That change preceded registration. Seventeen author/independent tests passed normally and optimized before v3 execution.

Five reviewed repairs are retained, not rewritten into raw data. All five have introduction+180 days after Congress end; they cannot enter the day180 forecasting cohort. Calendar window is descriptive, not full at-risk eligibility. No action/outcome status or source availability is implied.

The prior five-case source investigation incidentally exposed procedural outcomes; those five remain design-exposed. This audit reads identity/date projections and reference definitions, not outcome fields. Any later sample is for source readiness, not untouched confirmatory evaluation.

## Exact source partition

| Disposition | Rows |
|---|---:|
| Logical source records under declared CSV dialect | 414,277 |
| Accepted target candidate rows | 75,622 |
| Valid outside-target identities | 338,501 |
| Outside-target missing-Congress quarantine | 38 |
| Error rows | 116 |
| Applied reviewed repairs within accepted target rows | 5 |
| Reversible title CR offsets | 99 |
| Candidate sample released | 0 / 100 |

The 116 errors comprise97 missing target introduction dates, five dates equal to the Congress-end boundary, and14 unsupported identities. The latter include eight historical half-number IDs, five zero-number IDs and one historical document type. Unsupported syntax is not proof that the underlying historical legislation is erroneous. The five boundary cases are H.R.9705–9709 in Congress117, dated January3,2023; source membership is independently present in the official directory. Day-precision data cannot resolve intraday Congress boundaries. Do not silently change the dates.

Among75,622 accepted target rows,63,897 reach day180 strictly before Congress end and11,725 do not. These are not final eligible training counts. Source/historical, at-risk, family, label, review and class coverage remain separate.

Version reference parsed independently of failed sampling:54 rows, including IH=Introduced(House) and IS=Introduced(Senate). This confirms mapping semantics only; it does not establish joined introduced text for a case.

## Official acquisition and separate offline correction

Exactly12 current directory HTML requests: Congresses113–118 crossed with hr/s at `https://www.govinfo.gov/bulkdata/BILLSTATUS/{congress}/{type}`. All HTTP200,35,211,033 body bytes, no cap or transport failure. Each response capped at5,000,000 bytes plus one sentinel; socket timeout20seconds, zero redirects/retries, no hard total deadline. No bill XML or texts fetched by this phase. ExactURL/code/protocol/test identities registered before requests.

Initial directory parser v1 marked all indexes unaccepted because each included its standard ZIP-download resource. It still extracted exact XML IDs. A separately registered offline v2 recognizes only the exact same-directory ZIP as a non-XML resource. All12 indexes then passed the declared syntactic checks, with identical XML identity sets and no new requests. Neither acceptance nor lack of pagination certifies all introduced bills or historical availability. Preserve the initial negative result.

## Per-Congress/type comparison

| Congress | Type | Accepted BICAM candidates | Official current IDs | Intersection | Candidate only | Official only |
|---:|---|---:|---:|---:|---:|---:|
| 113 | hr | 5893 | 5885 | 5885 | 8 | 0 |
| 113 | s | 3020 | 3020 | 3020 | 0 | 0 |
| 114 | hr | 6536 | 6526 | 6526 | 10 | 0 |
| 114 | s | 3548 | 3548 | 3548 | 0 | 0 |
| 115 | hr | 7401 | 7394 | 7394 | 7 | 0 |
| 115 | s | 3805 | 3805 | 3805 | 0 | 0 |
| 116 | hr | 9067 | 9062 | 9062 | 5 | 0 |
| 116 | s | 5086 | 5086 | 5086 | 0 | 0 |
| 117 | hr | 9704 | 9709 | 9704 | 0 | 5 |
| 117 | s | 5357 | 5357 | 5357 | 0 | 0 |
| 118 | hr | 10559 | 10564 | 10559 | 0 | 5 |
| 118 | s | 5646 | 5649 | 5646 | 0 | 3 |

Both sides are qualified sets: BICAM candidates exclude the explicitly reported116 errors; official identities describe today's directory presence. Absence does not imply non-introduction, reserved number, repeal or a negative label. The13 official-only cases include five BICAM boundary-error cases and eight other identities absent from its accepted candidate projection. The30 candidate-only cases are lower-numbered House identities; their actual status has not been adjudicated.

### Every set difference

| Direction | IDs |
|---|---|
| Official only | hr10559-118, hr10560-118, hr10561-118, hr10563-118, hr10564-118, hr9705-117, hr9706-117, hr9707-117, hr9708-117, hr9709-117, s5595-118, s5639-118, s5649-118 |
| Candidate only | hr1-114, hr10-116, hr11-114, hr11-115, hr13-113, hr13-114, hr13-115, hr14-113, hr14-114, hr14-115, hr15-114, hr15-116, hr16-113, hr16-114, hr16-115, hr16-116, hr17-113, hr17-114, hr17-115, hr17-116, hr18-113, hr18-114, hr18-115, hr18-116, hr19-113, hr19-114, hr4-114, hr8-113, hr9-113, hr9-115 |

### Every error case

Five canonical target error IDs are present in the official directory;97 are absent, and14 unsupported IDs are not assigned a canonical membership verdict.

| CSV row | ID | Issue | Original Congress | Original introduction | Official membership |
|---:|---|---|---|---|---|
| 1957 | hr9706-117 | invalid_target_introduction | 117.0 | 2023-01-03 | True |
| 60992 | hr9708-117 | invalid_target_introduction | 117.0 | 2023-01-03 | True |
| 126903 | hr9707-117 | invalid_target_introduction | 117.0 | 2023-01-03 | True |
| 160011 | hr9705-117 | invalid_target_introduction | 117.0 | 2023-01-03 | True |
| 160012 | hr9709-117 | invalid_target_introduction | 117.0 | 2023-01-03 | True |
| 183246 | s3932-113 | invalid_target_introduction | 113 | (blank) | False |
| 202343 | hr7103-114 | invalid_target_introduction | 114.0 | (blank) | False |
| 202471 | s3414-113 | invalid_target_introduction | 113.0 | (blank) | False |
| 205934 | hr11200-113 | invalid_target_introduction | 113.0 | (blank) | False |
| 206261 | hr0-113 | invalid_identity | 113.0 | (blank) | None |
| 207089 | hr1025½-41 | invalid_identity | 41.0 | 1870-01-31 | None |
| 209143 | s5005-115 | invalid_target_introduction | 115.0 | (blank) | False |
| 215183 | sres0-106 | invalid_identity | 106 | (blank) | None |
| 216754 | hr6091-113 | invalid_target_introduction | 113 | (blank) | False |
| 217633 | s3322-113 | invalid_target_introduction | 113 | (blank) | False |
| 218129 | s5307-116 | invalid_target_introduction | 116 | (blank) | False |
| 218488 | s3378-113 | invalid_target_introduction | 113 | (blank) | False |
| 218840 | hr8693-113 | invalid_target_introduction | 113 | (blank) | False |
| 219289 | hr13500-118 | invalid_target_introduction | 118 | (blank) | False |
| 221615 | s3679-113 | invalid_target_introduction | 113 | (blank) | False |
| 222066 | s260½-30 | invalid_identity | 30 | 1848-04-13 | None |
| 222749 | s3235-113 | invalid_target_introduction | 113 | (blank) | False |
| 223256 | s4038-113 | invalid_target_introduction | 113 | (blank) | False |
| 223364 | hr6089-113 | invalid_target_introduction | 113 | (blank) | False |
| 223822 | hr11618-113 | invalid_target_introduction | 113 | (blank) | False |
| 226089 | s3209-113 | invalid_target_introduction | 113 | (blank) | False |
| 227545 | hr1382½-40 | invalid_identity | 40 | 1868-07-11 | None |
| 230550 | s3385-113 | invalid_target_introduction | 113 | (blank) | False |
| 230847 | hr189½-42 | invalid_identity | 42 | 1871-03-20 | None |
| 234260 | s3290-113 | invalid_target_introduction | 113 | (blank) | False |
| 234810 | s3210-113 | invalid_target_introduction | 113 | (blank) | False |
| 236855 | s3562-113 | invalid_target_introduction | 113 | (blank) | False |
| 237024 | hr10575-117 | invalid_target_introduction | 117 | (blank) | False |
| 238056 | s4047-114 | invalid_target_introduction | 114 | (blank) | False |
| 238606 | hr5914-113 | invalid_target_introduction | 113 | (blank) | False |
| 238665 | s6251-113 | invalid_target_introduction | 113 | (blank) | False |
| 241475 | s3512-113 | invalid_target_introduction | 113 | (blank) | False |
| 242865 | hr6072-113 | invalid_target_introduction | 113 | (blank) | False |
| 243368 | hr6225-113 | invalid_target_introduction | 113 | (blank) | False |
| 245340 | hr6482-113 | invalid_target_introduction | 113 | (blank) | False |
| 246289 | s53019-116 | invalid_target_introduction | 116 | (blank) | False |
| 248466 | s3036-113 | invalid_target_introduction | 113 | (blank) | False |
| 249318 | hr7902-115 | invalid_target_introduction | 115 | (blank) | False |
| 251810 | hr14½-38 | invalid_identity | 38 | 1863-12-22 | None |
| 254567 | s0-115 | invalid_identity | 115 | (blank) | None |
| 258202 | s3349-113 | invalid_target_introduction | 113 | (blank) | False |
| 259592 | s3310-113 | invalid_target_introduction | 113 | (blank) | False |
| 259847 | hr11159-115 | invalid_target_introduction | 115 | (blank) | False |
| 260489 | hr41172-114 | invalid_target_introduction | 114 | (blank) | False |
| 260498 | hr6529-113 | invalid_target_introduction | 113 | (blank) | False |
| 260768 | hr15316-113 | invalid_target_introduction | 113 | (blank) | False |
| 262741 | hr6684-113 | invalid_target_introduction | 113 | (blank) | False |
| 263127 | s5339-116 | invalid_target_introduction | 116 | (blank) | False |
| 263857 | hr6350-113 | invalid_target_introduction | 113 | (blank) | False |
| 265075 | hr13781-113 | invalid_target_introduction | 113 | (blank) | False |
| 270073 | hr6138-113 | invalid_target_introduction | 113 | (blank) | False |
| 271354 | hr13270-115 | invalid_target_introduction | 115 | (blank) | False |
| 271702 | s3040-113 | invalid_target_introduction | 113 | (blank) | False |
| 273666 | s3309-113 | invalid_target_introduction | 113 | (blank) | False |
| 275779 | hr6564-113 | invalid_target_introduction | 113 | (blank) | False |
| 276158 | hr6061-113 | invalid_target_introduction | 113 | (blank) | False |
| 280961 | hr7045-114 | invalid_target_introduction | 114 | (blank) | False |
| 284004 | s5137-116 | invalid_target_introduction | 116 | (blank) | False |
| 285297 | hr12259-114 | invalid_target_introduction | 114 | (blank) | False |
| 290488 | s3469-113 | invalid_target_introduction | 113 | (blank) | False |
| 291357 | s3706-113 | invalid_target_introduction | 113 | (blank) | False |
| 291578 | hr11630-114 | invalid_target_introduction | 114 | (blank) | False |
| 297295 | hr6915-113 | invalid_target_introduction | 113 | (blank) | False |
| 298786 | s3057-113 | invalid_target_introduction | 113 | (blank) | False |
| 303081 | hr5987-113 | invalid_target_introduction | 113 | (blank) | False |
| 303764 | s3157-113 | invalid_target_introduction | 113 | (blank) | False |
| 305129 | s3202-113 | invalid_target_introduction | 113 | (blank) | False |
| 309278 | hr742½-41 | invalid_identity | 41 | 1870-01-10 | None |
| 312386 | hr13773-114 | invalid_target_introduction | 114 | (blank) | False |
| 312865 | s15737-118 | invalid_target_introduction | 118 | (blank) | False |
| 313624 | s6193-116 | invalid_target_introduction | 116 | (blank) | False |
| 315107 | hr590½-42 | invalid_identity | 42 | 1871-12-11 | None |
| 317794 | hr15787-113 | invalid_target_introduction | 113 | (blank) | False |
| 318151 | s6160-117 | invalid_target_introduction | 117 | (blank) | False |
| 319009 | s3217-113 | invalid_target_introduction | 113 | (blank) | False |
| 319783 | hr7045-113 | invalid_target_introduction | 113 | (blank) | False |
| 320201 | s3730-113 | invalid_target_introduction | 113 | (blank) | False |
| 326904 | hr6043-113 | invalid_target_introduction | 113 | (blank) | False |
| 327687 | s5488-113 | invalid_target_introduction | 113 | (blank) | False |
| 329232 | hr6390-113 | invalid_target_introduction | 113 | (blank) | False |
| 333576 | s3464-113 | invalid_target_introduction | 113 | (blank) | False |
| 341428 | s6017-113 | invalid_target_introduction | 113 | (blank) | False |
| 343294 | s3752-113 | invalid_target_introduction | 113 | (blank) | False |
| 348331 | hr5979-113 | invalid_target_introduction | 113 | (blank) | False |
| 349946 | s3158-113 | invalid_target_introduction | 113 | (blank) | False |
| 355294 | hr14357-113 | invalid_target_introduction | 113 | (blank) | False |
| 358345 | hr6408-113 | invalid_target_introduction | 113 | (blank) | False |
| 364437 | hr6082-113 | invalid_target_introduction | 113 | (blank) | False |
| 364847 | hr260½-30 | invalid_identity | 30 | 1848-02-29 | None |
| 366099 | hr13733-114 | invalid_target_introduction | 114 | (blank) | False |
| 366425 | s4079-115 | invalid_target_introduction | 115 | (blank) | False |
| 368170 | hr6141-113 | invalid_target_introduction | 113 | (blank) | False |
| 372728 | hr6469-113 | invalid_target_introduction | 113 | (blank) | False |
| 376678 | s3254-113 | invalid_target_introduction | 113 | (blank) | False |
| 376923 | hr7902-113 | invalid_target_introduction | 113 | (blank) | False |
| 377877 | s10994-115 | invalid_target_introduction | 115 | (blank) | False |
| 378094 | cen_doc_h4-8 | invalid_identity | 8 | (blank) | None |
| 382896 | hr10923-113 | invalid_target_introduction | 113 | (blank) | False |
| 383404 | hr6096-113 | invalid_target_introduction | 113 | (blank) | False |
| 384675 | hr0-116 | invalid_identity | 116 | (blank) | None |
| 385620 | hr6365-113 | invalid_target_introduction | 113 | (blank) | False |
| 387649 | s5481-113 | invalid_target_introduction | 113 | (blank) | False |
| 388443 | hr6007-113 | invalid_target_introduction | 113 | (blank) | False |
| 391547 | s6406-115 | invalid_target_introduction | 115 | (blank) | False |
| 392417 | hr6431-113 | invalid_target_introduction | 113 | (blank) | False |
| 396380 | hr11200-117 | invalid_target_introduction | 117 | (blank) | False |
| 397808 | hr6375-113 | invalid_target_introduction | 113 | (blank) | False |
| 402066 | s7066-117 | invalid_target_introduction | 117 | (blank) | False |
| 403184 | s5718-113 | invalid_target_introduction | 113 | (blank) | False |
| 403598 | hr0-110 | invalid_identity | 110 | (blank) | None |
| 411103 | hr6249-113 | invalid_target_introduction | 113 | (blank) | False |

### Every quarantine case

Identifier-derived outside-target status only; original Congress is blank.

| CSV row | ID | Original introduction |
|---:|---|---|
| 1154 | sres350-116 | (blank) |
| 2833 | sres259-103 | (blank) |
| 4715 | s2650-103 | (blank) |
| 22084 | sres742-116 | (blank) |
| 32124 | hconres134-118 | (blank) |
| 35600 | sres5-103 | (blank) |
| 40504 | sres897-118 | (blank) |
| 40505 | sres902-118 | (blank) |
| 40508 | sres924-118 | (blank) |
| 42091 | hres1611-118 | (blank) |
| 49317 | hres477-107 | (blank) |
| 63047 | sres913-118 | (blank) |
| 71753 | sres915-118 | (blank) |
| 82932 | sjres117-118 | (blank) |
| 83004 | sres905-118 | (blank) |
| 83005 | sres906-118 | (blank) |
| 85340 | sres4-103 | (blank) |
| 90701 | sres528-112 | (blank) |
| 91663 | hres351-106 | (blank) |
| 101002 | sres900-118 | (blank) |
| 102622 | sres925-118 | (blank) |
| 108660 | s2452-103 | (blank) |
| 109760 | sres514-113 | (blank) |
| 109761 | sres515-113 | (blank) |
| 113376 | sres6-103 | (blank) |
| 115427 | sres904-118 | (blank) |
| 117145 | sres261-103 | (blank) |
| 120994 | sres256-107 | (blank) |
| 123128 | sres260-103 | (blank) |
| 128579 | sres907-118 | (blank) |
| 131125 | sres499-111 | (blank) |
| 132730 | sres68-105 | (blank) |
| 160885 | hres1585-118 | (blank) |
| 163033 | sres899-118 | (blank) |
| 193400 | sres926-118 | (blank) |
| 194544 | sres448-116 | (blank) |
| 196435 | sres892-118 | (blank) |
| 196436 | sres921-118 | (blank) |

## Validation, limits and continuation

Root reran all30 new tests normally and optimized: passed. Independent replay checked all414,277 logical source records, exact errors/quarantine/repairs, calendar flags and54 reference rows. A separate HTML parser reproduced all75,605 official identities and the unchanged XML sets across directory parser versions. The offline set comparison preserves all errors, rather than treating the accepted-candidate set as complete.

No confidence interval or predictive metric is applicable: these are exact counts of the acquired snapshot. No model promotion, 60% improvement, validated forecast, class sufficiency or original historical-byte proof is claimed.

Continue through a separately registered100-case official-directory source-readiness audit, fixed before inspecting its bill XML, with no replacement cases. That is a deliberate adaptive source change after the observed failures. It must retain source/exposure limits and cannot retroactively validate BICAM v3. Other possible repairs and mismatches remain visible for later scoped adjudication.

## Reproduction and evidence

Protocols: [target v3](../../research/BICAM_INVENTORY_TARGET_V3.md), [official directory v1](../../research/BICAM_OFFICIAL_INVENTORY_V1.md), [offline directory v2](../../research/BICAM_OFFICIAL_INVENTORY_OFFLINE_V2.md), [set comparison](../../research/BICAM_INVENTORY_COMPARE_V1.md).

[Target independent review](../../research/reviews/20261109-bicam-target-inventory-v3-review.md). Raw data remains ignored. Reproduction commands are in each frozen protocol; use existing offline inputs and fresh output directories, never overwrite registrations. Root tests: `python3 -m unittest tests.test_bicam_inventory_target_v3 tests.test_bicam_target_independent tests.test_bicam_official_inventory_v1 tests.test_bicam_official_inventory_offline_v2 tests.test_bicam_inventory_compare_v1`, repeated with `python3 -O`.

| Artifact under data/research-runs | SHA-256 |
|---|---|
| bicam-inventory-target-v3-20261109/applied-repairs.json | `7494c25aa6f1ad6420bf8feabb4402fbf614a5e85b543df5dc51fffabf24fa58` |
| bicam-inventory-target-v3-20261109/errors.json | `c85a1035309f147be3008b3dc0bbcbf9c68bf9a77fd06bce663d83633e2d95ce` |
| bicam-inventory-target-v3-20261109/identity-census.json | `4fb153bd9de84ae4de637a2de6b41b4f13577580938aff441107638541eebbc5` |
| bicam-inventory-target-v3-20261109/independent-review.json | `4ad60ab45b746d10755e1a8c8fd8fa7daafce49a96e77711ffd5ee9801240097` |
| bicam-inventory-target-v3-20261109/quarantine.json | `00b079731d3059a36a8ed4db07cb85c17b22de2d77df898fb329fffed510bb58` |
| bicam-inventory-target-v3-20261109/registration.json | `09a2280f60a3ae3d3b04a700604e6ae934fed66ff0f47f4cbdd39219dc418750` |
| bicam-inventory-target-v3-20261109/result.json | `df52b9e2b077aae94539d0bb2fa8bb81d5d80aaa818e87a90596a7367b5f636c` |
| bicam-inventory-target-v3-20261109/sample.json | `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` |
| bicam-inventory-target-v3-20261109/title-cr-offsets.json | `3f8745ff673110e43cf38cc26dd03e6582db8af316d35df0bee05b9cef5f4989` |
| bicam-inventory-target-v3-20261109/version-reference.json | `556b0f9673db3107487c519512daab4b344ed162ddeb0281e3b5fc38466079cd` |
| bicam-official-inventory-v1-20261109/113-hr-receipt.json | `f717198992223fce0bc48dc09ce88f35c44fb8d87441249c66f7f918a0564233` |
| bicam-official-inventory-v1-20261109/113-s-receipt.json | `8583291ac9c49da8ab57c63a44aa8bdecf140751cd743a6ca0a749f10fb0585d` |
| bicam-official-inventory-v1-20261109/114-hr-receipt.json | `af56a86fd66022ded6e7402bf7ccc98a2eb3a6c243cd36bcfa645fdee95652df` |
| bicam-official-inventory-v1-20261109/114-s-receipt.json | `160882aadef6e61ddd4238e768facdca0e868b3aeb4bc13f35c4317572f4a7a2` |
| bicam-official-inventory-v1-20261109/115-hr-receipt.json | `784943e7d24e4e584ae5eff7847071fbe71a7b0118972cf0496c027155baa2d0` |
| bicam-official-inventory-v1-20261109/115-s-receipt.json | `32e156ead56f9631fa5e6168ed1476029eeb69b8cd4bb7a95cf59d3c513750fe` |
| bicam-official-inventory-v1-20261109/116-hr-receipt.json | `ba3157eb30ee1e42c8d88e5c2c269337af823f216ee5907b97e35b627292968d` |
| bicam-official-inventory-v1-20261109/116-s-receipt.json | `d6c8c79eb5eb6d596735d543cb622570b91338864611b496a000a0851b81fe0f` |
| bicam-official-inventory-v1-20261109/117-hr-receipt.json | `d599798c6f89429af4359dfda88fa6f7a3329fb213ddebe937a5fe363bc24e7c` |
| bicam-official-inventory-v1-20261109/117-s-receipt.json | `e5c736fa71040bf1f8eb18f5205047618c0d6e48b9faaed5e9de106ae2315fd2` |
| bicam-official-inventory-v1-20261109/118-hr-receipt.json | `a1adcd1739a2317a5d43e206c1af367fe9c00265d95dab20af39dfc250e81024` |
| bicam-official-inventory-v1-20261109/118-s-receipt.json | `1e869907c57ca1152c3107dfdaadaa9010358e547458517b365952455608ca6b` |
| bicam-official-inventory-v1-20261109/registration.json | `86c23b0d77890c9f0ba9efd4e371cde48b4f7b68db66f803be029dd8d3d21b89` |
| bicam-official-inventory-v1-20261109/result.json | `1beaa6942a2179aff7f77c84c1f11b72bdeb50b6885dce53127d9595fd864dd9` |
| bicam-official-inventory-offline-v2-20261109/independent-review.json | `89411324a54fa306482a4ceb6b38d0a5be38d953bd8ab956d8d3cdc6b59a6b08` |
| bicam-official-inventory-offline-v2-20261109/registration.json | `4790159c39f1cd1389292a51899c222553680113b0586d8d268c02ba71c81823` |
| bicam-official-inventory-offline-v2-20261109/result.json | `242240ae0b11f89cbcfa8b14459f18deb454d70742052a86d5da9b3ec8e6e681` |
| bicam-inventory-compare-v1-20261109/independent-review.json | `445e4c626966d417b3f26b8cce6a607c4f9a82e2162ca253bf7d3b9d201cf893` |
| bicam-inventory-compare-v1-20261109/registration.json | `24ee980df911cf9e2cbebfda8c1f8c6a75a7dfccf704bce56ac450546ca3cdd2` |
| bicam-inventory-compare-v1-20261109/result.json | `34896006dca80724b948f3e77c8ad71a923371703b5ddc31111806eb4d474f8b` |

Root preservation check: all98 prior artifacts and frozen-model audit unchanged. No full-suite rerun for this source-only batch;30 new tests passed normal/optimized. The research lease remains active for the immediately following100-case audit.
