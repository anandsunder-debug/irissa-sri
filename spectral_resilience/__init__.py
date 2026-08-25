"""Generic Spectral Resilience Index (SRI) library.

A domain-neutral research implementation for analysing stability,
operational stress, topology, spectral drift, and resilience in coupled
systems.
"""

from .core import SRIResult, compute_sri, build_system_matrix, spectral_entropy
from .topology import graph_from_edges, weighted_adjacency, laplacian
from .features import telemetry_features

__version__ = "0.2.0"

__all__ = [
    "SRIResult",
    "compute_sri",
    "build_system_matrix",
    "spectral_entropy",
    "graph_from_edges",
    "weighted_adjacency",
    "laplacian",
    "telemetry_features",
]
