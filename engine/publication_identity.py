"""Versioned publication identity reconciliation; independent of frozen cohorts."""
from datetime import date
import re
import xml.etree.ElementTree as ET

M = {'m': 'http://www.loc.gov/mods/v3'}
RULE = 'introduced-action-date-v2'


def validate_introduction(mods, package, introduced_at):
    """Crosscheck an introduced package's action date, not its issue date.

    Accept MODS bytes or a parsed Element. Missing, ambiguous, mismatched, or
    chronologically inconsistent metadata fails closed. This establishes no
    historical byte availability and grants no human audit approval.
    """
    if isinstance(mods, bytes):
        if b'<!ENTITY' in mods.upper():
            raise ValueError('XML entities are not accepted')
        mods = ET.fromstring(mods)
    match = re.fullmatch(r'BILLS-(\d+)(hr|s)(\d+)(ih|is)', package)
    if not match or match[4] != ('ih' if match[2] == 'hr' else 'is'):
        raise ValueError('Expected exact introduced bill package identity')
    if mods.findtext('m:recordInfo/m:recordIdentifier', namespaces=M) != package:
        raise ValueError('MODS package identity mismatch')
    intro = str(introduced_at)[:10]
    issued = mods.findtext('m:originInfo/m:dateIssued', namespaces=M)
    try:
        date.fromisoformat(intro)
        date.fromisoformat(issued or '')
    except ValueError as exc:
        raise ValueError('Missing or invalid introduction/issue date') from exc
    actions = []
    for action in mods.findall('m:extension/m:action', M):
        text = ' '.join(''.join(action.itertext()).split())
        if re.search(r'\bintroduced\s+the\s+following\s+bill\b', text, re.I):
            actions.append({'date': action.get('date'), 'text': text})
    if not actions:
        raise ValueError('Missing explicit MODS introduction action')
    if any(action['date'] != intro for action in actions):
        raise ValueError('Conflicting introduction action date')
    if issued < intro:
        raise ValueError('Publication issue date precedes introduction')
    return {'rule': RULE, 'package': package, 'introduced_at': intro,
            'issued_at': issued, 'introduction_actions': actions,
            'issue_date_differs': issued != intro,
            'basis': 'BILLSTATUS introduction crosschecked against explicit MODS introduction action; issue date remains separate',
            'human_audit_satisfied': False}
