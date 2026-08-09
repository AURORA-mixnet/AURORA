# -*- coding: utf-8 -*-

"""
Stochastic-matrix normalization utilities.

The routines in this module enforce row normalization while bounding column
sums for routing-matrix updates.
"""

import numpy as np



def normalize_stochastic(A: np.ndarray, theta: float, max_iter: int = 100000, tol: float = 1e-10) -> np.ndarray:
    if theta < 1:
        raise ValueError("theta must be >= 1")

    A = np.array(A, dtype=float, copy=True)

    for _ in range(max_iter):

        # ---- Step 1: Column scaling ----
        col_sums = A.sum(axis=0)
        scale = np.ones_like(col_sums)
        mask = col_sums > theta + tol
        scale[mask] = theta / col_sums[mask]
        A *= scale  # broadcast across rows
        # ---- Step 2: Row normalization ----
        row_sums = A.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1.0  # safety#

        A /= row_sums
        ## ---- Convergence check ----
        if np.all(A.sum(axis=0) <= theta + tol):
            return A

    return A


# ✅ Example (FIXED)
