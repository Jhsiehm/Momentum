"""Validate paired machine design annotations; agreement is not accuracy."""
import argparse
import hashlib
import json
from pathlib import Path
from engine.paper_evaluation import seal, unseal, require
from scripts.paper_review_packet import persist_or_compare


def validate(review, spec, inputs, registration_hash, reviewer):
    require(review['reviewer']==reviewer and review['registration_hash']==registration_hash,'Wrong reviewer/registration')
    require(review['human_certified'] is False and review['historical_feature_eligible'] is False,'Invalid certification claim')
    require([r['bill_id'] for r in review['records']]==spec['selected_ids'],'Review identity/order mismatch')
    byid={r['bill_id']:r for r in inputs};spans=[]
    for row in review['records']:
        require(isinstance(row['summary'],str) and row['summary'].strip(),'Missing bill meaning summary')
        require(set(row['labels'])==set(spec['mechanisms']),'Missing/extra mechanism')
        text=byid[row['bill_id']]['text']
        for name,label in row['labels'].items():
            require(label['status'] in spec['labels'],'Unknown label')
            require(isinstance(label['rationale'],str) and label['rationale'].strip(),'Missing rationale')
            quote=label['quote']
            require(quote is None or isinstance(quote,str),'Invalid quote type')
            if label['status']=='present':require(bool(quote) and quote.strip(),'Present label lacks evidence')
            if quote:
                start=text.find(quote)
                require(start>=0,'Evidence quote does not resolve to source')
                spans.append(dict(bill_id=row['bill_id'],mechanism=name,start=start,end=start+len(quote),quote=quote))
    return spans


def compare(directory):
    directory=Path(directory)
    registration=json.loads((directory/'registration.json').read_text());spec=unseal(registration)
    inputs=unseal(json.loads((directory/'inputs.json').read_text()))
    require(hashlib.sha256(json.dumps(inputs,sort_keys=True).encode()).hexdigest()==spec['inputs_hash'],'Inputs changed')
    reviews=[];evidence={};hashes={}
    for name in spec['reviewers']:
        envelope=json.loads((directory/(name+'.json')).read_text());review=unseal(envelope)
        evidence[name]=validate(review,spec,inputs,registration['hash'],name)
        reviews.append(review);hashes[name]=envelope['hash']
    require(len(reviews)==2,'Exactly two independent submissions required')
    disagreements=[];byfield={};total=0;agree=0
    for a,b in zip(reviews[0]['records'],reviews[1]['records']):
        for name in spec['mechanisms']:
            left,right=a['labels'][name]['status'],b['labels'][name]['status'];total+=1
            cell=byfield.setdefault(name,dict(n=0,agreement=0,confusion={}))
            cell['n']+=1;cell['agreement']+=int(left==right)
            key=left+'|'+right;cell['confusion'][key]=cell['confusion'].get(key,0)+1
            if left==right:agree+=1
            else:disagreements.append(dict(bill_id=a['bill_id'],mechanism=name,agent_a=a['labels'][name],agent_b=b['labels'][name]))
    result=seal(dict(registration_hash=registration['hash'],review_hashes=hashes,comparisons=total,agreements=agree,
                     agreement_fraction=agree/total,by_mechanism=byfield,disagreements=disagreements,
                     resolved_quote_spans=evidence,human_certified=False,historical_feature_eligible=False,
                     interpretation='Descriptive agreement between two agents on selected design cases; no accuracy, precision, recall or independence guarantee'))
    persist_or_compare(directory/'comparison.json',result)
    return result


def verify_adjudication(directory):
    directory=Path(directory)
    comparison=compare(directory)
    registration=json.loads((directory/'registration.json').read_text());spec=unseal(registration)
    inputs=unseal(json.loads((directory/'inputs.json').read_text()))
    envelope=json.loads((directory/'adjudication.json').read_text());body=unseal(envelope)
    spans=validate(body,spec,inputs,registration['hash'],spec['adjudicator'])
    require(body['comparison_hash']==comparison['hash'],'Wrong comparison binding')
    require(body['review_hashes']==comparison['body']['review_hashes'],'Wrong review binding')
    require(body['original_disagreements']==comparison['body']['disagreements'],'Original disagreements changed')
    reviewers=[unseal(json.loads((directory/(r+'.json')).read_text())) for r in spec['reviewers']]
    expected={(r['bill_id'],m) for r in body['records'] for m in spec['mechanisms']}
    challenges={(r['bill_id'],r['mechanism']):r for r in body['challenges']}
    require(set(challenges)==expected and len(challenges)==len(body['challenges']),'Missing/duplicate challenge')
    for a,b,c in zip(reviewers[0]['records'],reviewers[1]['records'],body['records']):
        for name in spec['mechanisms']:
            challenge=challenges[(a['bill_id'],name)]
            require(challenge['agent_a']==a['labels'][name] and challenge['agent_b']==b['labels'][name],'Original review label changed')
            require(challenge['original_agreement']==(a['labels'][name]['status']==b['labels'][name]['status']),'Agreement flag mismatch')
            require(challenge['adjudicated_status']==c['labels'][name]['status'],'Adjudicated status mismatch')
            require(isinstance(challenge['challenge_rationale'],str) and challenge['challenge_rationale'].strip(),'Missing challenge rationale')
    result=seal(dict(adjudication_hash=envelope['hash'],challenge_count=len(challenges),quote_count=len(spans),
                     human_certified=False,semantic_accuracy_verified=False))
    persist_or_compare(directory/'adjudication-verification.json',result)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path)
    p.add_argument('--adjudication',action='store_true');args=p.parse_args()
    r=verify_adjudication(args.directory) if args.adjudication else compare(args.directory)
    print(json.dumps({k:v for k,v in r['body'].items() if k not in ('by_mechanism','disagreements','resolved_quote_spans')},indent=2))
