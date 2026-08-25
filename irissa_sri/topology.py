"""Topology and graph utilities for distributed software systems."""

from __future__ import annotations
import numpy as np

def graph_from_edges(nodes, edges):
    """Return a symmetric weighted adjacency matrix.

    Parameters
    ----------
    nodes : sequence[str]
        Node/service names.
    edges : iterable
        Tuples (source, target, weight). Undirected representation is used
        for the reference SRI model.
    """
    nodes = list(nodes)
    idx = {n: i for i, n in enumerate(nodes)}
    A = np.zeros((len(nodes), len(nodes)), dtype=float)
    for source, target, weight in edges:
        if source not in idx or target not in idx:
            raise ValueError("Edge contains a node not present in nodes.")
        if source == target:
            continue
        w = float(weight)
        if w < 0:
            raise ValueError("Edge weights must be non-negative.")
        i, j = idx[source], idx[target]
        A[i, j] += w
        A[j, i] += w
    return A, idx

def weighted_adjacency(nodes, edges):
    return graph_from_edges(nodes, edges)[0]

def laplacian(A):
    """Weighted graph Laplacian D-A."""
    A = np.asarray(A, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A must be a square matrix.")
    return np.diag(A.sum(axis=1)) - A
