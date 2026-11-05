"""Synthetic, internally consistent records. Never mixed with official data."""
import random
from datetime import datetime, timedelta, timezone
from .store import congress_end

TOPICS = ['Infrastructure', 'Health', 'Energy', 'Technology', 'Economy']
TITLES = ['Regional rail modernization', 'Rural hospital access', 'Grid resilience and storage', 'Public sector AI accountability', 'Small business lending access', 'Safe bridges investment', 'Community mental health workforce', 'Clean energy permitting', 'Consumer data protection', 'Domestic manufacturing capacity', 'Water infrastructure renewal', 'Prescription cost transparency', 'Nuclear workforce development', 'Broadband deployment coordination', 'Regional economic opportunity']

def seed(store):
    if store.checkpoint('fixture-v1'):
        return
    rng = random.Random(1873)
    for congress in range(113, 119):
        count = 15 if congress == 118 else 60
        year = 1787 + 2 * congress
        for i in range(count):
            kind = 's' if i % 3 == 0 else 'hr'
            bill_id = f'demo-{congress}-{kind}{100 + i}'
            intro = datetime(year, 1, 9, tzinfo=timezone.utc) + timedelta(days=i % 20)
            intro_str = intro.isoformat().replace('+00:00', 'Z')
            topic = TOPICS[i % 5]
            common = {'bill_id': bill_id, 'family_id': f'demo-family-{congress}-{i}', 'dataset': 'demo',
                      'source_url': '', 'source_name': 'Synthetic chronology fixture', 'archive_proof': 'fixture-v1; simulated contemporaneous availability'}
            store.add('bill', dict(common, source_key=bill_id, congress=congress, type=kind,
                                  title=TITLES[i % len(TITLES)] + (' — example' if congress == 118 else f' — prior example {i + 1}'),
                                  topic=topic, sponsor='Synthetic sponsor', introduced_at=intro_str,
                                  effective_at=intro_str, published_at=intro_str, observed_at=intro_str,
                                  verified_available_at=intro_str))
            strength = rng.random()
            maximum = 3 if strength > .76 else 2 if strength > .45 else 1 if strength > .15 else 0
            stages = [(0, 0, 'Introduced and referred to the relevant committee.')]
            if maximum >= 1:
                stages.append((45 + i % 45, 1, 'Committee reported the measure after consideration.'))
            if maximum >= 2:
                stages.append((120 + i % 80, 2, 'The originating chamber passed the measure.'))
            if maximum >= 3:
                stages.append((240 + i % 70, 3, 'Both chambers agreed to the same text.'))
            success = int(rng.random() < (0.04 + 0.65 * strength ** 2))
            if success:
                stages.append((650, 4, 'Signed into law (synthetic outcome).'))
            for index, (days, stage, text) in enumerate(stages):
                effective = (intro + timedelta(days=days)).isoformat().replace('+00:00', 'Z')
                known = (intro + timedelta(days=days, hours=6)).isoformat().replace('+00:00', 'Z')
                store.add('event', dict(common, source_key=f'{bill_id}-event-{index}', stage=stage, text=text,
                                       effective_at=effective, published_at=known, observed_at=known, verified_available_at=known))
            end = congress_end(congress)
            resolved = (intro + timedelta(days=650, hours=6)).isoformat().replace('+00:00', 'Z') if success else end
            store.add('resolution', dict(common, source_key=f'{bill_id}-resolution', value=success,
                                         effective_at=resolved, observed_at=resolved, published_at=resolved,
                                         verified_available_at=resolved, complete_coverage=True,
                                         definition='Own-bill enactment by Congress end; synthetic complete coverage'))
            if congress == 118 and i < 8:
                store.watch('demo', bill_id, True)
    store.checkpoint('fixture-v1', {'seed': 1873, 'purpose': 'Synthetic demonstration only'})
