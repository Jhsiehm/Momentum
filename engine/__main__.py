import argparse
import json
from .store import Store
from .fixtures import seed
from .server import load_env, serve
from .ingest import ingest_bill, import_xml, sync_congress, import_audited_records
from .model import forecast, research
from .evaluate import evaluate
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Point-in-time legislative forecasting research')
    sub = parser.add_subparsers(dest='command', required=True)
    serve_p = sub.add_parser('serve'); serve_p.add_argument('--port', type=int, default=8765)
    sub.add_parser('seed')
    imp = sub.add_parser('ingest'); imp.add_argument('congress', type=int); imp.add_argument('type', choices=['hr', 's']); imp.add_argument('number', type=int); imp.add_argument('--refresh', action='store_true')
    xml = sub.add_parser('import-xml'); xml.add_argument('file'); xml.add_argument('--source-url', required=True)
    audit = sub.add_parser('import-audited'); audit.add_argument('file')
    sync = sub.add_parser('sync'); sync.add_argument('congress', type=int); sync.add_argument('--limit', type=int, default=20)
    f = sub.add_parser('forecast'); f.add_argument('bill_id'); f.add_argument('cutoff'); f.add_argument('--dataset', choices=['demo', 'official'], default='official')
    export = sub.add_parser('export'); export.add_argument('path'); export.add_argument('--dataset', choices=['demo', 'official'], default='official')
    backtest = sub.add_parser('backtest'); backtest.add_argument('--dataset', choices=['demo', 'official'], default='demo'); backtest.add_argument('--test-congress', type=int, default=118); backtest.add_argument('--age-days', type=int, default=180)
    ev = sub.add_parser('evaluate'); ev.add_argument('predictions'); ev.add_argument('labels')
    args = parser.parse_args()
    load_env()
    if args.command == 'serve':
        serve(args.port); return
    store = Store()
    try:
        if args.command == 'seed':
            seed(store); result = {'status': 'seeded synthetic demonstration'}
        elif args.command == 'ingest':
            result = ingest_bill(store, args.congress, args.type, args.number, args.refresh)
        elif args.command == 'import-xml':
            result = import_xml(store, Path(args.file).read_bytes(), args.source_url)
        elif args.command == 'import-audited':
            result = import_audited_records(store, args.file)
        elif args.command == 'sync':
            result = sync_congress(store, args.congress, args.limit)
        elif args.command == 'forecast':
            result = forecast(store, args.dataset, args.bill_id, args.cutoff)
        elif args.command == 'export':
            rows = store.ledger(args.dataset)
            Path(args.path).write_text(''.join(json.dumps(r) + '\n' for r in rows))
            result = {'forecasts': len(rows), 'path': args.path}
        elif args.command == 'backtest':
            from datetime import timedelta
            from .model import date
            predictions = []
            for bill in store.bills(args.dataset):
                if bill['congress'] == args.test_congress:
                    cutoff = (date(bill['introduced_at']) + timedelta(days=args.age_days)).isoformat()
                    predictions.append(forecast(store, args.dataset, bill['bill_id'], cutoff))
            result = {'test_congress': args.test_congress, 'available': sum(p['status'] == 'available' for p in predictions), 'attempted': len(predictions), 'report': research(store, args.dataset)}
        elif args.command == 'evaluate':
            result = evaluate(args.predictions, args.labels)
        print(json.dumps(result, indent=2))
    finally:
        store.close()

if __name__ == '__main__':
    main()
