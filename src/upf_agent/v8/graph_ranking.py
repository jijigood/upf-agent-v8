"""Bounded pure-Python PageRank: no SciPy dependency and no graph-source rescanning."""

from math import isfinite


def personalized_pagerank(
    node_ids, edges, seeds, *, alpha=0.85, tolerance=1e-8, max_iterations=1000
):
    """Undirected, unweighted simple adjacency; uniform personalization over accepted roots.

    Dangling mass follows the same personalization. Stop on absolute global L1 residual,
    not N*tolerance. Failed convergence returns no usable scores, never partial success.
    """
    if not isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("alpha must be finite and between 0 and 1")
    if not isfinite(tolerance) or not 0 < tolerance < 1 or max_iterations < 1:
        raise ValueError("positive finite tolerance and iteration budget required")
    nodes = sorted(set(node_ids))
    roots = sorted(set(seeds) & set(nodes))
    if not roots:
        return {
            "status": "no_valid_seed",
            "converged": False,
            "iterations": 0,
            "residual": None,
            "scores": {},
            "ranking_edge_visits": 0,
        }
    adjacency = {n: set() for n in nodes}
    for left, right in edges:
        if left not in adjacency or right not in adjacency:
            raise ValueError("ranked edge outside filtered candidate graph")
        adjacency[left].add(right)
        adjacency[right].add(left)
    personalization = {n: 1 / len(roots) if n in roots else 0.0 for n in nodes}
    previous = dict(personalization)
    visits, residual = 0, None
    for iteration in range(1, max_iterations + 1):
        dangling = sum(previous[n] for n in nodes if not adjacency[n])
        current = {n: (1 - alpha + alpha * dangling) * personalization[n] for n in nodes}
        for node in nodes:
            if adjacency[node]:
                value = alpha * previous[node] / len(adjacency[node])
                for neighbor in sorted(adjacency[node]):
                    current[neighbor] += value
                    visits += 1
        residual = sum(abs(current[n] - previous[n]) for n in nodes)
        if residual <= tolerance:
            return {
                "status": "converged",
                "converged": True,
                "iterations": iteration,
                "residual": residual,
                "scores": current,
                "ranking_edge_visits": visits,
            }
        previous = current
    return {
        "status": "not_converged",
        "converged": False,
        "iterations": max_iterations,
        "residual": residual,
        "scores": {},
        "ranking_edge_visits": visits,
    }
