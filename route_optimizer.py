"""Nearest-Neighbor TSP approximation using Dijkstra distances."""
import math
from graph_algorithms import dijkstra, reconstruct_path

def nearest_neighbor_route(graph, depot, destinations):
    """Build an approximate closed tour and expand legs into road paths.

    Returns a dictionary with visit_order, expanded_path, distance and legs.
    Unreachable destinations are reported in unreachable and omitted from tour.
    """
    if depot not in graph:
        raise ValueError(f"Unknown depot: {depot}")
    remaining = set(destinations)
    remaining.discard(depot)
    visit_order = [depot]
    expanded_path = [depot]
    legs = []
    total = 0.0
    current = depot
    while remaining:
        distances, previous = dijkstra(graph, current)
        reachable = [node for node in remaining if distances.get(node, math.inf) < math.inf]
        if not reachable:
            break
        next_node = min(reachable, key=lambda node: (distances[node], node))
        leg_path = reconstruct_path(previous, current, next_node)
        leg_distance = distances[next_node]
        legs.append({"from": current, "to": next_node, "distance": leg_distance, "path": leg_path})
        expanded_path.extend(leg_path[1:])
        total += leg_distance
        visit_order.append(next_node)
        remaining.remove(next_node)
        current = next_node
    if current != depot:
        distances, previous = dijkstra(graph, current)
        if distances.get(depot, math.inf) < math.inf:
            leg_path = reconstruct_path(previous, current, depot)
            leg_distance = distances[depot]
            legs.append({"from": current, "to": depot, "distance": leg_distance, "path": leg_path})
            expanded_path.extend(leg_path[1:])
            total += leg_distance
            visit_order.append(depot)
    return {"visit_order": visit_order, "expanded_path": expanded_path,
            "distance": total, "legs": legs, "unreachable": sorted(remaining)}
