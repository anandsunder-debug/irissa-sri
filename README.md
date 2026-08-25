# IRISSA SRI

A research/reference Python library for a telemetry- and topology-based
Spectral Resilience Index (SRI) for distributed software systems.

## What it does

The initial implementation provides:

- weighted service dependency graphs
- normalized telemetry stress
- a transparent reference system/Jacobian matrix
- eigenvalue and spectral-radius analysis
- spectral entropy
- spectral drift between runtime states
- a bounded SRI score in `[0, 1]`
- warnings for threshold crossing, drift, stress, and conditioning

## Important research status

This package is **not a production reliability standard** and the SRI formula is
a research scaffold. Before using it for automated rollback, capacity changes,
or incident prevention, calibrate its coefficients and thresholds against
historical production incidents and controlled experiments.

The key next step is replacing the reference matrix in `build_system_matrix()`
with an empirically estimated telemetry Jacobian:

    J_ij = d x_i(t+dt) / d x_j(t)

Then validate whether changes in spectral properties lead conventional incident
signals.

## Quick start

```python
from irissa_sri import graph_from_edges, telemetry_features, compute_sri

nodes = ["frontend", "api", "db"]
edges = [
    ("frontend", "api", 1.0),
    ("api", "db", 0.8),
]

A, index = graph_from_edges(nodes, edges)

_, stress = telemetry_features(
    latency=0.35,
    error_rate=0.05,
    retry_rate=0.10,
    saturation=0.45,
    queue_depth=0.20,
    resource_pressure=0.30,
)

result = compute_sri(A, stress=stress)

print(result.sri)
print(result.spectral_radius)
print(result.warnings)
```

## Enterprise integration roadmap

1. OpenTelemetry receiver/processor
2. Prometheus exporter
3. Kubernetes topology discovery
4. Chaos Mesh validation harness
5. Argo Rollouts analysis provider
6. Historical incident calibration
7. Production-safe recommendation mode
8. Only then consider automated remediation

## Research questions

- Does SRI predict cascading failures earlier than conventional thresholds?
- Which spectral feature is most predictive of failure?
- Does topology-aware SRI outperform metric-only anomaly detection?
- How stable is SRI across workloads and architectures?
- Can SRI reduce unnecessary capacity headroom without increasing incidents?

**Standalone package:** this repository is independent of the existing application repository.
