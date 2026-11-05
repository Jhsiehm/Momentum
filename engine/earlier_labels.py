"""Bounded final-calendar evidence for complete 116th-Congress binary outcomes."""
import hashlib
import io
import re
from . import cohort

PACKAGE = 'CCAL-116hcal-S2'
PDF_URL = f'https://www.govinfo.gov/content/pkg/{PACKAGE}/pdf/{PACKAGE}-pt7.pdf'


def parse_calendar(text, congress=116, expected=344):
    if 'PUBLIC' not in text or 'LAWS' not in text:
        raise ValueError('Missing public-law table heading')
    pattern = re.compile(rf'{congress}[–−-](\d+)\s*\.+\s*(H\.J\.\s*Res\.|S\.J\.\s*Res\.|H\.R\.|S\.)\s*(\d+)')
    rows = [{'law': int(n), 'bill_id': f'{congress}-{re.sub("[^a-z]", "", kind.lower())}{int(bill)}'}
            for n, kind, bill in pattern.findall(text)]
    if len(rows) != expected or {r['law'] for r in rows} != set(range(1, expected + 1)):
        raise ValueError('Incomplete or duplicate final-calendar law sequence')
    if len({r['bill_id'] for r in rows}) != expected:
        raise ValueError('Duplicate final-calendar bill identity')
    return sorted(rows, key=lambda r: r['law'])


def historical_census(sources, laws):
    """All binary outcomes require complete final calendar, not selected positive bills.

    Enactment dates come from the crosschecked NARA census, not this calendar.
    They must not be claimed historically available through this proof.
    """
    import pypdf
    mods, proof = cohort.package_audit(sources, PACKAGE)
    title = mods.findtext('m:titleInfo/m:title', namespaces=cohort.M)
    if title != 'House Calendars, Final - 116th Congress, 2nd Session':
        raise ValueError('Wrong final calendar title')
    extensions = mods.findall('m:extension', cohort.M)
    if not any(e.findtext('m:edition', namespaces=cohort.M) == 'FINAL' and
               e.findtext('m:congress', namespaces=cohort.M) == '116' for e in extensions):
        raise ValueError('Missing final edition / Congress assertion')
    raw, pdf_source = sources.get(PDF_URL)
    reader = pypdf.PdfReader(io.BytesIO(raw))
    text = '\n'.join(page.extract_text(extraction_mode='layout') for page in reader.pages)
    rows = parse_calendar(text)
    expected = sorted([{'law': r['law'], 'bill_id': r['bill_id']} for r in laws], key=lambda r: r['law'])
    if rows != expected:
        raise ValueError('Final calendar / NARA census disagreement')
    return {'congress': 116, 'complete': True, 'complete_laws': len(rows),
            'available_at': proof['available_at'], 'calendar': proof,
            'table_source': pdf_source, 'rows': rows,
            'extraction': {'tool': 'pypdf', 'version': pypdf.__version__, 'mode': 'layout',
                           'pages': len(reader.pages), 'text_sha256': hashlib.sha256(text.encode()).hexdigest()},
            'basis': 'Final official calendar enumerates all public-law / originating-bill pairs; exact sequence and identities crosschecked against final NARA census.',
            'limitations': ['Calendar proves bounded binary own-bill enactment labels; it does not provide historical enactment-date provenance.',
                            'Availability uses official package preservation metadata, not independently proven historical rendition byte identity.',
                            'This alternate source requires a new protocol; original frozen study remains unchanged.']}


def dated_law(sources, law):
    """Independent law-date provenance, required when outcomes use a date boundary."""
    from .label_investigation import law_identity
    mods, proof = cohort.package_audit(sources, f"PLAW-116publ{law['law']}")
    actual = law_identity(mods, 116, law['law'])
    if actual != law:
        raise ValueError('Individual law / NARA date or identity disagreement')
    return {**actual, 'available_at': proof['available_at'], 'proof': proof}
