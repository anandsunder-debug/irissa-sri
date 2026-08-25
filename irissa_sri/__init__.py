"""IRISSA Spectral Resilience Index reference library."""

from .core import SRIResult, compute_sri, build_system_matrix
from .topology import graph_from_edges, weighted_adjacency, laplacian
from .features import telemetry_features

__version__ = "0.1.0"

__all__ = [
    "SRIResult",
    "compute_sri",
    "build_system_matrix",
    "graph_from_edges",
    "weighted_adjacency",
    "laplacian",
    "telemetry_features",
]
