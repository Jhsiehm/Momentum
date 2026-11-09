# Current official bill-status directory inventory v1

November 9, 2026. This registered source-coverage audit retrieves exactly twelve GovInfo directory HTML pages: Congresses 113–118 crossed with H.R. and S. at `https://www.govinfo.gov/bulkdata/BILLSTATUS/{congress}/{type}`. It does not retrieve bill XML, text, action histories or labels, and fits no models.

Before requests, seal this protocol, runner, synthetic tests and exact URLs in an immutable runtime registration. One request per URL; no redirects or retries; 20-second socket timeout (not a measured total-run bound); five-million-byte response cap plus one sentinel byte. Save request intent, response status/headers/body/hash, cap disposition and all parsing failures. Failures do not trigger replacement requests or silent format repairs.

Parse UTF-8 HTML anchors only. Accept filenames matching the exact Congress/type and positive integer bill number, on the official HTTPS host under the same directory; reject ambiguous query/fragment or out-of-scope bill links. Count duplicate links and preserve rejected links. Flag pagination links and absent closing HTML. Empty, paginated, truncated or malformed listings do not pass index acceptance. These conservative syntactic checks do not prove an unpaginated listing includes every introduced bill. No maximum-number interpolation is allowed.

Save each directory's distinct IDs and counts. A separately versioned offline comparison can join these current official IDs to the frozen BICAM identity projection, preserving both difference sets and all corpus exclusions. Directory filenames establish current presence only: they do not certify genuine introduction, historical public availability, law status, cohort eligibility or complete official coverage. Neither listing absence nor a corpus blank creates a negative outcome label.

Synthetic tests precede registration. Independent post-run review must replay directory parsing, hashes, counts and scope without additional source requests. No findings authorize new model fits or change existing research gates. Raw responses and results remain ignored under `data/research-runs/`.

Reproduction uses a fresh directory: `python3 -m scripts.bicam_official_inventory_v1 --output data/research-runs/bicam-official-inventory-v1-NEW`. Never overwrite a prior registration or response.
