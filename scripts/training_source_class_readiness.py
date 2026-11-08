"""Post-acquisition class counts from exposed labels; never select or fit cases."""
import argparse
import json
from pathlib import Path
from engine.paper_evaluation import require, seal, unseal
from engine.store import digest
from scripts.cross_congress_evaluate import load_rows
from scripts.paper_review_packet import persist_or_compare


def summarize(memberships, labels, available):
    result = {}
    for fold, membership in memberships.items():
        core, cal = membership['core_ids'], membership['calibration_ids']
        require(len(set(core+cal)) == len(core+cal), 'Overlapping or duplicate training roles')
        result[fold] = {}
        for role, ids in [('core', core), ('calibration', cal)]:
            selected = [bid for bid in ids if bid in available]
            require(all(bid in labels and type(labels[bid]) in (int, float) and labels[bid] in (0, 1) for bid in selected), 'Invalid or missing exposed outcome')
            positives = int(sum(labels[bid] for bid in selected))
            result[fold][role] = dict(n=len(selected), recorded_positive=positives,
                                      both_classes=0 < positives < len(selected))
    return result


def run(directory):
    directory = Path(directory)
    def read(name): return json.loads((directory/name).read_text())
    registration, result = read('registration.json'), read('result.json')
    spec, report = unseal(registration), unseal(result)
    require(report['registration_hash'] == registration['hash'], 'Result registration mismatch')
    baseline = set(spec.get('baseline_available_ids', spec.get('baseline_design_ids', [])))
    available = set(baseline)
    selected_ids = {r['bill_id'] for r in spec['selection']}
    for bid in selected_ids:
        row = unseal(read('records/'+bid+'.json'))
        require(row['bill_id'] == bid and row['registration_hash'] == registration['hash'], 'Source record binding mismatch')
        if row['status'] == 'metadata_dated_current_xml': available.add(bid)
    rows = load_rows()
    labels = {r['bill_id']: r['y'] for r in rows if 'y' in r}
    before = summarize(spec['memberships'], labels, baseline)
    after = summarize(spec['memberships'], labels, available)
    for fold, roles in after.items():
        for role, count in roles.items():
            require(count['n'] == report['coverage_after'][fold][role]['metadata_dated_xml'], 'Coverage count mismatch')
    used = set().union(*(set(m['core_ids']+m['calibration_ids']) & available for m in spec['memberships'].values()))
    output = seal(dict(registration_hash=registration['hash'], coverage_result_hash=result['hash'],
                       exposed_label_digest=digest({bid: labels[bid] for bid in sorted(used)}),
                       before=before, after=after,
                       all_partitions_have_both_classes=all(c['both_classes'] for roles in after.values() for c in roles.values()),
                       predictive_ready=False,
                       unresolved=['Historical rendition/source/label/family eligibility uncertified',
                                   'New text lacks reviewed mechanism extraction',
                                   'No registered matched predictive comparison; class presence alone is insufficient'],
                       scope='Post-acquisition counts of already-exposed labels; no selection changes, fitting, predictions or scores.'))
    persist_or_compare(directory/'class-readiness.json', output)
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    print(json.dumps(run(parser.parse_args().directory), indent=2))
