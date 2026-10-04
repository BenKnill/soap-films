"""Exhaust all labelled full Steiner topologies; solve each convex SOCP.

Collapsed edges are allowed, so non-full optimal trees are included too.
The scoring reference is an interval from feasible primal and dual solutions,
not the solver's termination flag or the film simulation's best dip.
"""
import json
import sys

import clarabel
import numpy as np
from scipy import sparse


def topologies(n):
    trees = [[(0, n), (1, n), (2, n)]]
    for pin in range(3, n):
        junction = n + pin - 2
        trees = [edges[:i] + edges[i + 1:] + [(a, junction),
                 (b, junction), (pin, junction)]
                 for edges in trees for i, (a, b) in enumerate(edges)]
    return trees


def solve_topology(pins, edges):
    n, m, k = len(pins), len(edges), len(pins) - 2
    incidence = np.zeros((m, k))
    fixed = np.zeros((m, 2))
    for i, (a, b) in enumerate(edges):
        for node, sign in ((a, 1), (b, -1)):
            if node < n:
                fixed[i] += sign * pins[node]
            else:
                incidence[i, node - n] += sign
    # s = b - A*x = (edge length bound, edge displacement) in SOC(3).
    A = np.zeros((3 * m, 2 * k + m))
    rhs = np.zeros(3 * m)
    for i in range(m):
        A[3 * i, 2 * k + i] = -1
        A[3 * i + 1, :k] = -incidence[i]
        A[3 * i + 2, k:2 * k] = -incidence[i]
        rhs[3 * i + 1:3 * i + 3] = fixed[i]
    settings = clarabel.DefaultSettings()
    settings.verbose = False
    settings.max_iter = 200
    settings.tol_gap_abs = settings.tol_gap_rel = settings.tol_feas = 1e-10
    solver = clarabel.DefaultSolver(
        sparse.csc_matrix((2 * k + m, 2 * k + m)),
        np.r_[np.zeros(2 * k), np.ones(m)], sparse.csc_matrix(A), rhs,
        [clarabel.SecondOrderConeT(3) for _ in edges], settings)
    sol = solver.solve()
    if str(sol.status) not in ('Solved', 'AlmostSolved'):
        raise RuntimeError(f'SOCP failed: {sol.status}')
    x = np.asarray(sol.x)
    junctions = np.column_stack((x[:k], x[k:2 * k]))
    upper = np.linalg.norm(fixed + incidence @ junctions, axis=1).sum()
    flow = np.asarray(sol.z).reshape(m, 3)[:, 1:].copy()
    # Repair stationarity, then scale into the unit disks. Weak duality gives
    # -sum(fixed * flow) <= every embedding of this topology.
    flow -= incidence @ np.linalg.solve(incidence.T @ incidence,
                                       incidence.T @ flow)
    flow /= max(1.0, np.linalg.norm(flow, axis=1).max()) * (1 + 1e-12)
    residual = np.abs(incidence.T @ flow).sum()
    # An optimum may be projected into the pins' convex hull. Account for the
    # remaining floating-point balance residual on that bounded domain.
    lower = -(fixed * flow).sum() - residual * np.abs(pins).max() - 1e-9
    return float(lower), float(upper), junctions.tolist()


def optimum(pins):
    pins = np.asarray(pins, dtype=float)
    n = len(pins)
    if not 3 <= n <= 8 or pins.shape != (n, 2) or not np.isfinite(pins).all():
        raise ValueError('expected 3..8 finite planar pins')
    trees = topologies(n)
    solutions = [solve_topology(pins, tree) for tree in trees]
    lower = min(s[0] for s in solutions)
    winner = min(range(len(trees)), key=lambda i: solutions[i][1])
    upper = solutions[winner][1]
    if upper - lower > 1e-7 or lower > upper:
        raise RuntimeError(f'optimum unresolved: [{lower}, {upper}]')
    return dict(n=n, topologies=len(trees), lower=lower, upper=upper,
                edges=trees[winner], junctions=solutions[winner][2])


if __name__ == '__main__':
    try:
        print(json.dumps([optimum(pins) for pins in json.load(sys.stdin)]))
    except Exception as error:
        print(f'FAIL: optimum enumeration: {error}', file=sys.stderr)
        sys.exit(1)
