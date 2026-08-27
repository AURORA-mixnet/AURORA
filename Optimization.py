"""
Linear-programming routines for routing optimization.

This module implements Routing with Linear Programming (RLP) exactly as
specified by AURORA Eqs. (3)-(5).
"""

import numpy as np
from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable, PULP_CBC_CMD


def _validate_inputs(L_111, Omega, alpha):
    """Validate and normalize the inputs used by the RLP formulation."""
    L = np.asarray(L_111, dtype=float)
    omega = np.asarray(Omega, dtype=float)
    alpha = float(alpha)

    if L.ndim != 2 or L.shape[0] != L.shape[1]:
        raise ValueError("L_111 must be a square W x W latency matrix.")

    W = L.shape[0]
    if omega.ndim != 1 or len(omega) != W:
        raise ValueError("Omega must be a one-dimensional vector of length W.")
    if W == 0:
        raise ValueError("The routing problem must contain at least one node.")
    if not np.all(np.isfinite(L)) or not np.all(np.isfinite(omega)):
        raise ValueError("Latency and capacity inputs must be finite.")
    if np.any(omega < 0):
        raise ValueError("Processing capacities must be non-negative.")
    if float(np.sum(omega)) <= 0:
        raise ValueError("At least one processing capacity must be positive.")
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("alpha must lie in [0, 1].")

    return L, omega, alpha, W


def optimize_pulp(L_111, Omega, alpha):
    """Solve the camera-ready RLP formulation from Eqs. (3)-(5).

    Let gamma_ij be the probability of forwarding from node i in the current
    layer to node j in the next layer, and let

        fraction_j = omega_j / sum_m omega_m.

    The implemented LP is exactly:

        min  (1/W) * sum_i sum_j gamma_ij * L_ij                  (Eq. 3)

        s.t. 0 <= gamma_ij <= 1,
             sum_j gamma_ij = 1                                  (Eq. 4)

             alpha * fraction_j
                 <= (1/W) * sum_i gamma_ij
                 <= (1-alpha) + alpha * fraction_j               (Eq. 5)

    Eq. (5) is entered into PuLP after multiplying all three terms by W.
    No powered capacity fractions and no slack variables are used.
    """
    L, omega, alpha, W = _validate_inputs(L_111, Omega, alpha)

    prob = LpProblem("RLP_CameraReady", LpMinimize)

    # gamma_ij in [0, 1], Eq. (4).
    gamma = LpVariable.dicts(
        "gamma", (range(W), range(W)), lowBound=0.0, upBound=1.0
    )

    # Eq. (3). The factor 1/W does not change the minimizer, but is retained
    # so the executable formulation literally matches the paper.
    prob += (1.0 / W) * lpSum(
        L[i, j] * gamma[i][j]
        for i in range(W)
        for j in range(W)
    )

    # Eq. (4): each row is a probability distribution.
    for i in range(W):
        prob += lpSum(gamma[i][j] for j in range(W)) == 1.0

    # Eq. (5): use the unmodified capacity fraction omega_j / sum(omega).
    omega_total = float(np.sum(omega))
    for j in range(W):
        fraction = float(omega[j] / omega_total)
        column_sum = lpSum(gamma[i][j] for i in range(W))

        # Eq. (5), multiplied by W:
        # W*alpha*fraction <= sum_i gamma_ij
        #                      <= W*((1-alpha) + alpha*fraction).
        lower = W * alpha * fraction
        upper = W * ((1.0 - alpha) + alpha * fraction)

        prob += column_sum >= lower
        prob += column_sum <= upper

    prob.solve(PULP_CBC_CMD(msg=False))

    status = LpStatus[prob.status]
    if status != "Optimal":
        raise RuntimeError(f"RLP optimization failed: {status}")

    result = np.array(
        [[gamma[i][j].varValue for j in range(W)] for i in range(W)],
        dtype=float,
    )
    result[np.abs(result) < 1e-12] = 0.0
    return result


# Backward-compatible names retained because older experiment scripts may call
# them.  They intentionally delegate to the same camera-ready formulation so
# that no stale alternative RLP equations remain in the repository.
def optimize_pulp0(L_111, Omega, alpha):
    return optimize_pulp(L_111, Omega, alpha)


def optimize_pulp1(L_111, Omega, alpha):
    return optimize_pulp(L_111, Omega, alpha)
