"""Generic operational feature normalization."""

from __future__ import annotations
import numpy as np

DEFAULT_FEATURE_WEIGHTS = {
    "latency": 0.25,
    "error_rate": 0.20,
    "retry_rate": 0.15,
    "saturation": 0.20,
    "queue_depth": 0.10,
    "resource_pressure": 0.10,
}

def _clip01(x):
    return np.clip(np.asarray(x, dtype=float), 0.0, 1.0)

def telemetry_features(latency, error_rate, retry_rate, saturation,
                       queue_depth=0.0, resource_pressure=0.0, weights=None):
    """Return normalized stress features and a weighted stress score."""
    w = dict(DEFAULT_FEATURE_WEIGHTS)
    if weights:
        w.update(weights)
    x = np.array([_clip01(latency), _clip01(error_rate), _clip01(retry_rate),
                  _clip01(saturation), _clip01(queue_depth), _clip01(resource_pressure)], dtype=float)
    weight_vec = np.array([w["latency"], w["error_rate"], w["retry_rate"],
                           w["saturation"], w["queue_depth"], w["resource_pressure"]], dtype=float)
    if weight_vec.sum() <= 0:
        raise ValueError("Feature weights must sum to a positive value.")
    weight_vec /= weight_vec.sum()
    return x, float(weight_vec @ x)
