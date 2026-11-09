"""Freeze an outcome-blind E3 specification; deliberately cannot release fitting."""
import argparse
import hashlib
import json
import re
from pathlib import Path

from engine.paper_evaluation import require, seal, unseal
from engine.store import ROOT, digest

SOURCE = ROOT/'data/research-runs/exploratory-calendar-20261108-v1/registration.json'
SOURCE_SEAL = 'b61d21f14255b73ee55573f78865114c0646ef748bc1f9dc0c22af440e108200'
FILES = (
    'scripts/freeze_matched_text_comparison_v1.py',
    'tests/test_matched_text_comparison_v1.py',
    'docs/research/MATCHED_TEXT_COMPARISON_V1.md',
    'docs/research/BILL_CONTEXT_EXPERIMENT_PLAN_V1.md',
    'docs/research/BILL_CONTEXT_METHODS_CLARIFICATION_V1.md',
    'docs/research/PAPER_PROTOCOL_V1.md',
    'engine/paper_evaluation.py', 'engine/store.py',
)
ROLES = ('core_ids', 'calibration_ids', 'evaluation_ids')
GATES = {
    'historical_introduced_text': 'Exact historical rendition/availability evidence is not certified for the planned populations; an eight-case feasibility result cannot certify them.',
    'source_family_outcome_reviews': 'Required subject-bound qualified source, family and outcome reviews remain pending; agent agreement is not certification.',
    'positive_family_scope': 'Methods signoff must name the exact applicable populations before testing 200 reviewed positive training / 100 development families; overlapping folds cannot be summed.',
    'temporal_and_family_eligibility': 'Identity-only membership does not establish label availability, negative coverage, at-risk cutoffs or global-family disjointness.',
    'eligible_matched_membership': 'Freeze source-eligible arm-common core/calibration/evaluation rows and every exclusion before scoring; none is certified here.',
    'core_calibration_classes': 'Both classes required in core and calibration; class adequacy cannot be certified by identity-only manifests.',
    'text_preprocessing': 'Exact Unicode normalization, tokenization and tested focal-identifier/status masking implementation require a separate pre-fit code freeze; negation/substantive statute references must survive.',
    'sparse_numerical_verification': 'Pin research dependencies and sparse objective/solver implementation; independent scalar equivalence, deterministic replay and convergence fixtures must pass.',
    'storage_runtime_preflight': 'Source coverage, memory/storage and six-hour runtime preflight must be documented; no dependency-installation budget assumed.',
    'execution_registration': 'A subsequent sealed execution registration must bind all accepted evidence, exact eligible rows, exposure, complete feature/solver code and remaining programme budget before any fit.',
}


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def memberships_only(source):
    """Copy only registered identity fields; never load row features or outcomes."""
    require(set(source.get('memberships', {})) == {'115', '116', '117'}, 'Three exact folds required')
    result = {}
    for fold, original in sorted(source['memberships'].items()):
        require(set(original) == set(ROLES), 'Unexpected membership fields')
        result[fold] = {}
        used = set()
        for role in ROLES:
            ids = original[role]
            require(isinstance(ids, list) and bool(ids), 'Nonempty identity list required')
            require(all(isinstance(i, str) and re.fullmatch(r'\d+-(hr|s)[1-9]\d*', i) for i in ids), 'Invalid identity')
            require(len(ids) == len(set(ids)), 'Duplicate identity')
            require(not used.intersection(ids), 'Within-fold partition overlap')
            used.update(ids)
            for bill in ids:
                congress = int(bill.split('-')[0])
                require(congress == int(fold) if role == 'evaluation_ids' else 113 <= congress < int(fold), 'Invalid temporal Congress membership')
            result[fold][role] = list(ids)
    return result


def specification(source):
    membership = memberships_only(source)
    counts = {fold: {role: len(ids) for role, ids in rows.items()} for fold, rows in membership.items()}
    return dict(
        version='matched-text-comparison-specification-v1', status='blocked_specification_only',
        hypothesis='Introduced bill language lowers calibrated Brier loss beyond the six-feature anchor on identical eligible cases.',
        study='E3 exposed-development text comparison, Congresses 115–117',
        arms=['anchor_sparse', 'anchor_plus_introduced_text_sparse'],
        descriptor_arm='Excluded because E2 descriptor quality has not passed; cannot add it after scores.',
        planned_memberships=membership, planned_membership_hash=digest(membership), planned_counts=counts,
        eligible_memberships=None, eligible_counts=None, eligibility_unknown_is_false=True,
        arms_share_one_membership=True, fit_cap=6, fits_per_fold=2, actual_fits=0,
        overall_programme_cap=75, wallclock_cap_seconds=21600,
        full_text_retained=True, structure_sidecars='Retained as context; not additional predictive columns in this contrast.',
        text=dict(version='introduced only', normalization='Unicode normalization; exact implementation pending',
                  lowercase=True, ngram_range=[1, 2], min_df=5, max_df=0.95, max_features=10000,
                  idf_fit_partition='core only', vocabulary_fit_partition='core only', norm='l2',
                  stemming=False, generic_stopwords=False, retain_negation=True,
                  masking='Focal bill identifier and status boilerplate; exact tested rule pending; preserve substantive statutory citations.',
                  text_scaling='No centering or variance standardization', embeddings=False),
        structured=dict(width=6, fit_partition='core only', scale_floor=0.1),
        objective=dict(loss='mean negative log likelihood', slope_l2=0.05, intercept_penalized=False),
        solver=dict(method='deterministic sparse L-BFGS for both arms', max_iterations=20000,
                    max_absolute_gradient=1e-6, minimum_iterations=None, hyperparameter_search=False,
                    failure='Any nonconverged comparison blocked; no outcome-dependent cap extension'),
        calibration=dict(method='existing monotone affine-logit', steps=2000,
                         partition='identical earlier disjoint calibration families per arm', both_classes_required=True),
        baselines=dict(rate='Beta(1,1) on eligible core plus calibration',
                       stage='(stage positives + 5 * global rate) / (stage n + 5), stages 0–3'),
        metrics=['raw/calibrated Brier', 'log loss', 'BSS rate', 'BSS stage', 'fixed-decile reliability and counts',
                 'expected events', 'positive/negative Brier', 'event/family counts', 'coverage/exclusions'],
        aggregate='Equal-period mean losses; BSS is ratio of mean losses; pooled bill-weighted loss secondary',
        lead_rule='Calibrated Brier strictly improves and log loss does not worsen in every required fold; a blocked fold blocks lead selection.',
        uncertainty=dict(method='paired global-family bootstrap', draws=10000, seed=20261105,
                         minimum_valid_draws=9000, invalid_draw='empty period; retain count',
                         interpretation='descriptive conditional intervals, not selection-adjusted independent confirmation'),
        gates={name: dict(status='unknown', satisfied=False, reason=reason) for name, reason in GATES.items()},
        predictive_execution_permitted=False, human_certified=False, independent_validation=False,
        limitations=['Previously exposed folds; identity-only freezing cannot remove development exposure.',
                     'No predictive score, label count or class-balance inspection is performed.',
                     'No 60% claim; any confirmatory contrast needs separate prior multiplicity/custody registration.'])


def freeze(directory, feasibility_result=None):
    directory = Path(directory).resolve()
    require((ROOT/'data').resolve() in directory.parents, 'Output must be beneath data/')
    require(not directory.exists(), 'Output must be new')
    source_bytes = SOURCE.read_bytes()
    source_envelope = json.loads(source_bytes)
    source = unseal(source_envelope)
    require(source_envelope['hash'] == SOURCE_SEAL, 'Unexpected source registration')
    files = {p: file_hash(ROOT/p) for p in FILES}
    inputs = {str(SOURCE.relative_to(ROOT)): hashlib.sha256(source_bytes).hexdigest()}
    if feasibility_result is not None:
        path = Path(feasibility_result).resolve()
        require((ROOT/'data').resolve() in path.parents, 'Feasibility input must be under data/')
        raw = path.read_bytes()
        unseal(json.loads(raw))
        inputs[str(path.relative_to(ROOT))] = hashlib.sha256(raw).hexdigest()
    body = specification(source)
    registration = seal(dict(kind='specification_freeze_not_execution_release', source_registration_hash=SOURCE_SEAL,
                             files=files, inputs=inputs, specification=body))
    directory.mkdir(parents=True, exist_ok=False)
    (directory/'registration.json').write_text(json.dumps(registration, sort_keys=True, indent=2)+'\n')
    require(all(file_hash(ROOT/p) == h for p,h in files.items()), 'Code changed during freeze')
    require(all(file_hash(ROOT/p) == h for p,h in inputs.items()), 'Input changed during freeze')
    result = seal(dict(registration_hash=registration['hash'], status='blocked',
                       gate_count=len(GATES), satisfied_gates=0, unknown_gates=len(GATES),
                       planned_counts=body['planned_counts'], eligible_counts=None,
                       actual_fits=0, predictive_tests=0, outcomes_loaded=False,
                       source_calendaring_exceptions_inherited=False,
                       next_action='Resolve evidence and implementation gates, then separately freeze eligible execution; do not fit from this specification.'))
    (directory/'result.json').write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory')
    parser.add_argument('--feasibility-result')
    args = parser.parse_args()
    print(json.dumps(freeze(args.directory, args.feasibility_result), sort_keys=True))
