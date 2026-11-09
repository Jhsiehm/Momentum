# Official BILLSTATUS hundred-case readiness audit — 9 November 2026

## Result and question

All 100 fixed cases succeeded: 100 GETs, 100 HTTP 200 responses, 100 parsed XML documents, 100 requested identity/introduction-date matches, zero observed errors and 1,441,575 response bytes. No replacements, retries, redirects, linked text-body downloads or model fits. This is source readiness, not a predictive experiment.

Question: can a hash sample of current official bill-status files provide metadata for a separately specified retrospective comparison? Population: 75,605 official-directory identities, Congresses 113–118, H.R./S. This adaptive official-source route does not release the failed BICAM sample. The first 100 ascending SHA-256(version + newline + canonical ID) were fixed before requests; the exact version is `official-billstatus-readiness-v1`. Twelve directory inputs, exact URLs, code/protocol/tests and sample are registered. No outcome enrichment. Sample by Congress: 113=11, 114=14, 115=15, 116=17, 117=24, 118=19.

## Configuration and limitations

One request per case; 2,000,000-byte response cap plus one sentinel, 20-second socket timeout, no hard total deadline. Capped prefixes and failures retained where available. DTD/entities, NUL/unsupported encodings, oversize XML, ambiguous/mixed identity schemas and mismatched Congress/type/number fail closed. Identity validity is distinct from calendar eligibility.

Extraction retains schema-path counts and declared identity/date/context-count/version metadata. Action text, action codes and law labels are not extracted as model features. Full XML and version metadata nevertheless reveal procedural progress; all cases are design-exposed, not untouched evaluation. Current event/edition dates are retrospective assertions, not historical-byte availability proofs. All 100 root schema-version attributes are absent; field shapes/path fingerprints were validated without claiming a schema-version number.

## Coverage and every shortfall

| Check | Observed result | Limit |
|---|---|---|
| Introduction dates |100 valid and within Congress |No exact historical publication time |
| Day-180 calendar window |88 pass;12 too late |Not at-risk or final training eligibility |
| Actions |100 containers;469 items;469 valid dates |Semantics/cutoff reconstruction separate |
| Sponsors |100 records;100 Bioguide IDs |No party-at-introduction proof |
| Cosponsors |82 containers;984 items;984 valid joining dates |18 absent containers remain unknown, not zero |
| Withdrawals |3 dates,all valid |No complete-history certification |
| Text versions |100 containers;122 records,all with URLs |No linked body downloaded/verified |
| Introduced metadata |98 cases |Missing hr2787-113: Reported in House only; s4805-116: Placed on Calendar Senate only |
| Introduced metadata plus day180 window |87 cases |Not historically qualified training population |

No missing case was replaced. Sponsor-party timing, committee-referral semantics, labels, family independence and class balance remain unestablished. Metadata timestamps must not be interpreted automatically as first publication.

## Every sampled case

Frozen hash order. Counts describe whole current metadata, not pre-cutoff features. Intro means introduced-edition metadata plus URL, not verified text. Window is calendar-only; unknown cosponsors means missing container.

| # | Bill | Introduction | Window | Actions | Cosponsors | Versions | Intro | Bytes | Raw SHA-256 |
|---:|---|---|---|---:|---:|---:|---|---:|---|
| 1 | [s16-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/s/BILLSTATUS-118s16.xml) | 2023-01-23 | True | 2 | 23 | 1 | True | 15501 | `db85d0e641a0c66947a097deced3bdf913591a0ed22620018aea95f52e04ef7f` |
| 2 | [s1512-113](https://www.govinfo.gov/bulkdata/BILLSTATUS/113/s/BILLSTATUS-113s1512.xml) | 2013-09-17 | True | 23 | 1 | 6 | True | 17355 | `7f5b65cef9e83f85d12d3112c03fed6b520f83ff5f44fa3e53c5f166bd20b94a` |
| 3 | [hr6235-116](https://www.govinfo.gov/bulkdata/BILLSTATUS/116/hr/BILLSTATUS-116hr6235.xml) | 2020-03-12 | True | 3 | 3 | 1 | True | 9081 | `1e3214840d1f82aa1dae51215f05374fc8218a4f25d1956f4618f4a7d857cba3` |
| 4 | [hr1852-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/hr/BILLSTATUS-117hr1852.xml) | 2021-03-11 | True | 3 | 1 | 1 | True | 9432 | `d3238daa12ab6c6fcd74c97f2cd740af830baeec63021f5acca0359234a22ef5` |
| 5 | [hr454-116](https://www.govinfo.gov/bulkdata/BILLSTATUS/116/hr/BILLSTATUS-116hr454.xml) | 2019-01-10 | True | 3 | 1 | 1 | True | 7100 | `fca44d65ef57fd7199febbe997357f534118082e7dcbba88534c7cd36d8df5bd` |
| 6 | [s2161-116](https://www.govinfo.gov/bulkdata/BILLSTATUS/116/s/BILLSTATUS-116s2161.xml) | 2019-07-18 | True | 2 | 3 | 1 | True | 9956 | `94be8f28c186373a0ec48f531d6e24e1b471815e2df294f0cf1efa111c4af0f2` |
| 7 | [hr7266-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/hr/BILLSTATUS-118hr7266.xml) | 2024-02-07 | True | 4 | 14 | 1 | True | 13703 | `2a10905b082d2e832e1b8c511636b613f4ca1c6a57827f23bd0db579bedd74ba` |
| 8 | [s2546-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/s/BILLSTATUS-118s2546.xml) | 2023-07-26 | True | 11 | 1 | 3 | True | 11844 | `248c30d38141da4c88311572a5efae0b8468be02e8dc89c237e419706d20f897` |
| 9 | [s283-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/s/BILLSTATUS-117s283.xml) | 2021-02-08 | True | 3 | 7 | 1 | True | 12215 | `ec65ac0b02bb1f336aef08fa79dba082e1f494118c6fbebff6c6565c9fdf83cc` |
| 10 | [hr7157-115](https://www.govinfo.gov/bulkdata/BILLSTATUS/115/hr/BILLSTATUS-115hr7157.xml) | 2018-11-16 | False | 5 | unknown | 1 | True | 8891 | `2fe8a4e929588e8ccdb8f916cba0c395468da69274a69a80c73ccb9feac203fb` |
| 11 | [hr1368-116](https://www.govinfo.gov/bulkdata/BILLSTATUS/116/hr/BILLSTATUS-116hr1368.xml) | 2019-02-26 | True | 4 | 136 | 1 | True | 64726 | `9869641ab7cfc2f4a3ce54ac62bed8a1ffa7405ad126da00c63d77777f7c328e` |
| 12 | [s4032-116](https://www.govinfo.gov/bulkdata/BILLSTATUS/116/s/BILLSTATUS-116s4032.xml) | 2020-06-22 | True | 2 | 9 | 1 | True | 9287 | `7e892629196084ebe9b20e4b1819d6c2169b7bb8147cb1705b628df35ff6d54f` |
| 13 | [s488-115](https://www.govinfo.gov/bulkdata/BILLSTATUS/115/s/BILLSTATUS-115s488.xml) | 2017-03-01 | True | 21 | 2 | 4 | True | 47159 | `da04356bc6c46c2320f95379b7146cdcf422d92e174f90f88815d770c338982b` |
| 14 | [s4543-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/s/BILLSTATUS-118s4543.xml) | 2024-06-13 | True | 2 | 2 | 1 | True | 6365 | `3e7d1f91f03e064de2a9efe4e0320cc9a4133f122b7d37b6e49d5810b331d86e` |
| 15 | [s155-116](https://www.govinfo.gov/bulkdata/BILLSTATUS/116/s/BILLSTATUS-116s155.xml) | 2019-01-16 | True | 2 | 3 | 1 | True | 7098 | `3949d7759e90ccbc7bd8df2e55563d475cd70853166c68f4aeabd021212ca3e3` |
| 16 | [hr9301-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/hr/BILLSTATUS-118hr9301.xml) | 2024-08-02 | False | 4 | 1 | 1 | True | 7333 | `396a063541420445867fb88f5a4f68312d320f31e43fedd28a1ddacaba3d986b` |
| 17 | [hr4543-116](https://www.govinfo.gov/bulkdata/BILLSTATUS/116/hr/BILLSTATUS-116hr4543.xml) | 2019-09-27 | True | 4 | 23 | 1 | True | 18253 | `c939808ef559b007363068102b72f56a0c8f39507e87124607dca02333a9a9f4` |
| 18 | [hr3231-113](https://www.govinfo.gov/bulkdata/BILLSTATUS/113/hr/BILLSTATUS-113hr3231.xml) | 2013-10-02 | True | 3 | 1 | 1 | True | 7605 | `36b28a0c52e5148933b665fb44603a7700427ab6583a71db0d212fd17f328dba` |
| 19 | [hr2358-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/hr/BILLSTATUS-118hr2358.xml) | 2023-03-29 | True | 3 | 5 | 1 | True | 8234 | `099190503d20d51afe0259a5a75c1ddaaad7a927af45d30a6db8ecf1fb87ac7f` |
| 20 | [s269-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/s/BILLSTATUS-118s269.xml) | 2023-02-02 | True | 2 | 5 | 1 | True | 13671 | `3a402205a5b5403b48cc700874706e1ed6318b9f8cc478ace8b9cc2c9c8b3d46` |
| 21 | [s2602-115](https://www.govinfo.gov/bulkdata/BILLSTATUS/115/s/BILLSTATUS-115s2602.xml) | 2018-03-22 | True | 9 | 6 | 2 | True | 17587 | `675440e6ebb417364e08d873170b6fa6304c1f20c1b8dc09dd1c7992a837b96c` |
| 22 | [s3141-115](https://www.govinfo.gov/bulkdata/BILLSTATUS/115/s/BILLSTATUS-115s3141.xml) | 2018-06-26 | True | 2 | unknown | 1 | True | 5468 | `e00ee85faf3071bbe042adf08b7dcd90f11afde59909d011867d7f0289181333` |
| 23 | [hr10297-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/hr/BILLSTATUS-118hr10297.xml) | 2024-12-04 | False | 3 | 5 | 1 | True | 8460 | `8c56360e686255b0a17458457df7066d8bb6426ca3cab074efb2e1c516a3cad5` |
| 24 | [hr2787-113](https://www.govinfo.gov/bulkdata/BILLSTATUS/113/hr/BILLSTATUS-113hr2787.xml) | 2013-07-23 | True | 4 | unknown | 1 | False | 27398 | `8fba208e06da7f87fb5651492f554724ac192d84ffefa4f6bb0421e77d9826c5` |
| 25 | [hr6023-114](https://www.govinfo.gov/bulkdata/BILLSTATUS/114/hr/BILLSTATUS-114hr6023.xml) | 2016-09-14 | False | 6 | 4 | 1 | True | 11924 | `34eb19c5981f6c824e40e17416e66cb2bdd9b56bf4f9777a7b35fb4f29bb891a` |
| 26 | [hr5926-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/hr/BILLSTATUS-117hr5926.xml) | 2021-11-09 | True | 3 | unknown | 1 | True | 6033 | `477985977193291f13928ed9b1d204aff97191aedffdc33c3e070b7b718ce7f0` |
| 27 | [s2568-116](https://www.govinfo.gov/bulkdata/BILLSTATUS/116/s/BILLSTATUS-116s2568.xml) | 2019-09-26 | True | 2 | 15 | 1 | True | 11996 | `8b8f3730ab26f1b32f9514f70c34632d69d983c728afb96bf3f3e66eed248cd2` |
| 28 | [hr384-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/hr/BILLSTATUS-117hr384.xml) | 2021-01-21 | True | 5 | 33 | 1 | True | 22518 | `882cdbed3b99e870e77ec5ead9a7ca8f8f7a84b3be2452d1e056b00688305712` |
| 29 | [s1776-114](https://www.govinfo.gov/bulkdata/BILLSTATUS/114/s/BILLSTATUS-114s1776.xml) | 2015-07-15 | True | 13 | 2 | 3 | True | 25472 | `9e10b984740495557ea2002bb260de4736427f0600b6db09a77671202cdec1b9` |
| 30 | [hr3157-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/hr/BILLSTATUS-117hr3157.xml) | 2021-05-12 | True | 3 | 6 | 1 | True | 8813 | `2bd332ed45cffee908d7d3c3ac39a7519ab5f975269cea2c4ba684327729d7c2` |
| 31 | [s3046-115](https://www.govinfo.gov/bulkdata/BILLSTATUS/115/s/BILLSTATUS-115s3046.xml) | 2018-06-11 | True | 2 | 9 | 1 | True | 8749 | `4bc24e2ec20e4decec7d44dd71ab3881d508524231d95e76c0602e09bd692a67` |
| 32 | [hr9317-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/hr/BILLSTATUS-118hr9317.xml) | 2024-08-06 | False | 4 | 3 | 1 | True | 8314 | `1e015e127771e0b7cd417e84bbd975a8cd82e7421327dc14217cc21184cbba4b` |
| 33 | [hr4487-115](https://www.govinfo.gov/bulkdata/BILLSTATUS/115/hr/BILLSTATUS-115hr4487.xml) | 2017-11-29 | True | 4 | 2 | 1 | True | 10807 | `69368ebfc48c9cd42ef890a364b30f2432f8a3c4ffc9353affd2023261a5870b` |
| 34 | [s2573-113](https://www.govinfo.gov/bulkdata/BILLSTATUS/113/s/BILLSTATUS-113s2573.xml) | 2014-07-09 | False | 2 | unknown | 1 | True | 6796 | `3ab7038d400d3031cdcd25e4cddaa41cf9b4e6cfdc6db58ffc5f47319395b628` |
| 35 | [s3582-116](https://www.govinfo.gov/bulkdata/BILLSTATUS/116/s/BILLSTATUS-116s3582.xml) | 2020-03-25 | True | 2 | 3 | 1 | True | 8255 | `f3ba0d9b03c06fd09d9c36a23e54a7b379c505d8a0b985a49473d944a4e6676d` |
| 36 | [hr565-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/hr/BILLSTATUS-117hr565.xml) | 2021-01-28 | True | 6 | 11 | 1 | True | 15327 | `ed4d4169863be693c744ab789a55ab8db9bcabc1fe07721b74fc1194cfe5af5e` |
| 37 | [s935-116](https://www.govinfo.gov/bulkdata/BILLSTATUS/116/s/BILLSTATUS-116s935.xml) | 2019-03-28 | True | 2 | 3 | 1 | True | 10003 | `d24f4efc296dd4f9d012e11a21b4659d1db32886c4cc04267ced7ee94846f405` |
| 38 | [s1935-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/s/BILLSTATUS-117s1935.xml) | 2021-05-27 | True | 2 | 1 | 1 | True | 8370 | `b8ce3b575f7e462ff607ce0d60b245163c683b61afc8b073aac9d6d9686314cb` |
| 39 | [hr8175-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/hr/BILLSTATUS-117hr8175.xml) | 2022-06-22 | True | 5 | 10 | 1 | True | 14162 | `252be62370c999bd49c329e315c23357edfa91006ed855f74cf6652d28db9656` |
| 40 | [hr6833-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/hr/BILLSTATUS-117hr6833.xml) | 2022-02-25 | True | 51 | 31 | 6 | True | 171923 | `36118261505712a6c459257374436433b6eea2ca9b43278e3696a16d12d65df5` |
| 41 | [hr3559-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/hr/BILLSTATUS-117hr3559.xml) | 2021-05-28 | True | 4 | unknown | 1 | True | 7725 | `52bc7930e4c2b93bc7da6b3dcbb1e727502b13f9d8ff2436f16126194ee06715` |
| 42 | [s922-116](https://www.govinfo.gov/bulkdata/BILLSTATUS/116/s/BILLSTATUS-116s922.xml) | 2019-03-28 | True | 2 | 3 | 1 | True | 10303 | `2709e626acca8eb2330de5f6790229881271d9694fcf976ea71f270a5b725221` |
| 43 | [hr1548-114](https://www.govinfo.gov/bulkdata/BILLSTATUS/114/hr/BILLSTATUS-114hr1548.xml) | 2015-03-23 | True | 4 | 65 | 1 | True | 35094 | `c239643085d56bfc4cf18ffa482139eace8fa3a3cc049acfb162424b14c965c1` |
| 44 | [hr2180-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/hr/BILLSTATUS-117hr2180.xml) | 2021-03-23 | True | 5 | 13 | 1 | True | 15169 | `7754fce5ce5ab3924093baa1adc9fdf9bbdb2fb51ab9df44a35d21c0680b4c7e` |
| 45 | [hr3754-114](https://www.govinfo.gov/bulkdata/BILLSTATUS/114/hr/BILLSTATUS-114hr3754.xml) | 2015-10-09 | True | 5 | unknown | 1 | True | 8706 | `3f100a4832b1806f6dbd020a61bcaac3986c3c5d03df54c59ec999313f6193dc` |
| 46 | [hr943-113](https://www.govinfo.gov/bulkdata/BILLSTATUS/113/hr/BILLSTATUS-113hr943.xml) | 2013-03-04 | True | 4 | unknown | 1 | True | 7390 | `3a6688c9c334f569169252da8cf627b405ab27fe9602858ed9b413707d071ca5` |
| 47 | [hr4816-114](https://www.govinfo.gov/bulkdata/BILLSTATUS/114/hr/BILLSTATUS-114hr4816.xml) | 2016-03-21 | True | 5 | 42 | 1 | True | 29529 | `249988d20fdcea6061d9db3561c536c72c8f5b3200f7d6ea338af039909ad2ab` |
| 48 | [hr6640-116](https://www.govinfo.gov/bulkdata/BILLSTATUS/116/hr/BILLSTATUS-116hr6640.xml) | 2020-04-28 | True | 4 | 11 | 1 | True | 14770 | `35a361e44a99bf1fe444d220909976146c8be665bec2c3d53c1ff22b1d7b292c` |
| 49 | [s3915-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/s/BILLSTATUS-117s3915.xml) | 2022-03-24 | True | 3 | 8 | 1 | True | 10253 | `f596e24cfcc700cd7026947d20efa5dbc8aa785563829af01ffcbb2af3a93367` |
| 50 | [s4363-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/s/BILLSTATUS-117s4363.xml) | 2022-06-08 | True | 2 | 1 | 1 | True | 5865 | `cf47e5b0f12ca936ae270514d8e54df96a87e76dd7b718a1801070d3e44fdff5` |
| 51 | [hr4076-116](https://www.govinfo.gov/bulkdata/BILLSTATUS/116/hr/BILLSTATUS-116hr4076.xml) | 2019-07-25 | True | 3 | 1 | 1 | True | 6984 | `d58f0f0fe165cab4fd9e8d720bce8844bd5c26f1274bad1a47a1fce79eaee9eb` |
| 52 | [hr155-114](https://www.govinfo.gov/bulkdata/BILLSTATUS/114/hr/BILLSTATUS-114hr155.xml) | 2015-01-06 | True | 7 | 7 | 1 | True | 14088 | `3657b77a3f6aab3bd38dcc70a162ac54284ffa39aa0bda94b5f37dac68418a88` |
| 53 | [hr1647-115](https://www.govinfo.gov/bulkdata/BILLSTATUS/115/hr/BILLSTATUS-115hr1647.xml) | 2017-03-21 | True | 9 | 2 | 1 | True | 13421 | `7a5468b194281dbbab265703f4391a1a79527d9563f8cd9d4f33a9b6b3315f8d` |
| 54 | [hr4652-113](https://www.govinfo.gov/bulkdata/BILLSTATUS/113/hr/BILLSTATUS-113hr4652.xml) | 2014-05-09 | True | 3 | 23 | 1 | True | 16097 | `bb766c996ab2a451c7df8b5cd163656ac713df0524680ab1490c47fd2f5c47fc` |
| 55 | [s4999-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/s/BILLSTATUS-117s4999.xml) | 2022-09-28 | False | 2 | unknown | 1 | True | 6120 | `376325b2bafd17426a69f64a2984108624bdc513c6ec2a76b71eaed544af2c61` |
| 56 | [hr5462-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/hr/BILLSTATUS-117hr5462.xml) | 2021-09-30 | True | 3 | 1 | 1 | True | 6301 | `7c88b126d17d694191f440aafb8668d79c54d48f694677df442d15d61cb087f2` |
| 57 | [s3199-116](https://www.govinfo.gov/bulkdata/BILLSTATUS/116/s/BILLSTATUS-116s3199.xml) | 2020-01-15 | True | 2 | 1 | 1 | True | 7214 | `e898e6ff3b829d281e8fe16456de05ec986991aa24d5ec0ac60e2767799aa672` |
| 58 | [hr7602-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/hr/BILLSTATUS-118hr7602.xml) | 2024-03-08 | True | 3 | 1 | 1 | True | 6298 | `4a75847a71c4375418c901cd90aa0996cd656375554b02dcd80bbbe43b7d5296` |
| 59 | [hr6002-115](https://www.govinfo.gov/bulkdata/BILLSTATUS/115/hr/BILLSTATUS-115hr6002.xml) | 2018-06-05 | True | 4 | unknown | 1 | True | 7551 | `488cf25daf43b165f819a2b813ab54bd0195fa73af155ffcf573c35d054d7fe9` |
| 60 | [hr6216-115](https://www.govinfo.gov/bulkdata/BILLSTATUS/115/hr/BILLSTATUS-115hr6216.xml) | 2018-06-25 | True | 22 | 6 | 5 | True | 17730 | `68720f9bf54f9d99b73a2d8cf71884448eb02e7a2f6d4caf0be08bd78326a367` |
| 61 | [s1323-113](https://www.govinfo.gov/bulkdata/BILLSTATUS/113/s/BILLSTATUS-113s1323.xml) | 2013-07-18 | True | 5 | 11 | 1 | True | 13033 | `37588a8a4e5b233355279db70125a5f74219a02e28ac5f41255b74fc5022cbce` |
| 62 | [hr450-115](https://www.govinfo.gov/bulkdata/BILLSTATUS/115/hr/BILLSTATUS-115hr450.xml) | 2017-01-11 | True | 4 | 1 | 1 | True | 7983 | `f243d608773f50f085f1b821362a52fca4c55110e0b4e113a02e73adf84465c7` |
| 63 | [hr162-116](https://www.govinfo.gov/bulkdata/BILLSTATUS/116/hr/BILLSTATUS-116hr162.xml) | 2019-01-03 | True | 3 | 4 | 1 | True | 8493 | `05003b345cf3c0cb6ed95b40e260be774393d3c62c1a227a63de515bfeb99eb5` |
| 64 | [hr8233-116](https://www.govinfo.gov/bulkdata/BILLSTATUS/116/hr/BILLSTATUS-116hr8233.xml) | 2020-09-11 | False | 4 | 2 | 1 | True | 8292 | `268d93a20c60cd94450a424ef6253acf7a285cbe796e313aa547da446989cafe` |
| 65 | [hr2507-113](https://www.govinfo.gov/bulkdata/BILLSTATUS/113/hr/BILLSTATUS-113hr2507.xml) | 2013-06-26 | True | 5 | 13 | 1 | True | 17374 | `a30386c615035d9b294a117ae0b147b689833b6f7e714f9a0c5cdd6a53f49f45` |
| 66 | [hr3102-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/hr/BILLSTATUS-117hr3102.xml) | 2021-05-11 | True | 3 | unknown | 1 | True | 7441 | `9b63a15d421d3fe0fb90074691420fe572b77674b09c67c7c882b0badf2da1e7` |
| 67 | [hr2446-114](https://www.govinfo.gov/bulkdata/BILLSTATUS/114/hr/BILLSTATUS-114hr2446.xml) | 2015-05-19 | True | 7 | 5 | 1 | True | 11667 | `b8e596d7a74ff4dfae88d927be1be72cad37e844027b36215c38f501a7d88031` |
| 68 | [hr3242-113](https://www.govinfo.gov/bulkdata/BILLSTATUS/113/hr/BILLSTATUS-113hr3242.xml) | 2013-10-03 | True | 3 | 1 | 1 | True | 6617 | `2f85c2c3940bf830c53b83c1c0116f4ec2fc3bf17a66ee46e1ca9c4509f3ef44` |
| 69 | [hr1116-113](https://www.govinfo.gov/bulkdata/BILLSTATUS/113/hr/BILLSTATUS-113hr1116.xml) | 2013-03-13 | True | 3 | unknown | 1 | True | 6889 | `f3381e167402aa10c23dee667bca136fbda01db226d394c60149f71ae00d1795` |
| 70 | [hr10493-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/hr/BILLSTATUS-118hr10493.xml) | 2024-12-18 | False | 14 | 1 | 1 | True | 22875 | `4c59b92fc5a3b212b9d9ac1445c93952733ffa6e0bf1ffc76dcd037403866b0a` |
| 71 | [hr3042-114](https://www.govinfo.gov/bulkdata/BILLSTATUS/114/hr/BILLSTATUS-114hr3042.xml) | 2015-07-13 | True | 3 | 6 | 1 | True | 9240 | `0604eba9db73548d751878f2a332cbe059dcb7177a7883be4e16423e42afc35b` |
| 72 | [s2986-114](https://www.govinfo.gov/bulkdata/BILLSTATUS/114/s/BILLSTATUS-114s2986.xml) | 2016-05-25 | True | 2 | 2 | 1 | True | 8358 | `0341fafc6a7f52afbfe53551a6bfc5d358d89c64905db12018e27b864cc7623a` |
| 73 | [s11-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/s/BILLSTATUS-118s11.xml) | 2023-01-23 | True | 2 | 2 | 1 | True | 9470 | `675eed79df7eea4d71270a41e0668fdc80cf7d65a492ec64014109fe9abc80e8` |
| 74 | [hr4718-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/hr/BILLSTATUS-118hr4718.xml) | 2023-07-18 | True | 3 | 4 | 1 | True | 9160 | `cdd7043a7ba021abb364c6b20d61b11e2c7ebfc1f20af4117a0002342c0c0ab1` |
| 75 | [s1799-114](https://www.govinfo.gov/bulkdata/BILLSTATUS/114/s/BILLSTATUS-114s1799.xml) | 2015-07-16 | True | 2 | unknown | 1 | True | 7956 | `5e43549364b693d61d3a05d8587def4b8430e9632d8459475e43b55065c60a44` |
| 76 | [s970-114](https://www.govinfo.gov/bulkdata/BILLSTATUS/114/s/BILLSTATUS-114s970.xml) | 2015-04-16 | True | 2 | 3 | 1 | True | 7354 | `9ec9ef9d2e978b0b15c40945a96551fd94ec32ae19b0c5e9204419c272a14889` |
| 77 | [s2175-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/s/BILLSTATUS-117s2175.xml) | 2021-06-22 | True | 2 | 1 | 1 | True | 6013 | `5a2eaf760449d844635bba12d629a4b24e7758170cad016b55d47d1e58771aca` |
| 78 | [hr4516-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/hr/BILLSTATUS-118hr4516.xml) | 2023-07-10 | True | 4 | unknown | 1 | True | 8446 | `998100a990f6f03c573ee8aa6b6f46d625c3ffd3607d0ab5642a7ed715792147` |
| 79 | [hr8118-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/hr/BILLSTATUS-117hr8118.xml) | 2022-06-16 | True | 4 | 17 | 1 | True | 15066 | `45e209aaa9c97778d5be1b9f8855539ff34429e4256216276ffb9588a5f3c866` |
| 80 | [s2770-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/s/BILLSTATUS-117s2770.xml) | 2021-09-21 | True | 2 | unknown | 1 | True | 6031 | `90df519795a55a1950c472a56ca39c7e45110e52c1e5fcfc6275b368c26bfa5e` |
| 81 | [s1705-113](https://www.govinfo.gov/bulkdata/BILLSTATUS/113/s/BILLSTATUS-113s1705.xml) | 2013-11-14 | True | 2 | 2 | 1 | True | 6959 | `c67bc0695d92798d4f407ebd31017351005f5a46008615b3d87eca38c85e7dc4` |
| 82 | [hr759-115](https://www.govinfo.gov/bulkdata/BILLSTATUS/115/hr/BILLSTATUS-115hr759.xml) | 2017-01-31 | True | 4 | 1 | 1 | True | 8010 | `4f733f6e3e5f480a4ff196a8ada2adf59237a0b3bd728d8851dbca2a35142d66` |
| 83 | [hr898-114](https://www.govinfo.gov/bulkdata/BILLSTATUS/114/hr/BILLSTATUS-114hr898.xml) | 2015-02-11 | True | 3 | 1 | 1 | True | 8767 | `659c0fbb00958b7dcaf8e70a24d321d85208e433fe3b76275d607e20d3251921` |
| 84 | [hr7055-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/hr/BILLSTATUS-117hr7055.xml) | 2022-03-11 | True | 4 | 15 | 1 | True | 13815 | `fc59de252797696aca978162b3d1d81345b1d33fcd266c4f36679b0b489c35ed` |
| 85 | [hr8897-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/hr/BILLSTATUS-118hr8897.xml) | 2024-06-28 | True | 3 | unknown | 1 | True | 7062 | `fc05b04164a0f336a4d23c8273b958d867965a76a6624ca3a686f432c95fd3a3` |
| 86 | [s3649-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/s/BILLSTATUS-117s3649.xml) | 2022-02-15 | True | 2 | 19 | 1 | True | 13678 | `93f11e663a133f0083da9e262f7e6d8f28ad39cf8ecd6dae645e1779af86f183` |
| 87 | [hr7839-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/hr/BILLSTATUS-117hr7839.xml) | 2022-05-19 | True | 4 | 4 | 1 | True | 10193 | `896fcc775b29656ce2ff5243920db9031b99bcd866b73b191ae73a6d294f2677` |
| 88 | [s4805-116](https://www.govinfo.gov/bulkdata/BILLSTATUS/116/s/BILLSTATUS-116s4805.xml) | 2020-10-19 | False | 3 | 15 | 1 | False | 10512 | `f66575a89150396d0cf19920a15a11ff485b62435e3e120fb90ba5c0c591f78c` |
| 89 | [hr733-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/hr/BILLSTATUS-118hr733.xml) | 2023-02-01 | True | 3 | 23 | 1 | True | 17367 | `0594b103693aff61864ae0a7762a01a4962337929e503958d70ba9b92e315928` |
| 90 | [hr4099-115](https://www.govinfo.gov/bulkdata/BILLSTATUS/115/hr/BILLSTATUS-115hr4099.xml) | 2017-10-24 | True | 4 | 237 | 1 | True | 104163 | `10c011e33e1a46f570d5872f7c3be2d1413e2159b2658ad9b613416f5d89afc4` |
| 91 | [s996-114](https://www.govinfo.gov/bulkdata/BILLSTATUS/114/s/BILLSTATUS-114s996.xml) | 2015-04-16 | True | 2 | 7 | 1 | True | 10437 | `d3e30063aeed24013646be95d333ec9d08e45127129901a955f23d66e38edd1f` |
| 92 | [hr3062-115](https://www.govinfo.gov/bulkdata/BILLSTATUS/115/hr/BILLSTATUS-115hr3062.xml) | 2017-06-26 | True | 4 | unknown | 1 | True | 9529 | `f6d6b3ac9b9df119bd63c3eb9eb02030d9e4524c90208d29f600d80363a2598b` |
| 93 | [s3517-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/s/BILLSTATUS-118s3517.xml) | 2023-12-14 | True | 2 | 2 | 1 | True | 8401 | `b32f54a3ea02e4ade902bb692bf9c26976f10f26e7c754419b11dff07ab70558` |
| 94 | [s3945-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/s/BILLSTATUS-118s3945.xml) | 2024-03-14 | True | 2 | unknown | 1 | True | 5780 | `7d871b3b25f5b1155c75bded8a87b6af89795da04c72ef99b7dd91e2f590a0ba` |
| 95 | [s2627-114](https://www.govinfo.gov/bulkdata/BILLSTATUS/114/s/BILLSTATUS-114s2627.xml) | 2016-03-03 | True | 3 | 1 | 1 | True | 7606 | `da8a1415a0ca41405c9dc4b8d345c8cd52503e3cf37d7c7b9346c6b52c5fcbd2` |
| 96 | [s752-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/s/BILLSTATUS-117s752.xml) | 2021-03-16 | True | 2 | 1 | 1 | True | 7119 | `b269acc79ef2ca1f1d0fcb6a0a7dc4c1c838ce3296f979ec13f0dcedf8ae85be` |
| 97 | [hr8091-118](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/hr/BILLSTATUS-118hr8091.xml) | 2024-04-19 | True | 4 | 10 | 1 | True | 10566 | `58ae432e9a33a0eafb85b55565157b7325f46b35871014b6734dc1bb0ddbb57f` |
| 98 | [hr5048-115](https://www.govinfo.gov/bulkdata/BILLSTATUS/115/hr/BILLSTATUS-115hr5048.xml) | 2018-02-15 | True | 3 | 1 | 1 | True | 8003 | `c107554c17c9c6e1011a83d2c5511ac46131bc33617d2f34853677bef9a2ad3a` |
| 99 | [hr8533-117](https://www.govinfo.gov/bulkdata/BILLSTATUS/117/hr/BILLSTATUS-117hr8533.xml) | 2022-07-27 | False | 4 | 1 | 1 | True | 9452 | `6df1734a528dbe2d6fb06216ce34a2a78fb498b28ba34b462d53216b4029d9fa` |
| 100 | [s5-115](https://www.govinfo.gov/bulkdata/BILLSTATUS/115/s/BILLSTATUS-115s5.xml) | 2018-12-04 | False | 2 | 1 | 1 | True | 6606 | `e0bb349a10e208921c31a65c67e708c17fcbd666398f0f9c7fa727ed48a11e5b` |

## Validation and next decision

Sixteen author/independent tests passed normally and optimized before execution. Independent replay reconstructed the exact sample from all 75,605 identities and verified all 100 raw hashes, identities, dates, complete path fingerprints, context/version outputs, calendar flags and coverage summaries. No independent network requests or model refits. The review documents its local verifier correction, with source bytes unchanged.

Root full suite: **721 tests passed in 83.818 seconds**. Software success is not forecast accuracy. No Brier/log loss, calibration, class count or predictive uncertainty is reported because no model was fitted or scored. Exact snapshot counts do not establish generalization. Initial receipt generation encountered a missing introduced-case key; corrected by explicitly treating the two missing cases as absent, not dropping them.

Continue with reviewed extraction/label-proxy/family/missingness rules for a separately registered retrospective context comparison. Proposed baseline retains six formulas but uses explicitly current edition-date assertions; challenger adds three dated context features. Sponsor party deferred before scores. No tuning, automatic promotion, historical-eligibility claim or 60% achievement. Existing E3/paper gates remain unchanged.

## Reproduction and immutable evidence

[Protocol](../../research/OFFICIAL_BILLSTATUS_READINESS_V1.md), [independent review](../../research/reviews/20261109-official-billstatus-readiness-review.md). Code: `scripts/official_billstatus_readiness_v1.py`. Tests: `python3 -m unittest tests.test_official_billstatus_readiness_v1 tests.test_official_readiness_independent`, repeated with `python3 -O`.

Network reproduction requires a fresh registered output directory; never overwrite existing runs. Prefer independent offline replay. All 100 intent/receipt/inspection files and XML remain ignored under `data/research-runs/official-billstatus-readiness-v1-20261109/`. Registration binds code/tests/protocol, directory inputs and exact sample URLs; individual raw hashes are above.

| Artifact | SHA-256 |
|---|---|
| context-coverage-summary.json | `151a532d788f5f85552f7509a799b8dfb7a28c52a8f912b04e6e091ca98616a1` |
| independent-coverage-review.json | `35125a074c13517599775e652249140728629730c500353655bf8c4f97a3b462` |
| independent-review.json | `92708cef4964c671c55aa160227e51c98c7e69bf07ee660c8ea25c4eba73d421` |
| introduced-version-coverage.json | `291c0ca327af2f637d6002fb7eb296385a974cdd956b62b839dd89515441965d` |
| registration.json | `1fd53504af49fac5cdc02a8b53737a3c681dcfc16c49846de78680e4f13421a2` |
| result.json | `3d1df97560c871a871286ba1cd721d52d7014806ab2de22388e402d44f586f6a` |
