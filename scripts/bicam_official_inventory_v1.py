"""Bounded current GovInfo directory inventory; no bill documents or labels."""
import argparse
from collections import Counter
import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request

VERSION = 'bicam-official-inventory-v1'
CAP = 5_000_000
URLS = [(c, t, f'https://www.govinfo.gov/bulkdata/BILLSTATUS/{c}/{t}')
        for c in range(113, 119) for t in ('hr', 's')]


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    raw = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, indent=2).encode()
    with path.open('xb') as stream:
        stream.write(raw)
    return digest(raw)


class Index(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.pagination = []
        self.closed_html = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag.lower() == 'a' and 'href' in attrs:
            href = attrs['href']
            self.links.append(href)
            if re.search(r'(?:[?&](?:page|offset|start)=|/page/)', href, re.I) or 'next' in attrs.get('rel', '').lower().split():
                self.pagination.append(href)
    def handle_endtag(self, tag):
        if tag.lower() == 'html':
            self.closed_html = True


def parse(raw, congress, bill_type, url):
    if congress not in range(113, 119) or bill_type not in ('hr', 's'):
        raise ValueError('Scope outside registration')
    parser = Index()
    parser.feed(raw.decode('utf-8', errors='strict'))
    parser.close()
    ids, rejected = [], []
    for href in parser.links:
        full = urllib.parse.urlsplit(urllib.parse.urljoin(url + '/', href))
        name = full.path.rsplit('/', 1)[-1]
        if not name.startswith('BILLSTATUS-'):
            continue
        match = re.fullmatch(r'BILLSTATUS-(\d+)(hr|s)([1-9]\d*)\.xml', name)
        expected_path = f'/bulkdata/BILLSTATUS/{congress}/{bill_type}/{name}'
        if (not match or full.scheme != 'https' or full.netloc != 'www.govinfo.gov'
                or full.query or full.fragment or full.path != expected_path
                or int(match[1]) != congress or match[2] != bill_type):
            rejected.append(href)
            continue
        ids.append(f'{bill_type}{int(match[3])}-{congress}')
    counts = Counter(ids)
    accepted = bool(ids) and parser.closed_html and not parser.pagination and not rejected
    return {'congress': congress, 'bill_type': bill_type, 'url': url,
            'ids': sorted(counts), 'unique_count': len(counts), 'matching_links': len(ids),
            'duplicate_links': {k: v for k, v in sorted(counts.items()) if v > 1},
            'rejected_bill_links': rejected, 'pagination_links': parser.pagination,
            'closed_html': parser.closed_html, 'accepted_index': accepted,
            'official_completeness_certified': False, 'historical_availability_certified': False}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def run(out):
    out.mkdir(parents=True, exist_ok=False)
    pinned = [Path(__file__), Path('tests/test_bicam_official_inventory_v1.py'),
              Path('docs/research/BICAM_OFFICIAL_INVENTORY_V1.md')]
    registration = {'version': VERSION, 'urls': URLS, 'max_requests': 12,
                    'body_cap': CAP, 'read_cap_with_sentinel': CAP + 1, 'socket_timeout': 20,
                    'retries': 0, 'redirects': 0, 'content': 'directory HTML only; no XML fetches',
                    'code_protocol_hashes': {str(p): digest(p.read_bytes()) for p in pinned}}
    reg_hash = save(out / 'registration.json', registration)
    opener = urllib.request.build_opener(NoRedirect)
    results = []
    for congress, bill_type, url in URLS:
        stem = f'{congress}-{bill_type}'
        receipt = {'url': url, 'retrieved_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}
        save(out / f'{stem}-intent.json', receipt)
        try:
            try:
                response = opener.open(urllib.request.Request(url, headers={'User-Agent': VERSION}), timeout=20)
            except urllib.error.HTTPError as error:
                response = error
            with response:
                receipt.update(status=response.status, headers=dict(response.headers))
                raw = response.read(CAP + 1)
                receipt.update(bytes=len(raw), raw_sha256=save(out / f'{stem}.html', raw), truncated=len(raw) > CAP)
                if receipt['truncated']:
                    raise ValueError('Response exceeds registered cap')
                if response.status != 200:
                    raise ValueError('Non-200 response')
                if 'text/html' not in response.headers.get('Content-Type', '').lower():
                    raise ValueError('Unexpected content type')
                receipt['parsed'] = parse(raw, congress, bill_type, url)
        except Exception as error:
            receipt.update(error_type=type(error).__name__, error=str(error))
        receipt['receipt_sha256'] = save(out / f'{stem}-receipt.json', receipt)
        results.append(receipt)
    complete = all(r.get('parsed', {}).get('accepted_index') for r in results)
    summary = {'version': VERSION, 'registration_sha256': reg_hash, 'requests': len(results),
               'bytes': sum(r.get('bytes', 0) for r in results), 'all_indexes_accepted': complete,
               'observed_unique_ids': sum(r.get('parsed', {}).get('unique_count', 0) for r in results),
               'results': results, 'official_completeness_certified': False,
               'historical_availability_certified': False, 'model_fits': 0}
    save(out / 'result.json', summary)
    print(json.dumps({k: v for k, v in summary.items() if k != 'results'}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    run(parser.parse_args().output)
