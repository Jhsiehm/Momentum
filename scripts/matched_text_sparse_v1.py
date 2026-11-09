"""Research-only sparse logistic solver; no I/O, calibration, or automatic retries.

Objective: mean logistic NLL + (0.05 / 2) * ||slopes||². Theta[0] is
an unpenalized intercept. Structured scaling is learned only from the explicitly
passed training-core matrix; callers own split/source eligibility. Text must
already have training-only vocabulary/IDF and row normalization. This module
never standardizes text columns. No real-data experiment is authorized here.

All SciPy L-BFGS-B settings are pinned below before any registered experiment.
A solver success alone is insufficient: finite output and an independently
recomputed gradient infinity norm <= 1e-6 are also required. Failure is returned
without retry or fallback. Runtime versions are included in every fit result.
"""
from __future__ import annotations

import numpy as np
import scipy
from scipy import sparse
from scipy.optimize import minimize
from scipy.special import expit

VERSION = "matched-text-sparse-v1"
L2 = 0.05
GRADIENT_TOLERANCE = 1e-6
SCALING_FLOOR = 0.1
STRUCTURED_COLUMNS = 6
SOLVER_OPTIONS = {
    "maxiter": 20000,
    "gtol": GRADIENT_TOLERANCE,
    "ftol": 0.0,
    "maxfun": 1000000,
    "maxls": 50,
    "maxcor": 10,
}


def _numeric_array(value, name):
    arr = np.asarray(value)
    if arr.dtype.kind not in "iuf":
        raise ValueError(f"{name} must contain real numeric values (not booleans)")
    arr = np.asarray(arr, dtype=np.float64)
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must be finite")
    return arr


def _matrix(X):
    if not sparse.issparse(X) or X.ndim != 2:
        raise ValueError("X must be a two-dimensional sparse matrix")
    if X.dtype.kind not in "iuf":
        raise ValueError("X must contain real numeric values")
    # A copy avoids canonicalization mutating the caller's sparse input.
    X = sparse.csr_matrix(X, dtype=np.float64, copy=True)
    X.sum_duplicates()
    X.sort_indices()
    if X.shape[0] == 0 or not np.all(np.isfinite(X.data)):
        raise ValueError("X must have rows and finite entries")
    return X


def _labels(y, n):
    y = _numeric_array(y, "y")
    if y.ndim != 1 or len(y) != n or not np.all((y == 0) | (y == 1)):
        raise ValueError("y must be a binary vector matching X rows")
    if np.unique(y).size != 2:
        raise ValueError("y must contain both classes")
    return y


def _evaluate(theta, X, y):
    """Stable objective and gradient on validated arrays, never densifying X."""
    z = np.asarray(X @ theta[1:]).reshape(-1) + theta[0]
    # logaddexp(0, signed logit) avoids inf-inf for confidently correct labels.
    signed = np.where(y == 1, -z, z)
    objective = float(np.mean(np.logaddexp(0.0, signed)) + L2 / 2 * np.dot(theta[1:], theta[1:]))
    residual = np.where(y == 1, -expit(-z), expit(z))
    grad = np.concatenate(([np.mean(residual)], np.asarray(X.T @ residual).reshape(-1) / len(y) + L2 * theta[1:]))
    return objective, grad


def objective_gradient(theta, X, y):
    """Return scalar objective and gradient; zero feature columns are allowed."""
    X = _matrix(X)
    y = _labels(y, X.shape[0])
    theta = _numeric_array(theta, "theta")
    if theta.ndim != 1 or theta.size != X.shape[1] + 1:
        raise ValueError("theta must contain intercept followed by one slope per column")
    return _evaluate(theta, X, y)


def fit(X, y):
    """One deterministic zero-initialized optimization, returning auditable status.

    Do not consume coefficients for prediction unless accepted is True. Numerical
    failure remains explicit, including scipy success with inadequate gradient.
    Exceptions due to invalid inputs are raised before optimization.
    """
    X = _matrix(X)
    y = _labels(y, X.shape[0])
    result = minimize(
        _evaluate, np.zeros(X.shape[1] + 1), args=(X, y), jac=True,
        method="L-BFGS-B", bounds=None, options=dict(SOLVER_OPTIONS),
    )
    theta = np.asarray(result.x, dtype=np.float64)
    # Recompute directly from the returned parameters, independently of the
    # optimizer's cached fun/jac and the optimization callback.
    with np.errstate(over="ignore", invalid="ignore"):
        logits = np.asarray(X.dot(theta[1:])).reshape(-1) + theta[0]
        signs = 1.0 - 2.0 * y
        residual = signs * expit(signs * logits)
        gradient = np.empty(theta.size)
        gradient[0] = residual.sum() / len(y)
        gradient[1:] = np.asarray(X.transpose().dot(residual)).reshape(-1) / len(y) + L2 * theta[1:]
        objective = float(np.logaddexp(0.0, signs * logits).sum() / len(y) + (L2 / 2) * (theta[1:] ** 2).sum())
    finite = bool(np.all(np.isfinite(theta)) and np.isfinite(objective) and np.all(np.isfinite(gradient)))
    norm = float(np.max(np.abs(gradient))) if finite else None
    accepted = bool(result.success and finite and norm <= GRADIENT_TOLERANCE)
    return {
        "version": VERSION,
        "numpy_version": np.__version__, "scipy_version": scipy.__version__,
        "objective_definition": "mean_logistic_nll_plus_0.05_over_2_times_squared_slopes",
        "l2": L2, "intercept_penalized": False,
        "method": "L-BFGS-B", "bounds": None, "initialization": "all_zero",
        "options": dict(SOLVER_OPTIONS),
        "rows": X.shape[0], "columns": X.shape[1], "nonzero_entries": X.nnz,
        "parameters": theta.tolist() if np.all(np.isfinite(theta)) else None,
        "objective": objective if np.isfinite(objective) else None,
        "gradient_infinity_norm": norm,
        "optimizer_success": bool(result.success), "optimizer_status": int(result.status),
        "optimizer_message": str(result.message), "iterations": int(result.nit),
        "function_evaluations": int(result.nfev), "gradient_evaluations": int(result.njev),
        "finite": finite, "accepted": accepted,
        "status": "converged" if accepted else "nonconverged",
        "attempts": 1,
    }


def _structured(values):
    arr = _numeric_array(values, "structured values")
    if arr.ndim != 2 or arr.shape[1] != STRUCTURED_COLUMNS or arr.shape[0] == 0:
        raise ValueError("structured values must have rows and exactly six columns")
    return arr


def fit_structured_scaler(training_core):
    """Compute population standard deviations on the passed training core only."""
    arr = _structured(training_core)
    with np.errstate(over="ignore", invalid="ignore"):
        means = arr.mean(axis=0)
        scales = np.maximum(arr.std(axis=0, ddof=0), SCALING_FLOOR)
    if not np.all(np.isfinite(means)) or not np.all(np.isfinite(scales)):
        raise ValueError("structured scaling overflow")
    return {"version": VERSION, "columns": STRUCTURED_COLUMNS, "training_rows": len(arr),
            "ddof": 0, "floor": SCALING_FLOOR, "means": means.tolist(), "scales": scales.tolist()}


def transform_structured(values, scaler):
    """Apply frozen training-core scaling; return CSR without fitting anything."""
    arr = _structured(values)
    if not isinstance(scaler, dict) or scaler.get("version") != VERSION or scaler.get("columns") != STRUCTURED_COLUMNS or scaler.get("ddof") != 0 or scaler.get("floor") != SCALING_FLOOR:
        raise ValueError("invalid scaler metadata")
    means = _numeric_array(scaler.get("means"), "scaler means")
    scales = _numeric_array(scaler.get("scales"), "scaler scales")
    if means.shape != (STRUCTURED_COLUMNS,) or scales.shape != (STRUCTURED_COLUMNS,) or np.any(scales < SCALING_FLOOR):
        raise ValueError("invalid scaler vectors")
    with np.errstate(over="ignore", invalid="ignore"):
        transformed = (arr - means) / scales
    if not np.all(np.isfinite(transformed)):
        raise ValueError("structured transformation overflow")
    return sparse.csr_matrix(transformed)


def combine_features(structured_values, scaler, normalized_text):
    """Append already-normalized sparse text unchanged to scaled six columns.

    Each text row must have L2 norm 1 (tolerance 1e-10) or 0. Zero rows allow
    held-out documents with no training-vocabulary terms. Negative TF-IDF is
    rejected. No centering, rescaling, vocabulary, or IDF fitting occurs here.
    """
    structured = transform_structured(structured_values, scaler)
    text = _matrix(normalized_text)
    if text.shape[0] != structured.shape[0] or np.any(text.data < 0):
        raise ValueError("text must have matching rows and nonnegative entries")
    with np.errstate(over="ignore", invalid="ignore"):
        norm_squared = np.asarray(text.multiply(text).sum(axis=1)).reshape(-1)
    if not np.all((norm_squared == 0) | np.isclose(norm_squared, 1.0, rtol=0, atol=1e-10)):
        raise ValueError("text rows must be L2-normalized or empty")
    return sparse.hstack((structured, text), format="csr")
