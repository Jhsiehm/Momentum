"""Bounded official metadata acquisition; no automatic field correction."""
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request
import datetime

CASES = ('s4653-116', 's4899-117', 's5314-118', 's5543-118', 's5575-118')
URLS = {'s4653-116': 'https://www.govinfo.gov/content/pkg/CREC-2020-09-22/pdf/CREC-2020-09-22-senate.pdf', 's4899-117': 'https://www.govinfo.gov/content/pkg/CREC-2022-09-20/pdf/CREC-2022-09-20-pt1-PgD995.pdf', 's5314-118': 'https://www.govinfo.gov/content/pkg/CREC-2024-11-13/pdf/CREC-2024-11-13-dailydigest.pdf', 's5543-118': 'https://www.govinfo.gov/content/pkg/CREC-2024-12-16/pdf/CREC-2024-12-16.pdf', 's5575-118': 'https://www.govinfo.gov/content/pkg/CREC-2024-12-17/pdf/CREC-2024-12-17-pt1-PgS7104-2.pdf'}
OUT = Path('data/research-runs/bicam-five-record-20261109')

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

def save(path, data):
    with path.open('xb') as stream:
        stream.write(data)

def run():
    OUT.mkdir(parents=True, exist_ok=False)
    plan = {'cases': CASES, 'source': 'Congressional Record dated introduction evidence; adaptive fallback after official endpoint failures',
            'urls': URLS, 'requests': 5, 'per_response_cap': 10000000, 'socket_timeout': 20,
            'retries': 0, 'redirects': 0, 'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'acceptance': 'Manual independent identity and explicit introduction-date review; dateIssued alone insufficient.',
            'outputs': 'Separate reconciliation ledger, never overwrite original blanks; no sample or fits.'}
    save(OUT/'registration.json', json.dumps(plan, indent=2).encode())
    opener = urllib.request.build_opener(NoRedirect)
    for bid in CASES:
        number, congress = bid[1:].split('-')
        package = f'BILLS-{congress}s{number}is'
        url = URLS[bid]
        receipt = {'bill_id': bid, 'package': package, 'url': url,
                   'retrieved_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}
        save(OUT/f'{bid}-intent.json', json.dumps(receipt).encode())
        raw = b''
        try:
            try:
                response = opener.open(urllib.request.Request(url, headers={'User-Agent':'Momentum-identity-audit/1'}),timeout=20)
            except urllib.error.HTTPError as exc:
                response = exc
            with response:
                receipt.update(status=response.status, headers=dict(response.headers))
                raw = response.read(10000001)
                save(OUT/f'{bid}-response.bin', raw)
                receipt.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
                if len(raw)>10000000:
                    raise ValueError('Response cap exceeded; body is capped prefix')
                if response.status!=200:
                    raise ValueError('Non-200 response')
        except Exception as exc:
            receipt.update(error_type=type(exc).__name__,error=str(exc))
        save(OUT/f'{bid}-receipt.json',json.dumps(receipt,indent=2).encode())

if __name__ == '__main__':
    run()
