# Spectral Resilience Index

A generic Python library for topology-aware spectral resilience analysis of coupled systems.

The library provides a transparent research implementation of a bounded Spectral Resilience Index (SRI), combining system topology, operational stress, spectral radius, spectral entropy, spectral drift, and matrix conditioning.

## Install

```bash
pip install spectral-resilience-index
```

## Quick start

```python
from spectral_resilience import graph_from_edges, telemetry_features, compute_sri

nodes = ["frontend", "api", "database"]
edges = [("frontend", "api", 1.0), ("api", "database", 0.8)]
A, _ = graph_from_edges(nodes, edges)

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

## What it measures

- weighted interaction topology
- normalized operational stress
- reference interaction/Jacobian matrix
- spectral radius and stability margin
- spectral entropy
- spectral drift between states
- matrix conditioning
- bounded SRI score in `[0, 1]`

## Research status

This is a research/reference implementation, not a reliability standard. The default SRI coefficients and thresholds should be calibrated against historical incidents and controlled experiments before they are used for automated production decisions.

The next research step is an empirically estimated telemetry Jacobian:

`J_ij = d x_i(t+dt) / d x_j(t)`

The package is intentionally domain-neutral and can be applied to software, infrastructure, networks, cyber-physical systems, industrial processes, or other coupled systems represented as weighted graphs.

## Origin

This package originated from the IRISSA Spectral Resilience Index research work. The generic API is designed to make the underlying mathematics reusable independently of any single application or organization.

## License

MIT
