# AURORA routing revision: camera-ready equations + E1 m_u=5 support (final)
"""
Routing-distribution construction and analysis utilities.

This module implements routing policies, latency processing, and supporting
matrix operations used by the experiments.
"""

import os
import statistics
import warnings

import numpy as np

from Node_replacement import normalize_stochastic
from Optimization import optimize_pulp



# Import library for making the simulation, making random choices,
#creating exponential delays, and defining matrixes.


def compute_cdf(D, E):
    """
    Computes the CDF for a dataset D evaluated at points in E.

    Args:
        D (list): A list of data values (numerical).
        E (list): A list of evaluation points (numerical).

    Returns:
        list: A list O, where O[i] represents the percentage of values in D less than E[i].
    """
    # Sort the data list for efficient comparison
    D_sorted = sorted(D)
    n = len(D)
    O = []

    for e in E:
        # Count the number of elements in D that are less than e
        count = sum(1 for x in D_sorted if x <= e)
        # Calculate the percentage
        percentage = count / n
        O.append(percentage)

    return O
def Normalized(List, Omega0,Co):
    Sum = np.sum([List[i]*Co[i] for i in range(len(List))])
    Sum = Sum/Omega0
    return [List[i]/Sum for i in range(len(List))]


def Zero_Check(A):
    o1,o2 = np.shape(A)
    for i in range(o1):
        for j in range(o2):
            if int((10**(6))*A[i,j]) ==0:
                A[i,j] = 10**(-20)
    return A

def sort_and_recover(input_list):
    """
    Sorts the input list and returns:
    - The sorted list
    - A recovery list (indices mapping sorted list back to the original list)

    Args:
        input_list (list): The original list to sort.

    Returns:
        tuple: (sorted_list, recovery_list)
    """
    # Pair elements with their original indices
    indexed_list = list(enumerate(input_list))
    # Sort based on the values
    sorted_indexed_list = sorted(indexed_list, key=lambda x: x[1])
    # Extract the sorted list and the recovery indices
    sorted_list = [x[1] for x in sorted_indexed_list]
    recovery_list = [x[0] for x in sorted_indexed_list]
    return sorted_list, recovery_list

def recover_original(sorted_list, recovery_list):
    """
    Reconstructs the original list using the sorted list and recovery list.

    Args:
        sorted_list (list): The sorted list.
        recovery_list (list): The recovery list (indices mapping to original).

    Returns:
        list: The reconstructed original list.
    """
    # Create a placeholder list for the original
    original_list = [None] * len(sorted_list)
    # Use the recovery list to restore the original order
    for i, index in enumerate(recovery_list):
        original_list[index] = sorted_list[i]
    return original_list


def To_list(List):
    List_ = List.tolist()
    if len(List_)==1:
        output = List_[0]
    else:
        output = List_

    return output
def subtract_lists(list1, list2):
    # Check if both lists have the same length
    if len(list1) != len(list2):
        raise ValueError("Both lists must have the same length.")

    # Perform element-wise subtraction
    result = [a - b for a, b in zip(list1, list2)]
    for i in range(len(result)):
        if result[i] <0:
            result[i] =0


    return result

def Ent(List):
    L =[]
    for item in List:

        if item!=0:
            L.append(item)
    l = sum(L)
    for i in range(len(L)):
        L[i]=L[i]/l
    ent = 0
    for item in L:
        ent = ent - item*(np.log(item)/np.log(2))
    return ent

def Med(List):
    N = len(List)

    List_ = []
    for i in range(N):

        List_.append( statistics.median(List[i]))

    return List_


class Routing(object):
    def __init__(self,N,L):
        self.N = N
        self.L = L
        self.W = int(self.N/self.L)


    def alpha_closest(self, List, Omega, Top):
        """Rank-Based Routing (RBR), matching paper Eq. (7)."""
        alpha, K = Top
        alpha = float(alpha)
        K = int(K)
        if not 0.0 <= alpha <= 1.0:
            raise ValueError("alpha must lie in [0, 1].")

        latencies = np.asarray(List, dtype=float)
        capacities = np.asarray(Omega, dtype=float)
        W = len(capacities)
        if latencies.shape != capacities.shape or W == 0:
            raise ValueError("latency and capacity vectors must have equal non-zero length.")
        if not 1 <= K <= W:
            raise ValueError("RBR threshold T must satisfy 1 <= T <= W.")
        if np.any(latencies <= 0):
            raise ValueError("RBR requires strictly positive link latencies.")
        if np.any(capacities < 0) or capacities.sum() <= 0:
            raise ValueError("capacities must be non-negative with positive sum.")

        order = np.argsort(latencies, kind="mergesort")
        top = order[:K]
        weights = np.power(capacities, alpha) / (float(W) ** (1.0 - alpha))
        weights[top] = np.power(capacities[top], alpha) / np.power(
            latencies[top], 1.0 - alpha
        )
        total = float(weights.sum())
        if not np.isfinite(total) or total <= 0:
            raise ValueError("RBR produced an invalid normalization constant.")
        return (weights / total).tolist()

    def EXP_New(self, List, Omega_List, Tau):
        """Routing with Exponential Preference (REP), matching paper Eq. (6)."""
        alpha = float(Tau)
        if not 0.0 <= alpha <= 1.0:
            raise ValueError("alpha must lie in [0, 1].")

        latencies = np.asarray(List, dtype=float)
        capacities = np.asarray(Omega_List, dtype=float)
        W = len(capacities)
        if latencies.shape != capacities.shape or W == 0:
            raise ValueError("latency and capacity vectors must have equal non-zero length.")
        if np.any(capacities < 0) or capacities.sum() <= 0:
            raise ValueError("capacities must be non-negative with positive sum.")

        order = np.argsort(latencies, kind="mergesort")
        ranks = np.empty(W, dtype=int)
        ranks[order] = np.arange(W)
        scores = -ranks.astype(float)

        # Eq. (6) is singular at alpha=0.  Use its alpha -> 0+ limit.
        if alpha == 0.0:
            out = np.zeros(W, dtype=float)
            out[order[0]] = 1.0
            return out.tolist()

        # Evaluate exp(score*(1-alpha)/alpha) * omega**alpha in log space.
        positive = capacities > 0
        log_weights = scores * ((1.0 - alpha) / alpha)
        log_weights = np.where(
            positive,
            log_weights + alpha * np.log(np.where(positive, capacities, 1.0)),
            -np.inf,
        )
        log_weights -= np.max(log_weights)
        weights = np.exp(log_weights)
        total = float(weights.sum())
        if not np.isfinite(total) or total <= 0:
            raise ValueError("REP produced an invalid normalization constant.")
        return (weights / total).tolist()

    def Linear(self, L_Matrix_, Omega, alpha):
        """Routing with Linear Programming (RLP), using Eqs. (3)-(5)."""
        L_Matrix = np.asarray(L_Matrix_, dtype=float)
        R = optimize_pulp(L_Matrix, Omega, alpha)
        if R is None:
            raise RuntimeError("RLP optimization did not return a routing matrix.")
        return np.asarray(R, dtype=float)


    def Entropy_Transformation(self,List_R):

        T = np.zeros((len(List_R[0]),len(List_R[0])))
        for i1 in range(len(List_R[0])):
            T[i1,i1] = 1
        for k in range(len(List_R)):
            T = T.dot(List_R[k])


        H = []
        for i in range(len(List_R[0])):
            List = []
            for k in range(len(List_R[0])):
                List.append(T[i,k])
            L =[]
            for item in List:
                if item!=0:
                    L.append(item)
            l = np.sum(L)
            for i in range(len(L)):
                L[i]=L[i]/l
            ent = 0
            for item in L:
                ent = ent - item*(np.log(item)/np.log(2))
            H.append(ent)

        return H
    def Entropy_AVE(self,H,P):
        return To_list(np.matrix(P).dot(H))[0]


    def BALD(self, Matrix, theta):

        return normalize_stochastic(Matrix, theta)

    def Matrix_routing(self, fun, Matrix, Omega, Param):
        """Build a routing matrix for RLP, REP, or RBR.

        The legacy artifact names ``REB`` and ``RST`` are accepted as aliases
        for REP and RBR, respectively, so existing experiment code continues
        to work unchanged.
        """
        fun = str(fun).upper()
        if fun == "RLP":
            return self.Linear(Matrix, Omega, Param)

        if fun in {"REP", "REB"}:
            builder = self.EXP_New
        elif fun in {"RBR", "RST"}:
            builder = self.alpha_closest
        else:
            raise ValueError(f"unknown routing method: {fun}")

        matrix = np.asarray(Matrix, dtype=float)
        if matrix.ndim != 2 or matrix.shape != (self.W, self.W):
            raise ValueError(
                f"routing latency matrix must have shape {(self.W, self.W)}, "
                f"got {matrix.shape}"
            )

        out = np.zeros((self.W, self.W), dtype=float)
        for i in range(self.W):
            row = To_list(matrix[i, :])
            out[i, :] = builder(row, Omega, Param)
        return out

###########################Latency measurements###############################
    @staticmethod
    def _probability_vector(values, label="probabilities"):
        """Return a finite, non-negative, normalized probability vector.

        Numerical solvers can return tiny negative values for variables that
        are theoretically constrained to be non-negative.  Sampling routines
        reject such values.  We therefore clip negative round-off to zero and
        renormalize.  If a noticeably negative value is encountered we emit a
        warning instead of crashing the experiment, while still making the
        correction explicit.
        """
        probs = np.asarray(values, dtype=float).reshape(-1)
        if probs.size == 0:
            raise ValueError(f"{label} is empty")
        if not np.all(np.isfinite(probs)):
            raise ValueError(f"{label} contains NaN or infinite values")

        min_prob = float(np.min(probs))
        if min_prob < -1e-6:
            warnings.warn(
                f"{label} contained a negative value ({min_prob:.3e}); "
                "clipping negative entries to zero before normalization.",
                RuntimeWarning,
                stacklevel=2,
            )
        probs = np.clip(probs, 0.0, None)
        total = float(probs.sum())
        if not np.isfinite(total) or total <= 0.0:
            raise ValueError(f"{label} has zero or invalid probability mass")
        return probs / total

    def Latency_Measure(
        self,
        Latency_List,
        Routing_List,
        Path,
        m_u=1,
        n_sessions=None,
        seed=None,
    ):
        """Measure link delay under the supplied routing matrices.

        ``m_u == 1`` preserves the artifact's original exact expected-delay
        calculation.  For ``m_u > 1``, the function samples explicit sessions
        of ``m_u`` independently routed packets, takes the slowest packet in
        each session, and returns the mean of those session maxima.  E1 passes
        ``m_u=5`` to match the paper's session-level definition of ``d_l``.

        The Monte Carlo calculation is reproducible.  The number of sessions
        defaults to ``AURORA_LATENCY_SESSIONS`` (5000) and the RNG seed to
        ``AURORA_SEED`` (42).
        """
        m_u = int(m_u)
        if m_u < 1:
            raise ValueError("m_u must be at least 1")
        if len(Latency_List) != len(Routing_List):
            raise ValueError("Latency_List and Routing_List must have equal length")

        # Preserve the exact one-packet calculation for existing callers.
        if m_u == 1:
            if len(Latency_List) != 2 or len(Routing_List) != 2:
                # Generic exact expectation for an arbitrary number of hops.
                entry = self._probability_vector(Path, "entry distribution")
                state = entry.copy()
                expected = 0.0
                for hop, (latency, routing) in enumerate(zip(Latency_List, Routing_List)):
                    latency = np.asarray(latency, dtype=float)
                    routing = np.asarray(routing, dtype=float)
                    if latency.shape != routing.shape:
                        raise ValueError(
                            f"hop {hop}: latency and routing matrices must have equal shape"
                        )
                    clean = np.vstack(
                        [self._probability_vector(row, f"hop {hop} routing row {i}")
                         for i, row in enumerate(routing)]
                    )
                    expected += float(np.sum(state[:, None] * clean * latency))
                    state = state @ clean
                return expected

            # Original L=3 expression, but normalize rows defensively so solver
            # round-off cannot create invalid probability mass.
            p0 = self._probability_vector(Path, "entry distribution")
            r0 = np.vstack([
                self._probability_vector(row, f"routing row 0:{i}")
                for i, row in enumerate(np.asarray(Routing_List[0], dtype=float))
            ])
            r1 = np.vstack([
                self._probability_vector(row, f"routing row 1:{i}")
                for i, row in enumerate(np.asarray(Routing_List[1], dtype=float))
            ])
            l0 = np.asarray(Latency_List[0], dtype=float)
            l1 = np.asarray(Latency_List[1], dtype=float)
            if l0.shape != r0.shape or l1.shape != r1.shape:
                raise ValueError("latency and routing matrix shapes do not match")

            x = 0.0
            for i in range(r0.shape[0]):
                for j in range(r0.shape[1]):
                    for k in range(r1.shape[1]):
                        p = p0[i] * r0[i, j] * r1[j, k]
                        x += p * (l0[i, j] + l1[j, k])
            return float(x)

        if n_sessions is None:
            n_sessions = int(os.environ.get("AURORA_LATENCY_SESSIONS", "5000"))
        if seed is None:
            seed = int(os.environ.get("AURORA_SEED", "42"))
        n_sessions = int(n_sessions)
        if n_sessions < 1:
            raise ValueError("n_sessions must be positive")

        entry_p = self._probability_vector(Path, "entry distribution")
        rng = np.random.default_rng(int(seed))
        total_packets = n_sessions * m_u
        current = rng.choice(entry_p.size, size=total_packets, p=entry_p)
        packet_delay = np.zeros(total_packets, dtype=float)

        for hop, (latency, routing) in enumerate(zip(Latency_List, Routing_List)):
            latency = np.asarray(latency, dtype=float)
            routing = np.asarray(routing, dtype=float)
            if latency.ndim != 2 or routing.ndim != 2:
                raise ValueError(f"hop {hop}: latency and routing must be 2-D matrices")
            if latency.shape != routing.shape:
                raise ValueError(
                    f"hop {hop}: latency shape {latency.shape} does not match "
                    f"routing shape {routing.shape}"
                )
            if routing.shape[0] <= int(np.max(current)):
                raise ValueError(f"hop {hop}: current-node index exceeds routing rows")

            nxt = np.empty(total_packets, dtype=np.int64)
            for row in np.unique(current):
                mask = current == row
                probs = self._probability_vector(
                    routing[int(row)], f"hop {hop} routing row {int(row)}"
                )
                nxt[mask] = rng.choice(
                    routing.shape[1], size=int(mask.sum()), p=probs
                )

            packet_delay += latency[current, nxt]
            current = nxt

        session_delay = packet_delay.reshape(n_sessions, m_u).max(axis=1)
        return float(np.mean(session_delay))


    def Bandwidth(self,List_R,Omega,P):
        w_List = []
        W = len(List_R[0])
        I = np.zeros((len(List_R[0]),len(List_R[0])))
        for i1 in range(len(List_R[0])):
            I[i1,i1] = 1

        for k in range(len(List_R)+1):
            if k==0:
                for j in range(W):
                    w_List.append(round((P[j]*W)/Omega[k][j]*10)/10)
            else:
                Matrix  = np.copy(I)
                for _ in range(k):
                    Matrix = Matrix.dot(List_R[_])
                Temp = To_list(W*np.matrix(P).dot(Matrix))
                Temp_ = []
                for j_1 in range(len(Temp)):
                    Temp_.append(round((Temp[j_1]/Omega[k][j_1])*10)/10)


                w_List = w_List + Temp_

        E = [i/10 for i in range(51)]

        return compute_cdf(w_List, E)


#a = np.matrix([[0.01,0.05],[0.08,0.04]])

#P = [1.2,0.8]


#Example

#List = [0.1,0.01,0.05,0.34,0.5]


#Omega = [1,21,11,1,151]

#dis = Class.EXP_New(List, 0.5, Omega)

#dis = Class.alpha_closest(List, Omega, 0.5, 3)


