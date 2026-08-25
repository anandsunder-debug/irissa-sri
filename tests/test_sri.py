import numpy as np
from irissa_sri import compute_sri, graph_from_edges, telemetry_features

def test_graph_and_sri_are_bounded():
    A, idx = graph_from_edges(
        ["frontend", "api", "db"],
        [("frontend", "api", 1.0), ("api", "db", 0.8)]
    )
    result = compute_sri(A, stress=0.2)
    assert 0.0 <= result.sri <= 1.0
    assert result.spectral_radius >= 0.0
    assert len(result.eigenvalues) == 3

def test_telemetry_stress():
    _, stress = telemetry_features(
        latency=0.8, error_rate=0.1, retry_rate=0.2,
        saturation=0.7, queue_depth=0.4, resource_pressure=0.5
    )
    assert 0.0 <= stress <= 1.0

def test_drift():
    A = np.array([[0, 1], [1, 0]], dtype=float)
    r1 = compute_sri(A, stress=0.1)
    r2 = compute_sri(A * 1.5, stress=0.5, previous_eigenvalues=r1.eigenvalues)
    assert r2.spectral_drift >= 0.0
