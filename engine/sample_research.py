"""Freeze exact sampled evidence for the eligibility-gated development runner."""
import json
from . import sampling, collections, sessions


def propose(store, args):
    sample=sampling.get_sample(store,args['sample_id'])
    test_congress=sample['protocol']['test_congress']
    expected=[b for b in sample['bill_ids'] if int(b.split('-')[0])==test_congress]
    if not expected:raise ValueError('No evaluation bills were selected. Create a larger sample.')
    batches=[collections.get_collection(store,ident,sample.get('collection_version',1)) for ident in sample['evaluation_collection_ids']]
    actual=[b for batch in batches for b in batch['bill_ids']]
    if actual!=expected:raise ValueError('Frozen evaluation membership does not match the sample.')
    collection=dict(batches[0],id='sample:'+sample['id'],name=sample['name']+' · evaluation',bill_ids=expected,
                    source_collection_ids=sample['evaluation_collection_ids'],version=1)
    selected=set(sample['bill_ids']);test_ids=set(expected)
    records=[dict(row) for row in store.db.execute("SELECT * FROM records WHERE dataset='official' ORDER BY id") if row['bill_id'] in selected]
    # Exclude all recorded evaluation families from the earlier training universe.
    # Singleton/unadjudicated IDs remain an explicit audit blocker, not proof.
    test_families={json.loads(r['body'])['family_id'] for r in records if r['bill_id'] in test_ids}
    overlapping={r['bill_id'] for r in records if r['bill_id'] not in test_ids and json.loads(r['body'])['family_id'] in test_families}
    records=[r for r in records if r['bill_id'] not in overlapping]
    title=args.get('title') or sample.get('name','Audited sample')+' · comparison'
    hypothesis=args.get('hypothesis') or 'The structured action-history model improves Brier loss over the earlier-Congress historical-rate baseline on this frozen sample.'
    if not isinstance(title,str) or not 3<=len(title)<=160 or not isinstance(hypothesis,str) or not 10<=len(hypothesis)<=3000:
        raise ValueError('Use a title of 3–160 characters and hypothesis of 10–3,000 characters.')
    blockers=[]
    if sample['readiness']['audit_passed']<sample['audit_size']:blockers.append('The designated human audit is incomplete or contains unresolved corrections.')
    if any('unadjudicated' in json.loads(r['body']).get('family_status','unadjudicated') for r in records if r['kind']=='bill'):
        blockers.append('Sampled bill families require adjudication before a family-disjoint evaluation can be claimed.')
    context={'sample_id':sample['id'],'inventory_hash':sample['inventory_hash'],'sample_hash':sample['hash'],
             'audit_receipts':sample.get('audits',{}),'excluded_training_ids':sorted(overlapping),'blockers':blockers,
             'scope':'Only sampled evidence; latest Congress evaluation, earlier sampled Congresses training. Recorded evaluation families excluded from all training. No protected holdout claim.'}
    return sessions._save_proposal(store,title,hypothesis,180,collection,records,sample_context=context)
