import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from . import ai, workspace, rigor, bill_page, collections, sessions, monitoring, product_tools, explore, sampling, sample_research, autoresearch, campaigns, coverage_pipeline, consumer, evidence_audit
from . import intelligence, firm_workspace
from .fixtures import seed
from .ingest import ingest_bill
from .model import forecast, research, resolution, snapshot, locked_snapshot
from .store import ROOT, Store, now, timestamp


def load_env():
    path = ROOT / '.env'
    if path.exists():
        for line in path.read_text().splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def coverage(store, dataset):
    bills = store.bills(dataset)
    groups = {}
    for bill in bills:
        key = str(bill['congress'])
        row = groups.setdefault(key, {'congress': bill['congress'], 'bills': 0, 'events': 0, 'resolved': 0, 'archived': 0})
        row['bills'] += 1
        events = store.records('event', dataset, bill['bill_id'])
        row['events'] += len(events)
        row['resolved'] += bool(resolution(store, dataset, bill['bill_id']))
        row['archived'] += bool(bill.get('archive_proof'))
    return {'rows': sorted(groups.values(), key=lambda r: r['congress']),
            'latest_retrieval': max([b['observed_at'] for b in bills], default=None),
            'note': 'Synthetic fixture coverage only.' if dataset == 'demo' else 'Imported subset only. Not a census. Negative outcomes, family links and historical publication times require audit.'}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Paths and provider secrets never appear in routine logs.
        pass

    def respond(self, value, status=200):
        data = json.dumps(value, allow_nan=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(data)

    def context(self):
        host = self.headers.get('Host', '').split(':')[0]
        if host not in ('127.0.0.1', 'localhost'):
            raise ValueError('Use the loopback URL for this local application')
        parsed = urlparse(self.path)
        args = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        dataset = args.get('dataset', 'demo')
        if dataset not in ('demo', 'official'):
            raise ValueError('Unknown dataset')
        cutoff = timestamp(args.get('cutoff', '2023-07-01' if dataset == 'demo' else now()))
        if cutoff[:10] == now()[:10] and cutoff > now():
            cutoff = now()
        if cutoff > now():
            raise ValueError('Future replay cutoffs are not permitted')
        return parsed.path, args, dataset, cutoff

    def do_GET(self):
        store = None
        try:
            path, args, dataset, cutoff = self.context()
            if not path.startswith('/api/'):
                relative = 'index.html' if path == '/' else path.lstrip('/')
                file = (ROOT / 'web' / relative).resolve()
                if ROOT / 'web' not in file.parents or not file.is_file():
                    self.respond({'error': 'Not found'}, 404)
                    return
                self.send_response(200)
                self.send_header('Content-Type', mimetypes.guess_type(str(file))[0] or 'application/octet-stream')
                self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-ancestors 'self'")
                self.send_header('X-Content-Type-Options', 'nosniff')
                self.end_headers()
                self.wfile.write(file.read_bytes())
                return
            store = Store()
            workspace.initialize(store)
            if path == '/api/intelligence/capabilities':
                self.respond(intelligence.capabilities(store))
            elif path == '/api/intelligence/reports':
                self.respond(intelligence.reports(store))
            elif path == '/api/intelligence/report':
                self.respond(intelligence.report(store,args['id']))
            elif path == '/api/firm/profiles':
                self.respond(firm_workspace.profiles(store))
            elif path == '/api/firm/dashboard':
                self.respond(firm_workspace.dashboard(store,args['profile_id']))
            elif path == '/api/firm/brief':
                self.respond(firm_workspace.get_brief(store,args['id']))
            elif path == '/api/priorities':
                self.respond(consumer.priorities(store))
            elif path == '/api/activity':
                self.respond(consumer.activity(store))
            elif path == '/api/prospective':
                from . import prospective
                self.respond(prospective.list_receipts(store,dataset,args.get('bill_id')))
            elif path == '/api/campaigns':
                self.respond(campaigns.list_campaigns(store))
            elif path == '/api/campaign':
                self.respond(campaigns.detail(store,args.get('id','')))
            elif path == '/api/discover':
                self.respond(consumer.browse(store,args))
            elif path == '/api/coverage':
                self.respond(coverage_pipeline.summary(store))
            elif path == '/api/coverage/plans':
                self.respond(coverage_pipeline.list_plans(store))
            elif path == '/api/learning':
                from . import learning_workspace
                self.respond(learning_workspace.summary(store,args.get('dataset','official')))
            elif path == '/api/learning/detail':
                from . import learning_workspace
                self.respond(learning_workspace.detail(store,args.get('id','')))
            elif path == '/api/autoresearch':
                self.respond(autoresearch.summary(store))
            elif path == '/api/sampling/inventories':
                self.respond(sampling.list_inventories(store))
            elif path == '/api/sampling/samples':
                self.respond(sampling.list_samples(store))
            elif path == '/api/sampling/sample':
                self.respond(sampling.get_sample(store,args.get('id','')))
            elif path == '/api/sampling/assisted-audit':
                self.respond(evidence_audit.get_audit(store,args.get('id','')))
            elif path == '/api/sampling/assisted-audit.csv':
                report=evidence_audit.get_audit(store,args.get('id',''))
                if report is None:
                    raise ValueError('No machine-assisted audit is saved for this sample.')
                data=evidence_audit.export_audit_csv(report).encode('utf-8-sig')
                self.send_response(200)
                self.send_header('Content-Type','text/csv; charset=utf-8')
                self.send_header('Content-Disposition','attachment; filename="machine-assisted-audit.csv"')
                self.send_header('Cache-Control','no-store')
                self.send_header('X-Content-Type-Options','nosniff')
                self.end_headers()
                self.wfile.write(data)
            elif path == '/api/sampling/jobs':
                self.respond(sampling.list_bulk_jobs(store))
            elif path == '/api/sampling/job':
                self.respond(sampling.get_bulk_job(store,args.get('id','')))
            elif path == '/api/sampling/audit.csv':
                data=sampling.export_audit_csv(store,args.get('id','')).encode('utf-8-sig')
                self.send_response(200)
                self.send_header('Content-Type','text/csv; charset=utf-8')
                self.send_header('Content-Disposition','attachment; filename="sample-audit.csv"')
                self.send_header('Cache-Control','no-store')
                self.send_header('X-Content-Type-Options','nosniff')
                self.end_headers()
                self.wfile.write(data)
            elif path == '/api/explore':
                self.respond(explore.collection_view(store,args.get('collection_id',''),args.get('cutoff'),int(args.get('window_days','90')),int(args['collection_version']) if args.get('collection_version') else None))
            elif path == '/api/collections':
                self.respond(collections.list_collections(store))
            elif path == '/api/collection':
                self.respond(collections.get_collection(store, args.get('id', '')))
            elif path in ('/api/collections/import', '/api/import-job'):
                self.respond(collections.get_import_job(store, args.get('id', '')))
            elif path == '/api/import-jobs':
                self.respond(collections.list_import_jobs(store))
            elif path == '/api/sessions':
                self.respond([product_tools.session_brief(r) for r in sessions.list_sessions(store)])
            elif path == '/api/session':
                self.respond(product_tools.session_brief(sessions.get_session(store, args.get('id', ''))))
            elif path == '/api/session/export':
                self.respond(sessions.export_bundle(store, args.get('id', '')))
            elif path in ('/api/monitoring', '/api/watching'):
                self.respond(monitoring.summary(store))
            elif path == '/api/rigor':
                self.respond({'readiness': rigor.readiness(store, dataset), 'protocols': rigor.list_protocols(store), 'documents': {key: rigor.read_document(key) for key in rigor.DOCUMENTS}})
            elif path == '/api/research-report':
                self.respond(rigor.get_report(store, args.get('id', '')))
            elif path == '/api/research-document':
                self.respond(rigor.read_document(args.get('document', 'plan'), args.get('section')))
            elif path == '/api/chats':
                self.respond(workspace.list_chats(store))
            elif path == '/api/chat':
                self.respond(workspace.get_chat(store, args.get('id', '')))
            elif path == '/api/settings':
                self.respond(workspace.settings())
            elif path == '/api/bill-detail':
                self.respond(bill_page.detail(store,dataset,args.get('bill_id',''),args.get('cutoff') and cutoff))
            elif path == '/api/sources':
                self.respond(workspace.source_list(store, dataset))
            elif path == '/api/experiments':
                self.respond(workspace.experiment_list(store))
            elif path == '/api/experiment':
                self.respond(workspace.get_experiment(store, args.get('id', '')))
            elif path == '/api/config':
                self.respond({'today': now()[:10], 'ai_configured': bool(os.environ.get('OPENROUTER_API_KEY')), 'ai_model': os.environ.get('OPENROUTER_MODEL', 'openai/gpt-4o-mini')})
            elif path == '/api/bills':
                congress = int(args.get('congress', 118 if dataset == 'demo' else 119))
                bills = [b for b in store.bills(dataset) if b['congress'] == congress]
                rows = []
                for bill in bills:
                    snap = snapshot(store, dataset, bill['bill_id'], cutoff)
                    f = forecast(store, dataset, bill['bill_id'], cutoff)
                    if f['status'] == 'available':
                        snap = locked_snapshot(store, f)
                    rows.append({'bill_id': bill['bill_id'], 'title': snap['bill']['title'] if snap else 'Metadata unavailable at cutoff',
                                 'topic': snap['bill'].get('topic') if snap else 'Unknown', 'type': bill['type'],
                                 'stage': snap['stage_name'] if snap else 'Unavailable',
                                 'probability': f.get('probability'), 'forecast_id': f.get('id'),
                                 'reason': f.get('reason'), 'introduced_at': bill['introduced_at']})
                self.respond({'bills': rows, 'cutoff': cutoff, 'watchlist': store.watched(dataset), 'coverage': coverage(store, dataset)})
            elif path == '/api/snapshot':
                bill_id = args.get('bill_id', '')
                snap = snapshot(store, dataset, bill_id, cutoff)
                f = forecast(store, dataset, bill_id, cutoff)
                if f['status'] == 'available':
                    snap = locked_snapshot(store, f)
                previous = [p for p in store.ledger(dataset) if p['bill_id'] == bill_id and p['cutoff'] < cutoff]
                previous.sort(key=lambda p: p['cutoff'])
                self.respond({'snapshot': snap, 'forecast': f, 'previous': previous[-1] if previous else None})
            elif path == '/api/outcome':
                bill_id = args.get('bill_id', '')
                saved = store.saved(dataset, bill_id, cutoff, 'structured-l2-v1')
                result = resolution(store, dataset, bill_id)
                self.respond({'resolution': result, 'brier': (saved['probability'] - result['value']) ** 2 if saved and result else None,
                              'note': 'Outcome revealed separately. Saved forecasts unchanged.'})
            elif path == '/api/research':
                self.respond(research(store, dataset))
            elif path == '/api/discover':
                self.respond(consumer.browse(store,args))
            elif path == '/api/coverage':
                self.respond(coverage(store, dataset))
            elif path == '/api/ledger':
                self.respond(store.ledger(dataset))
            else:
                self.respond({'error': 'Not found'}, 404)
        except (ValueError, KeyError) as error:
            self.respond({'error': str(error)}, 400)
        except Exception:
            self.respond({'error': 'The request could not be completed. Check server data and retry.'}, 500)
        finally:
            if store:
                store.close()

    def do_POST(self):
        store = None
        try:
            path, args, dataset, cutoff = self.context()
            origin = self.headers.get('Origin')
            if origin and origin != 'http://' + self.headers.get('Host', ''):
                self.respond({'error': 'Cross-origin writes are not allowed'}, 403)
                return
            if not self.headers.get('Content-Type', '').startswith('application/json'):
                raise ValueError('Expected application/json')
            size = int(self.headers.get('Content-Length', '0'))
            if size > (262144 if path.startswith('/api/sampling/') else 16384):
                raise ValueError('Request is too large')
            body = json.loads(self.rfile.read(size) or '{}')
            if not isinstance(body, dict):
                raise ValueError('Expected a JSON object')
            store = Store()
            workspace.initialize(store)
            if path == '/api/intelligence/analyze':
                self.respond(intelligence.analyze(store,body),201)
            elif path == '/api/intelligence/rank':
                self.respond(intelligence.rank(store,body),201)
            elif path == '/api/intelligence/scenario':
                self.respond(intelligence.scenario(store,body),201)
            elif path == '/api/firm/profiles':
                self.respond(firm_workspace.save_profile(store,body),201)
            elif path == '/api/firm/work-item':
                self.respond(firm_workspace.save_work_item(store,body))
            elif path == '/api/firm/positions':
                self.respond(firm_workspace.add_position(store,body),201)
            elif path == '/api/firm/brief':
                self.respond(firm_workspace.create_brief(store,body),201)
            elif path == '/api/priorities':
                self.respond(consumer.priorities(store,body))
            elif path == '/api/prospective/capture':
                from . import prospective
                self.respond(prospective.capture(store,body.get('dataset','official'),body['bill_id']),201)
            elif path == '/api/campaigns':
                self.respond(campaigns.create(store,body),201)
            elif path == '/api/campaign/update':
                self.respond(campaigns.update(store,body['id'],{k:v for k,v in body.items() if k!='id'}))
            elif path == '/api/coverage/plan':
                self.respond(coverage_pipeline.plan_import(store,body),201)
            elif path == '/api/coverage/update':
                action=body.get('action') or {'paused':'pause','active':'resume'}.get(body.get('status'))
                self.respond(coverage_pipeline.update_plan(store,body['id'],{'action':action}))
            elif path == '/api/learning/train':
                from . import learning_workspace
                self.respond(learning_workspace.train(store,body['id']))
            elif path == '/api/autoresearch/settings':
                self.respond(autoresearch.configure(store,body))
            elif path == '/api/sampling/inventory':
                self.respond(sampling.discover_inventory(store,body),201)
            elif path == '/api/sampling/samples':
                self.respond(sampling.create_sample(store,body),201)
            elif path == '/api/sampling/import':
                self.respond(sampling.start_bulk_job(store,body),202)
            elif path == '/api/sampling/retry':
                self.respond(sampling.retry_bulk_job(store,body['id']),202)
            elif path in ('/api/sampling/review','/api/sampling/audit'):
                self.respond(sampling.save_audit(store,body),201)
            elif path == '/api/sampling/propose':
                self.respond(product_tools.session_brief(sample_research.propose(store,body)),201)
            elif path in ('/api/collections', '/api/collections/save'):
                self.respond(collections.save_collection(store, body), 201)
            elif path == '/api/collections/import':
                self.respond(collections.start_import_job(store, body), 202)
            elif path == '/api/sessions/propose':
                self.respond(product_tools.session_brief(sessions.propose(store, body)), 201)
            elif path == '/api/sessions/execute':
                self.respond(product_tools.session_brief(sessions.execute(store, body['id'])))
            elif path == '/api/sessions/revise':
                self.respond(product_tools.session_brief(sessions.revise(store, body['id'], body['changes'])), 201)
            elif path == '/api/sessions/replicate':
                self.respond(product_tools.session_brief(sessions.replicate(store, body['id'])), 201)
            elif path == '/api/sessions/compare':
                self.respond(sessions.compare(store, body['left_id'], body['right_id']))
            elif path == '/api/sessions/reproduce':
                self.respond(sessions.reproduce_bundle(sessions.export_bundle(store, body['id'])))
            elif path in ('/api/monitoring/settings', '/api/watching/settings'):
                self.respond(monitoring.configure(store, body))
            elif path in ('/api/monitoring/refresh', '/api/watching/refresh'):
                self.respond(monitoring.refresh_watched(store))
            elif path == '/api/chats':
                self.respond(workspace.new_chat(store), 201)
            elif path == '/api/chat/send':
                self.respond(workspace.submit_message(store, body['chat_id'], body['message'], body.get('dataset', 'demo'), body['request_id'],body.get('research_context')), 202)
            elif path == '/api/settings':
                self.respond(workspace.save_settings(body))
            elif path == '/api/settings/test':
                self.respond(workspace.connection_test())
            elif path == '/api/experiments':
                self.respond(workspace.start_experiment(store, body), 202)
            elif path == '/api/experiments/rerun':
                previous = workspace.get_experiment(store, body['id'])
                if previous.get('kind') == 'macro_pilot':
                    from . import macro_pilot
                    reproduced = macro_pilot.run(offline=True)
                    if reproduced['reproducibility_hash'] != previous['reproducibility_hash']:
                        raise ValueError('Macro reproduction does not match the saved report')
                    self.respond(dict(previous, reproduced=True))
                else:
                    self.respond(workspace.start_experiment(store, previous['config'], previous['id']), 202)
            elif path == '/api/watchlist':
                if not store.bill(dataset, body['bill_id']):
                    raise ValueError('Unknown bill')
                store.watch(dataset, body['bill_id'], bool(body['enabled']))
                self.respond({'watchlist': store.watched(dataset)})
            elif path == '/api/extract':
                snap = snapshot(store, dataset, body['bill_id'], cutoff)
                if not snap:
                    raise ValueError('No evidence available at cutoff')
                self.respond(ai.extract(store, snap))
            elif path == '/api/import':
                result = ingest_bill(store, int(body['congress']), body['type'], int(body['number']), refresh=True)
                self.respond(result)
            else:
                self.respond({'error': 'Not found'}, 404)
        except (ValueError, KeyError, TypeError) as error:
            self.respond({'error': str(error)}, 400)
        except Exception:
            self.respond({'error': 'Source request failed. Retry the import; successful records are retained.'}, 502)
        finally:
            if store:
                store.close()


def serve(port=8765):
    load_env()
    store = Store()
    seed(store)
    workspace.recover_interrupted(store)
    collections.recover_import_jobs(store)
    sampling.recover_bulk_jobs(store)
    sessions.initialize(store)
    monitoring.initialize(store)
    monitoring.recover_monitoring(store)
    autoresearch.recover(store)
    store.close()
    print(f'Legislative research workspace: http://127.0.0.1:{port}', flush=True)
    httpd = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    stop = monitoring.start_scheduler()
    research_stop = autoresearch.start_scheduler()
    try:
        httpd.serve_forever()
    finally:
        stop.set()
        research_stop.set()
        httpd.server_close()
