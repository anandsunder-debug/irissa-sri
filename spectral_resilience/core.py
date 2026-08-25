"""Generic Spectral Resilience Index calculations."""

from __future__ import annotations
from dataclasses import dataclass, asdict
import numpy as np
from scipy.linalg import eigvals

@dataclass
class SRIResult:
    sri: float
    stability_margin: float
    spectral_radius: float
    dominant_eigenvalue: complex
    spectral_gap: float
    spectral_entropy: float
    stress: float
    spectral_drift: float
    condition_number: float
    eigenvalues: list
    warnings: list

    def to_dict(self):
        return asdict(self)

def _normalize_spectrum(eigenvalues):
    magnitudes = np.abs(np.asarray(eigenvalues, dtype=float))
    total = magnitudes.sum()
    if total <= 0:
        return np.ones_like(magnitudes) / max(1, len(magnitudes))
    return magnitudes / total

def spectral_entropy(eigenvalues):
    """Normalized Shannon entropy of eigenvalue magnitudes."""
    p = _normalize_spectrum(eigenvalues)
    h = -float(np.sum(p * np.log(p + 1e-15)))
    return float(h / np.log(len(p))) if len(p) > 1 else 0.0

def build_system_matrix(adjacency, stress=0.0, coupling=1.0, damping=0.25):
    """Build a reference discrete-time interaction/Jacobian matrix."""
    A = np.asarray(adjacency, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("adjacency must be square")
    n = A.shape[0]
    if n == 0:
        raise ValueError("adjacency cannot be empty")
    scale = max(float(np.max(np.sum(np.abs(A), axis=1))), 1e-12)
    An = A / scale
    return (1.0 - float(damping)) * np.eye(n) + float(coupling) * (1.0 + float(stress)) * An

def compute_sri(adjacency, stress=0.0, previous_eigenvalues=None,
                coupling=1.0, damping=0.25, target_radius=1.0):
    """Compute a bounded research SRI in [0, 1].

    The default coefficients are transparent reference values and should be
    calibrated against domain-specific historical data before automation.
    """
    J = build_system_matrix(adjacency, stress, coupling, damping)
    vals = eigvals(J)
    mags = np.abs(vals)
    radius = float(np.max(mags))
    margin = max(0.0, 1.0 - radius / max(target_radius, 1e-12))
    entropy = spectral_entropy(vals)

    if previous_eigenvalues is None:
        drift = 0.0
    else:
        old = np.sort_complex(np.asarray(previous_eigenvalues, dtype=complex))
        new = np.sort_complex(vals)
        if len(old) != len(new):
            raise ValueError("previous_eigenvalues must have the same dimension.")
        drift = float(np.linalg.norm(np.abs(new) - np.abs(old)) /
                      max(np.linalg.norm(np.abs(old)), 1e-12))

    cond = float(np.linalg.cond(J))
    margin_score = np.clip(margin, 0.0, 1.0)
    drift_score = np.exp(-2.0 * max(0.0, drift))
    entropy_score = 1.0 - np.clip(entropy, 0.0, 1.0)
    stress_score = 1.0 - np.clip(float(stress), 0.0, 1.0)
    sri = float(np.clip(0.45 * margin_score + 0.20 * drift_score +
                        0.15 * entropy_score + 0.20 * stress_score, 0.0, 1.0))

    warnings = []
    if radius >= target_radius:
        warnings.append("spectral_radius_at_or_above_threshold")
    if drift > 0.10:
        warnings.append("material_spectral_drift")
    if stress > 0.80:
        warnings.append("high_operational_stress")
    if cond > 1e8:
        warnings.append("ill_conditioned_system_matrix")

    return SRIResult(
        sri=sri,
        stability_margin=float(margin),
        spectral_radius=radius,
        dominant_eigenvalue=complex(vals[np.argmax(mags)]),
        spectral_gap=float(np.max(mags) - np.partition(mags, -2)[-2]) if len(mags) > 1 else radius,
        spectral_entropy=entropy,
        stress=float(np.clip(stress, 0.0, 1.0)),
        spectral_drift=drift,
        condition_number=cond,
        eigenvalues=[complex(v) for v in vals],
        warnings=warnings,
    )
