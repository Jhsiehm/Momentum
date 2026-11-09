# Alternative rendition leads: post-result inspection

November 8, 2026 local date. This is an explicitly **post-result exploratory inspection**, not a registered endpoint, a new primary outcome, or historical-public-access certification. It does not change the eight-case feasibility verdict. No network request, text extraction, outcome access or model fit was performed.

**Result: switching to the currently packaged PDF or HTML does not establish historical eligibility.** All 16 retained PDF/HTML members match their recorded PREMIS SHA-256 digests, but their matching current rendition creation and checksum events are in January 2023, after the eight historical cutoffs. All eight PDF objects also have 2023 digital-signature-assignment events. PREMIS records source-rendition lineage extending to pre-cutoff submission events; this supplies concrete retrieval leads, not a proof that the current bytes existed or were publicly available then.

Method: inspect the same eight registered cases and already-downloaded PREMIS/ZIP pairs. Hash each exact package PDF and HTML member, locate the matching PREMIS object digest, follow its structural representation relationship, and report linked checksum/rendition events and source-rendition identifiers. “Earliest” below means earliest linked event found in these retained records, not first existence in all archives. A current creation event does not prove substantive text changed; a historical submission event does not establish public availability. PDF signatures were not cryptographically validated.

## Per-object results

| Bill / rendition | Cutoff | Current object | SHA-256 of ZIP member | Matching checksum event | Matching rendition creation |
| --- | --- | --- | --- | --- | --- |
| 113-hr3884 .pdf | 2014-07-14T23:59:59Z | `D09002ee1ba618c8b` | `34cf55a6fd70e98ae31e57070f083134ea5c463a7328d001393fd16ad0e5a368` | 2023-01-07T00:57:38-05:00 | 2023-01-07T00:57:39-05:00 |
| 113-hr3884 .htm | 2014-07-14T23:59:59Z | `D09002ee1ba618c8a` | `ab854062d643129dafa59b7202f181ffcab8b3979db7c0b944b939368852de8c` | 2023-01-07T00:57:38-05:00 | 2023-01-07T00:57:39-05:00 |
| 113-hr4267 .pdf | 2014-09-10T23:59:59Z | `D09002ee1ba5f689f` | `ca07d04032ebbfeb868896cdf800559afd00bb40c2d4d1a1dbeea7c568d95fde` | 2023-01-06T23:48:35-05:00 | 2023-01-06T23:48:35-05:00 |
| 113-hr4267 .htm | 2014-09-10T23:59:59Z | `D09002ee1ba5f67a6` | `464cc483ae511a034c3d9e9091776fff5484f579360ebbf9ec036c8c1da75c11` | 2023-01-06T23:48:34-05:00 | 2023-01-06T23:48:35-05:00 |
| 114-hr2776 .pdf | 2015-12-12T23:59:59Z | `D09002ee1ba41479d` | `db9b940969baf3f29afe623e0ed9f7d5ba2980b77d274306f609a29b52946b75` | 2023-01-06T04:53:20-05:00 | 2023-01-06T04:53:21-05:00 |
| 114-hr2776 .htm | 2015-12-12T23:59:59Z | `D09002ee1ba41479c` | `3764345e197ef37455f13a4475bf8c711ee69d3795bcbeb0fe6549f15baa0d2f` | 2023-01-06T04:53:20-05:00 | 2023-01-06T04:53:21-05:00 |
| 114-hr2447 .pdf | 2015-11-15T23:59:59Z | `D09002ee1ba43c2b4` | `a1e3c8403bab6db6e8e0883555a55491e8724f130a80cebe7b9a562789d6cfd8` | 2023-01-06T06:33:19-05:00 | 2023-01-06T06:33:20-05:00 |
| 114-hr2447 .htm | 2015-11-15T23:59:59Z | `D09002ee1ba43c2b3` | `a0199d37671a27ab1f24486605514292ef8a7abe7a20f546c6fb8a4a3ecb2873` | 2023-01-06T06:33:19-05:00 | 2023-01-06T06:33:19-05:00 |
| 115-hr4997 .pdf | 2018-08-12T23:59:59Z | `D09002ee1b9d1a340` | `e150845084bbf886d9d90a51fc69cedd536afe4079f7299e53ad46b467fd61f8` | 2023-01-03T15:20:40-05:00 | 2023-01-03T15:20:41-05:00 |
| 115-hr4997 .htm | 2018-08-12T23:59:59Z | `D09002ee1b9d1a33f` | `94d02580804543b3dd92c33c5e39da1c89f09bc41b5eba7607adcb0470fec03a` | 2023-01-03T15:20:39-05:00 | 2023-01-03T15:20:41-05:00 |
| 115-s2712 .pdf | 2018-10-16T23:59:59Z | `D09002ee1b9cac6fe` | `a7910f0bb24a9f6bf810c7dd4096d9833aec1232ab9119e8176bc2d4cf37c3a6` | 2023-01-03T10:23:04-05:00 | 2023-01-03T10:23:04-05:00 |
| 115-s2712 .htm | 2018-10-16T23:59:59Z | `D09002ee1b9cac6fd` | `86ddbfac047f991b7e7436556e9ca3b2d1bd06f0f87712fbc027d52efa1dae71` | 2023-01-03T10:23:03-05:00 | 2023-01-03T10:23:04-05:00 |
| 116-s2862 .pdf | 2020-05-12T23:59:59Z | `D09002ee1b99d7c7f` | `f13b1f2125badab95d90496af358a8cf2780a6963a72edd59b04513c73682527` | 2023-01-01T04:26:21-05:00 | 2023-01-01T04:26:21-05:00 |
| 116-s2862 .htm | 2020-05-12T23:59:59Z | `D09002ee1b99d7c7e` | `622692f53ac6519a83204593b597d03bffabc91434ca5c576d7ab66a0f1c4119` | 2023-01-01T04:26:20-05:00 | 2023-01-01T04:26:21-05:00 |
| 116-s843 .pdf | 2019-09-10T23:59:59Z | `D09002ee1b9b2937d` | `ca0fc89d28d087f5a5e33fe28c45c2eb61573e05d4cd320f2bfb05b3997ffa21` | 2023-01-02T09:52:38-05:00 | 2023-01-02T09:52:38-05:00 |
| 116-s843 .htm | 2019-09-10T23:59:59Z | `D09002ee1b9b2937c` | `47803e72854cbb684fac5e070f9b8bb7d44016b1835a1894e62a635fcc7784ce` | 2023-01-02T09:52:37-05:00 | 2023-01-02T09:52:38-05:00 |

## Historical lineage leads

| Bill / current rendition | Source rendition named by 2023 creation | Earliest linked historical event |
| --- | --- | --- |
| 113-hr3884 .pdf | `R0b002ee186e098be` | 2014-01-18T00:37:47-05:00 / Rendition Submitted |
| 113-hr3884 .htm | `R0b002ee186e098c2` | 2014-01-18T00:37:47-05:00 / Rendition Submitted |
| 113-hr4267 .pdf | `R0b002ee18802105c` | 2014-03-20T22:57:05-04:00 / Rendition Submitted |
| 113-hr4267 .htm | `R0b002ee188021060` | 2014-03-20T22:57:05-04:00 / Rendition Submitted |
| 114-hr2776 .pdf | `R0b002ee18cb214f3` | 2015-06-19T03:40:17-04:00 / Rendition Submitted |
| 114-hr2776 .htm | `R0b002ee18cb2191b` | 2015-06-19T03:40:17-04:00 / Rendition Submitted |
| 114-hr2447 .pdf | `R0b002ee18c7db446` | 2015-05-28T03:10:43-04:00 / Rendition Submitted |
| 114-hr2447 .htm | `R0b002ee18c7db44a` | 2015-05-28T03:10:43-04:00 / Rendition Submitted |
| 115-hr4997 .pdf | `R0b002ee1987f387d` | 2018-02-17T00:51:06-05:00 / Rendition Submitted |
| 115-hr4997 .htm | `R0b002ee1987f387b` | 2018-02-17T00:51:06-05:00 / Rendition Submitted |
| 115-s2712 .pdf | `R0b002ee19a242cc1` | 2018-04-26T22:11:54-04:00 / Rendition Submitted |
| 115-s2712 .htm | `R0b002ee19a242cbf` | 2018-04-26T22:11:54-04:00 / Rendition Submitted |
| 116-s2862 .pdf | `R0b002ee1a3cbb1df` | 2019-11-21T19:51:01-05:00 / Rendition Submitted |
| 116-s2862 .htm | `R0b002ee1a3cbb1dd` | 2019-11-21T19:51:01-05:00 / Rendition Submitted |
| 116-s843 .pdf | `R0b002ee1a03cf980` | 2019-04-03T01:21:58-04:00 / Rendition Submitted |
| 116-s843 .htm | `R0b002ee1a03cf97e` | 2019-04-03T01:21:58-04:00 / Rendition Submitted |

These links are not a validated byte-preserving transformation chain. Retrieve the earlier objects or obtain authoritative transformation/digest evidence and time-specific public-access evidence in a separately registered bounded study. Current public-access locations describe current holdings. Do not infer historical public access from those locations, submission, creation, signatures, HTTP metadata or package issue dates alone.

## Evidence and implications

Complete derived inspection: `data/research-runs/historical-source-feasibility-v1-20261108/alternative-rendition-exploration.json`, SHA-256 `aa075e85671c3264fdcda42b9f03b15d36b05dc75974a6278e6f1e7b50feecac`. This is an unsealed exploratory metadata record, distinct from the sealed registered result. It records all matching object/representation IDs, linked event IDs/details, filenames and PREMIS hashes. The original retained files were only read.

| Case | PREMIS raw file | PREMIS SHA-256 | ZIP raw file |
| --- | --- | --- | --- |
| 113-hr3884 | `request-00.raw` | `95dd180b17965907ab2dee3e42e5a5a9e0019959b4d0b620b516b5f1cad2b956` | `request-01.raw` |
| 113-hr4267 | `request-02.raw` | `108d2ed2740d78706ed80781f59eaa95d29a552518b15bfa12a40c93ac5ef9e6` | `request-03.raw` |
| 114-hr2776 | `request-04.raw` | `6389613d596f9d19ddc1a6de33d1924c98886609028b31f0f8a866f748f0f227` | `request-05.raw` |
| 114-hr2447 | `request-06.raw` | `88a313e845ccc880c054b98ea8ae932b76840a31fe65f4a229eceb1b22a46e3f` | `request-07.raw` |
| 115-hr4997 | `request-08.raw` | `c24883265dfbf527183341ada42adfa86a9e40c4fc78cb7df32f17058e8ce819` | `request-09.raw` |
| 115-s2712 | `request-10.raw` | `c97c974ae2a2f2c68ae13c5ebda8c349e445b7439d5faf92a99ff2f8fafb0f9f` | `request-11.raw` |
| 116-s2862 | `request-12.raw` | `0bce49e8aab4be748e1d60f2d3e1e668c1c5dd98c24d3c89942ee8b74ed668f5` | `request-13.raw` |
| 116-s843 | `request-14.raw` | `e70a1e4c196b88f2546dd3f95b104478022452737aaf931210d37981e996b419` | `request-15.raw` |

A PDF- or HTML-derived introduced-text feature remains conceptually compatible with E3’s introduced-language question, but it is a different extraction representation from the current XML renderer. It requires its own prospective source/extraction/normalization and mapping specification, code hashes and measurement checks before inclusion in a later execution registration. It cannot silently replace XML in frozen evidence, reuse XML offsets, or expand this completed feasibility study’s primary endpoint. No source or model gate is released here.

Actionable next route: pursue authenticated prior objects/digests or an adequately declared and reviewed transformation chain for the exact source rendition identifiers above. Merely downloading the current PDF/HTML at larger scale would reproduce the unresolved provenance problem.
