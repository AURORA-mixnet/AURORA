"""
Routing-distribution construction and analysis utilities.

This module implements routing policies, latency processing, and supporting
matrix operations used by the experiments.
"""

import math
import statistics

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


    def alpha_closest(self,List,Omega,Top):
        alpha,K = Top
        x = math.pi/4
        List_ = List.copy()
        dis = [((Omega[j])**alpha)/(self.W**((1-alpha)*math.pi)) for j in range(len(Omega))]
        Min = 10000000
        Index = []
        for i in range(K):
            index = List_.index(min(List_))
            Index.append(index)
            List_[index] = Min
        for item in Index:
            dis[item] = (((Omega[item])**alpha))/((List[item])**((1-alpha)*math.pi))
        Sum = np.sum(dis)
        Dis = [dis[i]/Sum for i in range(len(Omega))]
        return Dis
    def EXP_New(self,List,Omega_List,Tau):
        hyperrr = 5
        if Tau == 0:
            Tau = 0.01
        Tau = math.sqrt(Tau)

        Lambda = (1-Tau)/Tau
        List_1 = np.copy(List)

        List_0 = [(Omega_List[i])**(Tau*hyperrr) for i in range(len(Omega_List))]
        sorted_list, recovery_list = sort_and_recover(List_1)

        List_A = [(math.exp(-Lambda*i)) for i in range(len(sorted_list))]

        # Recover the original list
        reconstructed_list = recover_original(List_A, recovery_list)


        dis_ = [reconstructed_list[i]*List_0[i] for i in range(len(Omega_List))]

        Sum = np.sum(dis_)
        dis = [dis_[i]/Sum for i in range(len(Omega_List))]

        return dis

    def Linear(self,L_Matrix_,Omega,alpha):
        L_Matrix = np.array(L_Matrix_)

        R = optimize_pulp(L_Matrix,Omega,alpha)

        return R


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

    def Matrix_routing(self,fun,Matrix,Omega,Param):
        #fun: 'RST', 'REB', 'RLP'
        if fun == 'RLP':
            return self.Linear(Matrix,Omega,Param)

        else:
            Dis_Matrix = np.zeros((self.W,self.W))
            if fun == 'REB':
                for i in range(self.W):
                    List = To_list(Matrix[i,:])
                    dis = self.EXP_New(List,Omega,Param)
                    Dis_Matrix[i,:] = dis
            elif fun == 'RST':
                for i in range(self.W):
                    List = To_list(Matrix[i,:])
                    dis = self.alpha_closest(List,Omega,Param)
                    Dis_Matrix[i,:] = dis
        return Dis_Matrix

###########################Latency measurements###############################
    def Latency_Measure(self,Latency_List,Routing_List,Path):
        L = 3
        n1,n2 = np.shape(Latency_List[0])

        x = 0
        for i in range(n1):
            for j in range(n1):
                for k in range(n2):
                    p = Path[i]*Routing_List[0][i,j]*Routing_List[1][j,k]
                    l = Latency_List[0][i,j]+Latency_List[1][j,k]
                    x+=p*l
        return x


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


