"""
Linear-programming routines for routing optimization.

This module builds and solves the constrained optimization problems used to
derive routing matrices.
"""

import numpy as np
from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable, PULP_CBC_CMD



def optimize_pulp0(L_111, Omega, alpha):
    L = np.array(L_111)
    W, _ = L.shape

    # Define problem
    prob = LpProblem("MatrixOptimization", LpMinimize)

    # Decision variables: R[i][j] in [0,1]
    R_vars = LpVariable.dicts("R", (range(W), range(W)), lowBound=0, upBound=1)

    # Objective function
    prob += lpSum(L[i][j] * R_vars[i][j] for i in range(W) for j in range(W))

    # Row constraints: sum_j R[i][j] = 1
    for i in range(W):
        prob += lpSum(R_vars[i][j] for j in range(W)) == 1

    # Normalization constant: Omega_{k+1}
    Omega_total = sum((Omega[j] ** alpha) for j in range(W))

    # Column constraints
    for j in range(W):
        frac = (Omega[j] ** alpha) / Omega_total

        lower = W * alpha * frac
        upper = W * ((1 - alpha) + alpha * frac)  # your chosen version

        prob += lpSum(R_vars[i][j] for i in range(W)) >= lower
        prob += lpSum(R_vars[i][j] for i in range(W)) <= upper

    # Solve
    prob.solve(PULP_CBC_CMD(msg=False))

    # Check status
    if LpStatus[prob.status] == 'Optimal':
        R = np.array([[R_vars[i][j].varValue for j in range(W)] for i in range(W)])
        return R

    elif LpStatus[prob.status] == 'Infeasible':
        None
        prob.writeLP("MatrixOptimization_Infeasible.lp")
        return None

    else:
        raise ValueError("Optimization failed: " + LpStatus[prob.status])


def optimize_pulp1(L_111, Omega, alpha):
    L = np.array(L_111)
    W, _ = L.shape

    # Define problem
    prob = LpProblem("MatrixOptimization", LpMinimize)

    # Decision variables: gamma_{ij} in [0,1]
    R_vars = LpVariable.dicts("R", (range(W), range(W)), lowBound=0, upBound=1)

    # Objective function
    prob += lpSum(L[i][j] * R_vars[i][j] for i in range(W) for j in range(W))

    # Row constraints: sum_j gamma_{ij} = 1
    for i in range(W):
        prob += lpSum(R_vars[i][j] for j in range(W)) == 1

    # Normalization constant Omega_{k+1}
    Omega_total = sum(Omega[j] for j in range(W))

    # Column constraints (MATCHING YOUR IMAGE)
    for j in range(W):
        frac = (Omega[j])**alpha / Omega_total

        lower = W*alpha * frac
        upper = W*frac

        prob += lpSum(R_vars[i][j] for i in range(W)) >= lower
        prob += lpSum(R_vars[i][j] for i in range(W)) <= upper

    # Solve
    prob.solve(PULP_CBC_CMD(msg=False))

    # Check status
    if LpStatus[prob.status] == 'Optimal':
        R = np.array([[R_vars[i][j].varValue for j in range(W)] for i in range(W)])
        return R

    elif LpStatus[prob.status] == 'Infeasible':
        None
        prob.writeLP("MatrixOptimization_Infeasible.lp")
        return None

    else:
        raise ValueError("Optimization failed: " + LpStatus[prob.status])


def optimize_pulp(L_111, Omega, alpha, lambda_penalty=1000):
    L = np.array(L_111)
    W, _ = L.shape

    prob = LpProblem("MatrixOptimization", LpMinimize)

    # Decision variables
    R = LpVariable.dicts("R", (range(W), range(W)), lowBound=0, upBound=1)

    # Slack variables
    s_low = LpVariable.dicts("s_low", range(W), lowBound=0)
    s_up = LpVariable.dicts("s_up", range(W), lowBound=0)

    # Objective: original + penalty
    prob += (
        lpSum(L[i][j] * R[i][j] for i in range(W) for j in range(W))
        + lambda_penalty * lpSum(s_low[j] + s_up[j] for j in range(W))
    )

    # Row constraints
    for i in range(W):
        prob += lpSum(R[i][j] for j in range(W)) == 1

    # Normalize Omega
    Omega_total = sum(Omega)

    for j in range(W):
        frac = (Omega[j] / Omega_total) ** alpha if Omega[j] > 0 else 0

        lower = W * alpha * frac
        upper = W * frac

        col_sum = lpSum(R[i][j] for i in range(W))

        # Relaxed constraints
        prob += col_sum >= lower - s_low[j]
        prob += col_sum <= upper + s_up[j]

    prob.solve(PULP_CBC_CMD(msg=False))


    if LpStatus[prob.status] == 'Optimal':
        R_sol = np.array([[R[i][j].varValue for j in range(W)] for i in range(W)])
        return R_sol
    else:
        return None


