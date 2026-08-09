# -*- coding: utf-8 -*-

"""
Fairness-constrained path-selection helper functions.

This module contains optimization and selection utilities used by the routing
and baseline evaluation code.
"""

import numpy as np



# Example Usage
def To_list(List):
    List_ = List.tolist()
    if len(List_)==1:
        output = List_[0]
    else:
        output = List_

    return output


#Example


def Random(Max_Omega,beta):
    K = 3

    Budget = 0# take cares of the budget
    Ave_Budget = Max_Omega/K # maxium budget allowed to spend on one mix-nodes corruption
    N = len(beta)
    C = []
    while Budget < Max_Omega:

        Index = round(N*np.random.rand(1)[0])
        if Index ==N:
            Index = N-1

        while beta[Index] > Ave_Budget :
            Index = round(N*np.random.rand(1)[0])
            if Index ==N:
                Index = N-1


        C.append(Index)
        Budget += beta[Index]
        beta[Index] = 10000


    return C


def Greedy_For_Fairness(Omega,beta,R_List_,L):
    CNodes = []
    Omega_L = Omega/L
    Cap = 0
    C_List = []
    while Cap < Omega_L:
        Index = beta[0].index(max(beta[0]))
        C_List.append(Index)
        Cap += beta[0][Index]
        beta[0][Index] = -10000
    CNodes.append(C_List)


    for l in range(L-1):
        R_List = np.copy(R_List_)

        Cap = 0
        C_List = []
        while Cap < Omega_L:
            List_Node = R_List[l][CNodes[l]]
            List_Index = To_list(np.sum(List_Node,axis=0))

            Index = List_Index.index(max(List_Index))

            R_List[l][:,Index] = -10000
            Cap += beta[l+1][Index]
            beta[l+1][Index] = -10000
            C_List.append(Index)
        CNodes.append(C_List)


    return CNodes


def Greedy(L_M_,Max_Omega,beta):
    None
    L_M = np.copy(L_M_)
    Cap = 0
    C = []

    N = len(L_M)

    Index = int(N*np.random.rand(1)[0])

    Cap += beta[Index]

    L_M[:,Index] = 10000
    C.append(Index)

    while Cap < Max_Omega:


        List = To_list(np.sum(L_M[C],axis = 0))

        Index = List.index(min(List))

        L_M[:,Index] = 10000

        Cap += beta[Index]

        C.append(Index)

    return C


