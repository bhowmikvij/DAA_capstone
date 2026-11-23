"""Weighted undirected graph and Dijkstra shortest paths."""
import math

def build_graph(edges):
    graph = {}
    for source, target, distance in edges:
        distance = float(distance)
        if distance < 0:
            raise ValueError("Dijkstra requires non-negative edge weights")
        graph.setdefault(source, {})
        graph.setdefault(target, {})
        graph[source][target] = min(distance, graph[source].get(target, math.inf))
        graph[target][source] = min(distance, graph[target].get(source, math.inf))
    return graph

def dijkstra(graph, start):
    """Return distance and predecessor dictionaries from start."""
    if start not in graph:
        raise ValueError(f"Unknown start node: {start}")
    distances = {node: math.inf for node in graph}
    previous = {node: None for node in graph}
    unvisited = set(graph)
    distances[start] = 0.0
    while unvisited:
        current = min(unvisited, key=lambda node: distances[node])
        if distances[current] == math.inf:
            break
        unvisited.remove(current)
        for neighbor, weight in graph[current].items():
            if neighbor in unvisited:
                candidate = distances[current] + weight
                if candidate < distances[neighbor]:
                    distances[neighbor] = candidate
                    previous[neighbor] = current
    return distances, previous

def reconstruct_path(previous, start, target):
    if target == start:
        return [start]
    if target not in previous:
        return []
    path, current = [], target
    while current is not None:
        path.append(current)
        if current == start:
            return list(reversed(path))
        current = previous[current]
    return []
