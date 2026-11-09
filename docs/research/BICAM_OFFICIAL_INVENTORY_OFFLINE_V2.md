# Offline directory ZIP classification amendment v2

November 9, 2026. The registered v1 parser treated every anchor beginning `BILLSTATUS-` as a candidate XML link. Actual official listings also contain a same-directory downloadable ZIP; v1 correctly retained XML IDs but conservatively failed index acceptance because of that additional link. Preserve v1 registration, code, responses and failure dispositions.

This separately registered offline-only amendment recognizes exactly `https://www.govinfo.gov/bulkdata/BILLSTATUS/{Congress}/{type}/BILLSTATUS-{Congress}-{type}.zip` as a directory resource, retains its original href, and excludes it from rejected XML links. All XML identity/path/host and pagination/truncation checks remain unchanged. Unknown ZIP paths, hosts and queries still fail. No ZIP or XML is downloaded. All input and code/protocol hashes are sealed before parsing; only successful complete v1 responses with matching hashes are usable.

Run three synthetic amendment tests before freezing. Independently replay every saved response and compare XML identity lists with v1; expected XML membership change is zero. Current directory membership does not prove completeness, introduction, historical availability or outcome eligibility. No models or predictive tests run.

Reproduce with `python3 -m scripts.bicam_official_inventory_offline_v2 --source data/research-runs/bicam-official-inventory-v1-20261109 --output data/research-runs/bicam-official-inventory-offline-v2-NEW` using a fresh destination.
