"""Synthetic-validated candidate E3 preprocessing; not historical certification."""
import math
import re
import unicodedata
from collections import Counter

import numpy as np
from scipy.sparse import csr_matrix

from engine.paper_evaluation import require, seal
from scripts.bill_structural_input_v1 import validate

VERSION = 'matched-text-preprocessing-v1'
MASK_TAGS = frozenset({'metadata', 'action', 'congress', 'session', 'legis-num',
                       'current-chamber', 'legis-type', 'distribution-code', 'date',
                       'sponsor', 'cosponsor', 'committee-name'})
WORD = re.compile(r'[^\W_]+', re.UNICODE)


def prepare_document(raw, bill_id, view, view_hash, sidecar):
    """Authenticate topology; retain source text and source-coordinate segments.

    Mask named administrative subtrees outside legis-body, preserving official-title.
    Mask exact focal bill identifiers anywhere; other statutory references survive.
    Never globally mask status words.
    """
    validate(sidecar, raw, bill_id, view, view_hash)
    text = view['text']
    nodes = sidecar['nodes']
    bodies = [n for n in nodes if n['tag'] == 'legis-body']
    require(len(bodies) == 1, 'Exactly one substantive legis-body required')
    body = bodies[0]
    masks = []
    for n in nodes:
        if n['tag'] in MASK_TAGS:
            require(not (body['start'] <= n['start'] and n['end'] <= body['end']),
                    'Administrative subtree inside substantive body is ambiguous')
            masks.append(dict(start=n['start'], end=n['end'], reason='administrative_subtree', path=n['path']))
    kind, number = re.fullmatch(r'[1-9]\d*-(hr|s)([1-9]\d*)', bill_id).groups()
    prefix = r'H\s*\.?\s*R\s*\.?' if kind == 'hr' else r'S\s*\.?'
    identity = re.compile(r'(?<![\w.])' + prefix + r'\s*' + re.escape(number) + r'(?!\w)', re.I)
    for m in identity.finditer(text):
        masks.append(dict(start=m.start(), end=m.end(), reason='focal_identity', path=None))
    masks.sort(key=lambda m: (m['start'], m['end'], m['reason']))
    cuts = {0, len(text)}
    for n in nodes:
        if n['represented_span'] or n['cell'] or n['tag'] in {'fraction', 'mfrac'}:
            cuts.update((n['start'], n['end']))
    for m in masks:
        cuts.update((m['start'], m['end']))
    cuts = sorted(cuts)
    segments = []
    for start, end in zip(cuts, cuts[1:]):
        if any(m['start'] <= start and end <= m['end'] for m in masks):
            continue
        normalized = unicodedata.normalize('NFC', text[start:end]).lower()
        tokens = WORD.findall(normalized)
        if tokens:
            segments.append(dict(start=start, end=end, text=text[start:end], tokens=tokens))
    return dict(version=VERSION, bill_id=bill_id, view_hash=view_hash,
                sidecar_hash=seal(sidecar)['hash'], text=text, masks=masks,
                token_segments=segments, token_offsets_available=False,
                historical_feature_eligible=False)


def _terms(document):
    require(isinstance(document, dict) and document.get('version') == VERSION,
            'Expected versioned prepared document')
    counts = Counter()
    for segment in document['token_segments']:
        tokens = segment['tokens']
        require(isinstance(tokens, list) and all(isinstance(t, str) and t and WORD.fullmatch(t) for t in tokens),
                'Invalid token sequence')
        counts.update((t,) for t in tokens)
        counts.update(zip(tokens, tokens[1:]))
    return counts


class CoreTfidf:
    """One-shot core-only vocabulary/IDF. No outcomes or fit_transform API."""
    def __init__(self):
        self._fitted = False

    def fit(self, documents, document_ids, roles):
        require(not self._fitted, 'Refitting forbidden; use a new fold instance')
        require(isinstance(documents, (list, tuple)) and len(documents) > 0, 'Nonempty explicit core required')
        require(len(documents) == len(document_ids) == len(roles), 'Core membership lengths differ')
        require(all(isinstance(x, str) and x for x in document_ids) and len(set(document_ids)) == len(document_ids),
                'Core IDs must be unique nonempty strings')
        require(all(role == 'core' for role in roles), 'Only core rows may fit vocabulary')
        counts = [_terms(d) for d in documents]
        df, tf = Counter(), Counter()
        for row in counts:
            df.update(row.keys())
            tf.update(row)
        n = len(counts)
        terms = [t for t in df if df[t] >= 5 and df[t] <= .95 * n]
        terms = sorted(sorted(terms, key=lambda t: (-tf[t], t))[:10000])
        require(bool(terms), 'Empty eligible vocabulary blocks preprocessing')
        self.terms_ = tuple(terms)
        self.idf_ = np.array([math.log((1 + n) / (1 + df[t])) + 1 for t in terms], dtype=np.float64)
        self.idf_.flags.writeable = False
        self.document_ids_ = tuple(document_ids)
        self.core_document_hashes_ = tuple(seal(d)['hash'] for d in documents)
        self.document_frequency_ = tuple(df[t] for t in terms)
        self._fitted = True
        return self

    def transform(self, documents):
        require(self._fitted, 'Fit core vocabulary first')
        index = {t: i for i, t in enumerate(self.terms_)}
        data, indices, indptr = [], [], [0]
        for document in documents:
            row = sorted((index[t], count * self.idf_[index[t]])
                         for t, count in _terms(document).items() if t in index)
            norm = math.sqrt(sum(float(v) ** 2 for _, v in row))
            for col, value in row:
                indices.append(col)
                data.append(value / norm)
            indptr.append(len(data))
        return csr_matrix((np.array(data, dtype=np.float64), np.array(indices, dtype=np.int32),
                           np.array(indptr, dtype=np.int32)), shape=(len(documents), len(index)))

    def manifest(self):
        require(self._fitted, 'Fit core vocabulary first')
        return dict(version=VERSION, normalization='NFC_then_lower', tokenizer='unicode_alphanumeric_without_underscore',
                    ngrams=[1, 2], min_df=5, max_df=.95, max_features=10000,
                    tf='raw_count', idf_formula='log((1+n)/(1+df))+1', norm='L2',
                    ranking='descending_core_term_frequency_then_lexicographic_tuple',
                    columns='lexicographic_tuple', document_ids=list(self.document_ids_),
                    document_hashes=list(self.core_document_hashes_),
                    terms=[list(t) for t in self.terms_], idf=self.idf_.tolist(),
                    document_frequency=list(self.document_frequency_))
