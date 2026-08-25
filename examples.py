from irissa_sri import graph_from_edges, telemetry_features, compute_sri

nodes = ["frontend", "api", "db"]
edges = [("frontend", "api", 1.0), ("api", "db", 0.8)]
A, _ = graph_from_edges(nodes, edges)

_, stress = telemetry_features(
    latency=0.35, error_rate=0.05, retry_rate=0.10,
    saturation=0.45, queue_depth=0.20, resource_pressure=0.30
)

r = compute_sri(A, stress=stress)
print(r.to_dict())
