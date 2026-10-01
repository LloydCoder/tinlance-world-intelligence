"""Bounded, cycle-safe graph traversal."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Edge:
    source: str
    target: str
    predicate: str
    confidence: float

@dataclass(frozen=True, slots=True)
class GraphPath:
    nodes: tuple[str, ...]
    predicates: tuple[str, ...]

def bounded_paths(edges: list[Edge], start: str, *, max_depth: int = 3) -> tuple[GraphPath, ...]:
    if max_depth < 0:
        raise ValueError("max_depth must be non-negative")
    adjacency: dict[str, list[Edge]] = {}
    for edge in edges:
        if not 0 <= edge.confidence <= 1:
            raise ValueError("edge confidence must be 0..1")
        adjacency.setdefault(edge.source, []).append(edge)
    results: list[GraphPath] = []
    stack: list[tuple[str, tuple[str, ...], tuple[str, ...]]] = [(start, (start,), ())]
    while stack:
        node, nodes, predicates = stack.pop()
        if len(predicates) >= max_depth:
            continue
        for edge in adjacency.get(node, []):
            if edge.target in nodes:
                continue
            next_nodes = nodes + (edge.target,)
            next_predicates = predicates + (edge.predicate,)
            results.append(GraphPath(next_nodes, next_predicates))
            stack.append((edge.target, next_nodes, next_predicates))
    return tuple(results)
