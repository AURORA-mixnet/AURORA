# -*- coding: utf-8 -*-

"""
Core experiment and baseline-analysis routines for the NDSS artifact.

This module implements the simulation and analysis logic used by
``Experiments.py`` to reproduce the paper's experimental results.
"""

import pickle
import statistics

import numpy as np

from FCP_Functions import Greedy, Random, Greedy_For_Fairness
from Routings import Routing
from Sim import Simulation



# Import library for making the simulation, making random choices,
#creating exponential delays, and defining matrixes.


#Example


#Example


def Corruption_c(List,N):
    Corrupted_List ={}

    for i in range(N):

        Corrupted_List['PM'+str(i+1)] = False

    for j in List:
        Corrupted_List['PM'+str(j+1)] = True

    return Corrupted_List


def permutation_matrix(AA, BB):

    A = [int(item*10000)/10000 for item in AA]
    B = [int(item*10000)/10000 for item in BB]
    if sorted(A) != sorted(B):
        None
        raise ValueError("Lists must be permutations of each other.")

    n = len(A)
    P = np.zeros((n, n))

    # Create index mapping from A to B
    index_map = {value: i for i, value in enumerate(B)}

    for i, value in enumerate(A):
        P[index_map[value], i] = 1  # Place a 1 at the corresponding position

    return P


def To_list(List):
    List_ = List.tolist()
    if len(List_)==1:
        output = List_[0]
    else:
        output = List_

    return output
def dist_List(List):
    Sum = np.sum(List)

    return [List[i]/Sum for i in range(len(List))]


def find_median_from_cdf(cdf):
    """
    Finds the median of a discrete distribution given its CDF.

    Args:
        cdf (list): A list representing the cumulative probabilities of a discrete distribution.

    Returns:
        int: The index of the median value in the distribution.
    """
    for i, value in enumerate(cdf):
        if value >= 0.5:
            return i  # The first index where CDF reaches or exceeds 0.5 is the median index.

    raise ValueError("Invalid CDF: It should reach at least 0.5 somewhere.")


def Medd(List):
    N = len(List)

    List_ = []
    for i in range(N):

        List_.append( statistics.median(List[i]))

    return List_


def Med(List):
    N = len(List)

    List_ = []
    for i in range(N):

        List_.append( statistics.median(List[i]))

    return List_


class CirMixNet(object):

    def __init__(self,Targets,Iteration,Capacity,run,delay1,delay2,W1,W2,L,base,Initial = False):
        self.Iterations = Iteration
        self.CAP = Capacity
        self.delay1 = delay1
        self.delay2 = delay2
        self.Targets = Targets
        self.W1 = W1
        self.W2 = W2
        self.L = L
        self.N1 = self.W1*self.L
        self.N2 = self.W2*self.L
        self.b = base
        self.WW = {'NYM':self.W1,'RIPE':self.W2}
        self.run = run
        self.Data_type = ['NYM','RIPE']
        self.Design = ['DNA']
        self.Method = ['RLP','REB','RST']
        self.Tau = [0.085,0.2,0.4,0.6,0.8,1]
        self.T = [2,12,25,38,50,80]
        self.nn = 20
        self.CF = 0.3
        self.Initial = Initial
        self.RST_tau = 0.6
        self.RST_T = 12
        self.CDF = [i/10 for i in range(51)]
        #self.Data_Set_General = self.data_generator(Iteration)
        self.Data_Set_General = {'NYM':{},'RIPE':{}}
        self.theta_var = [1.1,1.5,2,3,5]

        if self.Initial== False:
            with open('Nym_RIPE_dataset_short_version.pkl','rb') as pkl_file:
                data0 = pickle.load(pkl_file)
            for item in self.Data_type:

                for It in range(self.Iterations):
                    self.Data_Set_General[item]['It'+str(It+1)] = data0[item]['It'+str(It+1)]


        data_W1 = {}
        for i1 in range(self.W1*(self.L)):
            data_W1['PM'+str(i1+1)] = False
        data_W2 = {}
        for i1 in range(self.W2*(self.L)):
            data_W2['PM'+str(i1+1)] = False
        self.Corrupted_Mix = {self.W1:data_W1,self.W2:data_W2}
        self.dict_R = {'RLP':'Linear' , 'RST':'alpha_closest' , 'REB': 'EXP_New'}


    def data_FCP(self,Iteration):
        data0 = {}
        W = {'NYM':self.W1,'RIPE':self.W2}

        for Data in ['NYM','RIPE']:
            data1 = {}
            for It in range(Iteration):

                Matrix = self.Data_Set_General[Data]['It'+str(It+1)]['DNA']['Matrix']
                Latency_List = self.Data_Set_General[Data]['It'+str(It+1)]['DNA']['Latency_List']
                Positions = self.Data_Set_General[Data]['It'+str(It+1)]['DNA']['Positions']
                Loc = self.Data_Set_General[Data]['It'+str(It+1)]['DNA']['Loc']
                O_ = self.Data_Set_General[Data]['It'+str(It+1)]['DNA']['Omega']
                Omega = self.Data_Set_General[Data]['It'+str(It+1)]['DNA']['x']
                _ = self.Data_Set_General[Data]['It'+str(It+1)]['DNA']['xx']

                O_1 = []
                for item in _:
                    O_1 += item
                #Latency_List_R = Latency_extraction(Matrix, Positions_R, self.L)
                #Omega_x = [[Omega[j*W[Data]+i] for i in range(W[Data])] for j in range(self.L)]
                #O_R = [Norm_List(item,W[Data]) for item in Omega_x]
                #Omega_ = [[Omega[j*W[Data]+i] for i in range(W[Data])] for j in range(self.L)]

                data4 = {'Latency_List': Latency_List,'Omega':O_, 'Positions':Positions,'Loc':Loc,'beta':[Omega,O_1],'L_M':Matrix}
                data1['It'+str(It+1)] = data4

            data0[Data] = data1

        return data0

    def PDFs(self,data):
        #self.Tau = [0.6]
        #self.T = [2]
        data0 = {}
        for It in range(len(data['NYM'])):
            data_0 = {}

            for dataset_type in self.Data_type:
                data_1 = {}
                Class_R = Routing(self.WW[dataset_type]*self.L,self.L)

                for design in self.Design:
                    data_2 = {}
                    L_Mix = data[dataset_type]['It'+str(It+1)][design]['Latency_List']
                    O_Mix = data[dataset_type]['It'+str(It+1)][design]['Omega']
                    for method in self.Method:
                        data_3 = {}

                        if not method == 'RST':

                            for tau in self.Tau:


                                List_R = [[L_Mix[j],Class_R.Matrix_routing(method,np.matrix(L_Mix[j]),O_Mix[j+1],tau)] for j in range(self.L-1)]
                                List_B = []
                                for var_i in range(len(self.theta_var)):
                                    List_B.append([[L_Mix[j],Class_R.BALD(List_R[j][1],self.theta_var[var_i])] for j in range(self.L-1)])
                                data_3['tau'+str(int(10*tau))] = [List_R,List_B]


                        else:

                            for tau in self.Tau:

                                List_R = [[L_Mix[j],Class_R.Matrix_routing(method,np.matrix(L_Mix[j]),O_Mix[j+1],(tau,self.RST_T))] for j in range(self.L-1)]
                                List_B = []
                                for var_i in range(len(self.theta_var)):
                                    List_B.append([[L_Mix[j],Class_R.BALD(List_R[j][1],self.theta_var[var_i])] for j in range(self.L-1)])
                                data_3['tau'+str(int(10*tau))] = [List_R,List_B]

                            for _ in self.T:

                                List_R = [[L_Mix[j],Class_R.Matrix_routing(method,np.matrix(L_Mix[j]),O_Mix[j+1],(self.RST_tau,_))] for j in range(self.L-1)]
                                List_B = []
                                for var_i in range(len(self.theta_var)):
                                    List_B.append([[L_Mix[j],Class_R.BALD(List_R[j][1],self.theta_var[var_i])] for j in range(self.L-1)])
                                data_3['T'+str(int(_))] = [List_R,List_B]

                        data_2[method] = data_3
                    data_2['Loc'] = data[dataset_type]['It'+str(It+1)][design]['Loc']
                    data_2['Positions'] = data[dataset_type]['It'+str(It+1)][design]['Positions']
                    data_1[design] = data_2

                data_0[dataset_type] = data_1
            data0['It'+str(It+1)] = data_0
        return data0


    def PDFs_FCP(self,data):
        #self.Tau = [0.6]
        #self.T = [2]
        data0 = {}
        for It in range(len(data['NYM'])):
            data_0 = {}

            for dataset_type in self.Data_type:

                data_1 = {}
                Class_R = Routing(self.WW[dataset_type]*self.L,self.L)


                data_2 = {}
                L_Mix = data[dataset_type]['It'+str(It+1)]['Latency_List']
                O_Mix = data[dataset_type]['It'+str(It+1)]['Omega']
                for method in self.Method:
                    data_3 = {}

                    if not method == 'RST':

                        for tau in self.Tau:


                            List_R = [Class_R.Matrix_routing(method,np.matrix(L_Mix[j]),O_Mix[j+1],tau) for j in range(self.L-1)]
                            List_B = []
                            for var_i in range(len(self.theta_var)):
                                List_B.append([Class_R.BALD(List_R[j],self.theta_var[var_i]) for j in range(self.L-1)])

                            data_3['tau'+str(int(10*tau))] = [List_R,List_B]


                    else:

                        for tau in self.Tau:

                            List_R = [Class_R.Matrix_routing(method,np.matrix(L_Mix[j]),O_Mix[j+1],(tau,self.RST_T)) for j in range(self.L-1)]
                            List_B = []
                            for var_i in range(len(self.theta_var)):
                                List_B.append([Class_R.BALD(List_R[j],self.theta_var[var_i]) for j in range(self.L-1)])
                            data_3['tau'+str(int(10*tau))] = [List_R,List_B]

                        for _ in self.T:

                            List_R = [Class_R.Matrix_routing(method,np.matrix(L_Mix[j]),O_Mix[j+1],(self.RST_tau,_)) for j in range(self.L-1)]
                            List_B = []
                            for var_i in range(len(self.theta_var)):
                                List_B.append([Class_R.BALD(List_R[j],self.theta_var[var_i]) for j in range(self.L-1)])
                            data_3['T'+str(int(_))] = [List_R,List_B]

                    data_2[method] = data_3

                data_0[dataset_type] = data_2
            data0['It'+str(It+1)] = data_0
        return data0


    def Basic_Analysis_1(self,ITTT):
        data0 = self.PDFs(self.Data_Set_General)

        Iterations = ITTT
        data3 = {}
        for typ in ['RIPE']:

            Class_R = Routing((self.WW[typ]*self.L),self.L)
            data2 = {}
            for des in self.Design:

                data1 = {}
                for mtd in self.Method:


                    if not mtd == 'RST':

                        L_0 = []
                        H_0 = []
                        W_0 = []
                        LB_0 = []
                        HB_0 = []
                        WB_0 = []
                        LB_02 = []
                        HB_02 = []
                        WB_02 = []
                        LB_03 = []
                        HB_03 = []
                        WB_03 = []
                        LB_04 = []
                        HB_04 = []
                        WB_04 = []
                        LB_05 = []
                        HB_05 = []
                        WB_05 = []
                        for tau in self.Tau:

                            L_1 = []
                            H_1 = []
                            W_1 = []
                            LB_1 = []
                            HB_1 = []
                            WB_1 = []
                            LB_2 = []
                            HB_2 = []
                            WB_2 = []
                            LB_3 = []
                            HB_3 = []
                            WB_3 = []
                            LB_4 = []
                            HB_4 = []
                            WB_4 = []
                            LB_5 = []
                            HB_5 = []
                            WB_5 = []
                            for It in range(Iterations):


                                O_Mix = self.Data_Set_General[typ]['It'+str(It+1)][des]['Omega']
                                P = dist_List(O_Mix[0])
                                datum = data0['It'+str(It+1)][typ][des][mtd]['tau'+str(int(10*tau))]

                                L1=[np.matrix(datum[0][i][0]) for i in range(self.L-1)]
                                R1 =[datum[0][i][1] for i in range(self.L-1)]
                                #RB1 =[datum[1][i][1] for i in range(self.L-1)]
                                RB1 = []
                                for var_i in range(len(self.theta_var)):
                                    RB1.append([datum[1][var_i][i][1] for i in range(self.L-1)])
                                L_1.append(Class_R.Latency_Measure(L1, R1, P))
                                H_1.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(R1),P))
                                W_1.append(Class_R.Bandwidth(R1, O_Mix, P))

                                LB_1.append(Class_R.Latency_Measure(L1, RB1[0], P))
                                HB_1.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(RB1[0]),P))
                                WB_1.append(Class_R.Bandwidth(RB1[0], O_Mix, P))

                                LB_2.append(Class_R.Latency_Measure(L1, RB1[1], P))
                                HB_2.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(RB1[1]),P))
                                WB_2.append(Class_R.Bandwidth(RB1[1], O_Mix, P))

                                LB_3.append(Class_R.Latency_Measure(L1, RB1[2], P))
                                HB_3.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(RB1[2]),P))
                                WB_3.append(Class_R.Bandwidth(RB1[2], O_Mix, P))

                                LB_4.append(Class_R.Latency_Measure(L1, RB1[3], P))
                                HB_4.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(RB1[3]),P))
                                WB_4.append(Class_R.Bandwidth(RB1[3], O_Mix, P))

                                LB_5.append(Class_R.Latency_Measure(L1, RB1[4], P))
                                HB_5.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(RB1[4]),P))
                                WB_5.append(Class_R.Bandwidth(RB1[4], O_Mix, P))
                            L_0.append(Medd([L_1]))
                            H_0.append(Medd([H_1]))
                            W_0.append(Medd(To_list(np.transpose(np.matrix(W_1)))))
                            LB_0.append(Medd([LB_1]))
                            HB_0.append(Medd([HB_1]))
                            WB_0.append(Medd(To_list(np.transpose(np.matrix(WB_1)))))

                            LB_02.append(Medd([LB_2]))
                            HB_02.append(Medd([HB_2]))
                            WB_02.append(Medd(To_list(np.transpose(np.matrix(WB_2)))))

                            LB_03.append(Medd([LB_3]))
                            HB_03.append(Medd([HB_3]))
                            WB_03.append(Medd(To_list(np.transpose(np.matrix(WB_3)))))

                            LB_04.append(Medd([LB_4]))
                            HB_04.append(Medd([HB_4]))
                            WB_04.append(Medd(To_list(np.transpose(np.matrix(WB_4)))))

                            LB_05.append(Medd([LB_5]))
                            HB_05.append(Medd([HB_5]))
                            WB_05.append(Medd(To_list(np.transpose(np.matrix(WB_5)))))

                        data1[mtd] = {'L':L_0,'LB0':LB_0,'H':H_0,'HB0':HB_0,'Band':W_0,'Band_B0':WB_0}
                        data1[mtd]['HB1'] = HB_02
                        data1[mtd]['Band_B1'] = WB_02
                        data1[mtd]['LB1'] = LB_02
                        data1[mtd]['HB2'] = HB_03
                        data1[mtd]['Band_B2'] = WB_03
                        data1[mtd]['LB2'] = LB_03
                        data1[mtd]['HB3'] = HB_04
                        data1[mtd]['Band_B3'] = WB_04
                        data1[mtd]['LB3'] = LB_04
                        data1[mtd]['HB4'] = HB_05
                        data1[mtd]['Band_B4'] = WB_05
                        data1[mtd]['LB4'] = LB_05
                    else:


                        TL_0 = []
                        TH_0 = []
                        TW_0 = []
                        TLB_0 = []
                        THB_0 = []
                        TWB_0 = []
                        TLB_02 = []
                        THB_02 = []
                        TWB_02 = []
                        TLB_03 = []
                        THB_03 = []
                        TWB_03 = []
                        TLB_04 = []
                        THB_04 = []
                        TWB_04 = []
                        TLB_05 = []
                        THB_05 = []
                        TWB_05 = []

                        L_0 = []
                        H_0 = []
                        W_0 = []
                        LB_0 = []
                        HB_0 = []
                        WB_0 = []
                        LB_02 = []
                        HB_02 = []
                        WB_02 = []
                        LB_03 = []
                        HB_03 = []
                        WB_03 = []
                        LB_04 = []
                        HB_04 = []
                        WB_04 = []
                        LB_05 = []
                        HB_05 = []
                        WB_05 = []
                        for tau in self.Tau:

                            L_1 = []
                            H_1 = []
                            W_1 = []
                            LB_1 = []
                            HB_1 = []
                            WB_1 = []
                            LB_2 = []
                            HB_2 = []
                            WB_2 = []
                            LB_3 = []
                            HB_3 = []
                            WB_3 = []
                            LB_4 = []
                            HB_4 = []
                            WB_4 = []
                            LB_5 = []
                            HB_5 = []
                            WB_5 = []
                            for It in range(Iterations):


                                O_Mix = self.Data_Set_General[typ]['It'+str(It+1)][des]['Omega']
                                P = dist_List(O_Mix[0])
                                datum = data0['It'+str(It+1)][typ][des][mtd]['tau'+str(int(10*tau))]

                                L1=[np.matrix(datum[0][i][0]) for i in range(self.L-1)]
                                R1 =[datum[0][i][1] for i in range(self.L-1)]
                                RB1 = []
                                for var_i in range(len(self.theta_var)):
                                    RB1.append([datum[1][var_i][i][1] for i in range(self.L-1)])

                                L_1.append(Class_R.Latency_Measure(L1, R1, P))
                                H_1.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(R1),P))
                                W_1.append(Class_R.Bandwidth(R1, O_Mix, P))

                                LB_1.append(Class_R.Latency_Measure(L1, RB1[0], P))
                                HB_1.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(RB1[0]),P))
                                WB_1.append(Class_R.Bandwidth(RB1[0], O_Mix, P))

                                LB_2.append(Class_R.Latency_Measure(L1, RB1[1], P))
                                HB_2.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(RB1[1]),P))
                                WB_2.append(Class_R.Bandwidth(RB1[1], O_Mix, P))

                                LB_3.append(Class_R.Latency_Measure(L1, RB1[2], P))
                                HB_3.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(RB1[2]),P))
                                WB_3.append(Class_R.Bandwidth(RB1[2], O_Mix, P))

                                LB_4.append(Class_R.Latency_Measure(L1, RB1[3], P))
                                HB_4.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(RB1[3]),P))
                                WB_4.append(Class_R.Bandwidth(RB1[3], O_Mix, P))

                                LB_5.append(Class_R.Latency_Measure(L1, RB1[4], P))
                                HB_5.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(RB1[4]),P))
                                WB_5.append(Class_R.Bandwidth(RB1[4], O_Mix, P))
                            L_0.append(Medd([L_1]))
                            H_0.append(Medd([H_1]))
                            W_0.append(Medd(To_list(np.transpose(np.matrix(W_1)))))
                            LB_0.append(Medd([LB_1]))
                            HB_0.append(Medd([HB_1]))
                            WB_0.append(Medd(To_list(np.transpose(np.matrix(WB_1)))))

                            LB_02.append(Medd([LB_2]))
                            HB_02.append(Medd([HB_2]))
                            WB_02.append(Medd(To_list(np.transpose(np.matrix(WB_2)))))

                            LB_03.append(Medd([LB_3]))
                            HB_03.append(Medd([HB_3]))
                            WB_03.append(Medd(To_list(np.transpose(np.matrix(WB_3)))))

                            LB_04.append(Medd([LB_4]))
                            HB_04.append(Medd([HB_4]))
                            WB_04.append(Medd(To_list(np.transpose(np.matrix(WB_4)))))

                            LB_05.append(Medd([LB_5]))
                            HB_05.append(Medd([HB_5]))
                            WB_05.append(Medd(To_list(np.transpose(np.matrix(WB_5)))))

                        for t in self.T:

                            L_1 = []
                            H_1 = []
                            W_1 = []
                            LB_1 = []
                            HB_1 = []
                            WB_1 = []
                            LB_2 = []
                            HB_2 = []
                            WB_2 = []
                            LB_3 = []
                            HB_3 = []
                            WB_3 = []
                            LB_4 = []
                            HB_4 = []
                            WB_4 = []
                            LB_5 = []
                            HB_5 = []
                            WB_5 = []
                            for It in range(Iterations):


                                O_Mix = self.Data_Set_General[typ]['It'+str(It+1)][des]['Omega']
                                P = dist_List(O_Mix[0])
                                datum = data0['It'+str(It+1)][typ][des][mtd]['T'+str(int(t))]

                                L1=[np.matrix(datum[0][i][0]) for i in range(self.L-1)]
                                R1 =[datum[0][i][1] for i in range(self.L-1)]
                                RB1 = []
                                for var_i in range(len(self.theta_var)):
                                    RB1.append([datum[1][var_i][i][1] for i in range(self.L-1)])

                                L_1.append(Class_R.Latency_Measure(L1, R1, P))
                                H_1.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(R1),P))
                                W_1.append(Class_R.Bandwidth(R1, O_Mix, P))

                                LB_1.append(Class_R.Latency_Measure(L1, RB1[0], P))
                                HB_1.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(RB1[0]),P))
                                WB_1.append(Class_R.Bandwidth(RB1[0], O_Mix, P))

                                LB_2.append(Class_R.Latency_Measure(L1, RB1[1], P))
                                HB_2.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(RB1[1]),P))
                                WB_2.append(Class_R.Bandwidth(RB1[1], O_Mix, P))

                                LB_3.append(Class_R.Latency_Measure(L1, RB1[2], P))
                                HB_3.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(RB1[2]),P))
                                WB_3.append(Class_R.Bandwidth(RB1[2], O_Mix, P))

                                LB_4.append(Class_R.Latency_Measure(L1, RB1[3], P))
                                HB_4.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(RB1[3]),P))
                                WB_4.append(Class_R.Bandwidth(RB1[3], O_Mix, P))

                                LB_5.append(Class_R.Latency_Measure(L1, RB1[4], P))
                                HB_5.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(RB1[4]),P))
                                WB_5.append(Class_R.Bandwidth(RB1[4], O_Mix, P))
                            TL_0.append(Medd([L_1]))
                            TH_0.append(Medd([H_1]))
                            TW_0.append(Medd(To_list(np.transpose(np.matrix(W_1)))))
                            TLB_0.append(Medd([LB_1]))
                            THB_0.append(Medd([HB_1]))
                            TWB_0.append(Medd(To_list(np.transpose(np.matrix(WB_1)))))

                            TLB_02.append(Medd([LB_2]))
                            THB_02.append(Medd([HB_2]))
                            TWB_02.append(Medd(To_list(np.transpose(np.matrix(WB_2)))))

                            TLB_03.append(Medd([LB_3]))
                            THB_03.append(Medd([HB_3]))
                            TWB_03.append(Medd(To_list(np.transpose(np.matrix(WB_3)))))

                            TLB_04.append(Medd([LB_4]))
                            THB_04.append(Medd([HB_4]))
                            TWB_04.append(Medd(To_list(np.transpose(np.matrix(WB_4)))))

                            TLB_05.append(Medd([LB_5]))
                            THB_05.append(Medd([HB_5]))
                            TWB_05.append(Medd(To_list(np.transpose(np.matrix(WB_5)))))
                        d1 = {'L':L_0,'LB0':LB_0,'H':H_0,'HB0':HB_0,'Band':W_0,'Band_B0':WB_0}
                        d1['HB1'] = HB_02
                        d1['Band_B1'] = WB_02
                        d1['LB1'] = LB_02
                        d1['HB2'] = HB_03
                        d1['Band_B2'] = WB_03
                        d1['LB2'] = LB_03
                        d1['HB3'] = HB_04
                        d1['Band_B3'] = WB_04
                        d1['LB3'] = LB_04
                        d1['HB4'] = HB_05
                        d1['Band_B4'] = WB_05
                        d1['LB4'] = LB_05

                        d2 = {'L':TL_0,'LB0':TLB_0,'H':TH_0,'HB0':THB_0,'Band':TW_0,'Band_B0':TWB_0}

                        d2['HB1'] = THB_02
                        d2['Band_B1'] = TWB_02
                        d2['LB1'] = TLB_02
                        d2['HB2'] = THB_03
                        d2['Band_B2'] = TWB_03
                        d2['LB2'] = TLB_03
                        d2['HB3'] = THB_04
                        d2['Band_B3'] = TWB_04
                        d2['LB3'] = TLB_04
                        d2['HB4'] = THB_05
                        d2['Band_B4'] = TWB_05
                        d2['LB4'] = TLB_05
                        data1[mtd] = {'tau':d1,'T':d2}
                data2[des] = data1
            data3[typ] = data2


        data_1 = {}

        Final_data0 = {'Analytical':data3,'Sim':data_1}


        return Final_data0


    def Basic_Analysis_2(self,ITTT):
        data0 = self.PDFs(self.Data_Set_General)

        Iterations = ITTT
        typ = 'RIPE'
        des = "DNA"
        data_1 = {}
        for mtd in ['REB']:

            L_0 = []
            H_0 = []
            LB_0 = []
            HB_0 = []

            LB_01 = []
            HB_01 = []

            LB_02 = []
            HB_02 = []
            for tau in self.Tau:

                L_1 = []
                H_1 = []
                LB_1 = []
                HB_1 = []

                LB_2 = []
                HB_2 = []

                LB_3 = []
                HB_3 = []

                for It in range(Iterations):


                    O_Mix = self.Data_Set_General['NYM']['It'+str(It+1)][des]['Omega']
                    P = dist_List(O_Mix[0])
                    datum = data0['It'+str(It+1)]['NYM']['DNA'][mtd]['tau'+str(int(10*tau))]

                    L1=[datum[0][i][0] for i in range(self.L-1)]
                    R1 =[To_list(datum[0][i][1]) for i in range(self.L-1)]
                    RB1 = []
                    for var_i in range(len(self.theta_var)):
                        RB1.append([To_list(datum[1][var_i][i][1]) for i in range(self.L-1)])


                    Latency_Sim0,Entropy_Sim0 = self.Sim(L1,R1,P,self.nn,self.WW['NYM'],self.Corrupted_Mix[self.WW[typ]])

                    LatencyB_Sim0,EntropyB_Sim0 = self.Sim(L1,RB1[0],P,self.nn,self.WW['NYM'],self.Corrupted_Mix[self.WW[typ]])

                    LatencyB_Sim1,EntropyB_Sim1 = self.Sim(L1,RB1[2],P,self.nn,self.WW['NYM'],self.Corrupted_Mix[self.WW[typ]])

                    LatencyB_Sim2,EntropyB_Sim2 = self.Sim(L1,RB1[4],P,self.nn,self.WW['NYM'],self.Corrupted_Mix[self.WW[typ]])

                    L_1 = L_1 + Latency_Sim0
                    H_1 = H_1 + Entropy_Sim0

                    LB_1 = LB_1 + LatencyB_Sim0
                    HB_1 = HB_1 + EntropyB_Sim0

                    LB_2 = LB_2 + LatencyB_Sim1
                    HB_2 = HB_2 + EntropyB_Sim1

                    LB_3 = LB_3 + LatencyB_Sim2
                    HB_3 = HB_3 + EntropyB_Sim2

                L_0.append(L_1)
                H_0.append(H_1)
                LB_0.append(LB_1)
                HB_0.append(HB_1)

                LB_01.append(LB_2)
                HB_01.append(HB_2)

                LB_02.append(LB_3)
                HB_02.append(HB_3)
            data_1[mtd] = {'SL':L_0,'SLB0':LB_0,'SH':H_0,'SHB0':HB_0,'SLB1':LB_01,'SHB1':HB_01,'SLB2':LB_02,'SHB2':HB_02}

        Final_data0 = {'Analytical':{},'Sim':data_1}


        return Final_data0


    def Sim(self,List_L,List_R,P,nn,W,Corrupted_Mix):

        Mix_dict = {'Routing':List_R,'Latency':List_L,'First':P}


        Sim_ = Simulation(self.Targets,self.run,self.delay1,self.delay2,W*self.L,self.L )

        Latency_Sim,Entropy_Sim = Sim_.Simulator(Corrupted_Mix,Mix_dict,nn)


        return Latency_Sim, Entropy_Sim


    def E2E_Analysis(self, e2e_limit, method, dataset_type, Iterations, T=False):
        self.alpha0 = [i/10 for i in range(11)]
        self.alpha0[0] = 0.082

        if T:
            self.alpha0 = [2,7,12,18,25,32,38,44,50,60,70]
        design = 'DNA'
        data = self.Data_Set_General
        data0 = {}
        Class_R = Routing(self.WW[dataset_type]*self.L,self.L)
        L_0 = []
        H_0 = []
        W_0 = []
        LB_0 = []
        HB_0 = []
        WB_0 = []
        SL_0 = []
        SH_0 = []
        SLB_0 = []
        SHB_0 = []


        for It in range(Iterations):
            L_Mix = data[dataset_type]['It'+str(It+1)][design]['Latency_List']
            O_Mix = data[dataset_type]['It'+str(It+1)][design]['Omega']
            P = dist_List(O_Mix[0])
            L_1 = []
            H_1 = []
            W_1 = []
            LB_1 = []
            HB_1 = []
            WB_1 = []
            SL_1 = []
            SH_1 = []
            SLB_1 = []
            SHB_1 = []

            for theta in self.theta_var:
                if not T:


                    if not method == 'RST':

                        List_R = [[L_Mix[j],Class_R.Matrix_routing(method,np.matrix(L_Mix[j]),O_Mix[j+1],0.3)] for j in range(self.L-1)]
                        List_RRR = [[L_Mix[j],Class_R.Matrix_routing(method,np.matrix(L_Mix[j]),O_Mix[j+1],0.7)] for j in range(self.L-1)]

                    else:
                        List_R = [[L_Mix[j],Class_R.Matrix_routing(method,np.matrix(L_Mix[j]),O_Mix[j+1],(0.3,self.RST_T))] for j in range(self.L-1)]
                        List_RRR = [[L_Mix[j],Class_R.Matrix_routing(method,np.matrix(L_Mix[j]),O_Mix[j+1],(0.7,self.RST_T))] for j in range(self.L-1)]

                else:
                    List_R = [[L_Mix[j],Class_R.Matrix_routing(method,np.matrix(L_Mix[j]),O_Mix[j+1],(self.RST_tau,0.3))] for j in range(self.L-1)]
                    List_RRR = [[L_Mix[j],Class_R.Matrix_routing(method,np.matrix(L_Mix[j]),O_Mix[j+1],(self.RST_tau,0.7))] for j in range(self.L-1)]

                List_BB = [[L_Mix[j],Class_R.BALD(List_R[j][1],theta)] for j in range(self.L-1)]
                List_B = [[L_Mix[j],Class_R.BALD(List_RRR[j][1],theta)] for j in range(self.L-1)]
                L11 = [np.matrix(L_Mix[j]) for j in range(self.L-1) ]
                R11 = [List_BB[j][1] for j in range(self.L-1)]
                RB11 = [List_B[j][1] for j in range(self.L-1)]


                Rouitng_Latency0 = Class_R.Latency_Measure(L11, R11, P)
                L_1.append(Rouitng_Latency0)
                H_1.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(R11),P))
                W_1.append(find_median_from_cdf(Class_R.Bandwidth(R11, O_Mix, P))*10)
                Rouitng_Latency1 = Class_R.Latency_Measure(L11, RB11, P)
                LB_1.append(Rouitng_Latency1)
                HB_1.append(Class_R.Entropy_AVE(Class_R.Entropy_Transformation(RB11),P))
                WB_1.append(find_median_from_cdf(Class_R.Bandwidth(RB11, O_Mix, P))*10)


                L1=[L_Mix[i] for i in range(self.L-1)]
                R1 =[To_list(List_BB[i][1]) for i in range(self.L-1)]
                RB1 =[To_list(List_B[i][1]) for i in range(self.L-1)]

                self.delay1 = (e2e_limit - Rouitng_Latency0)/self.L
                Latency_Sim0,Entropy_Sim0 = self.Sim(L1,R1,P,self.nn,self.WW[dataset_type],self.Corrupted_Mix[self.WW[dataset_type]])
                self.dealy1 = (e2e_limit - Rouitng_Latency1)/self.L
                LatencyB_Sim0,EntropyB_Sim0 = self.Sim(L1,RB1,P,self.nn,self.WW[dataset_type],self.Corrupted_Mix[self.WW[dataset_type]])

                SL_1.append(np.mean(Latency_Sim0))
                SH_1.append(np.mean(Entropy_Sim0))

                SLB_1.append(np.mean(LatencyB_Sim0))
                SHB_1.append(np.mean(EntropyB_Sim0))


            L_0.append(L_1)
            H_0.append(H_1)
            W_0.append(W_1)
            LB_0.append(LB_1)
            HB_0.append(HB_1)
            WB_0.append(WB_1)
            SL_0.append(SL_1)
            SH_0.append(SH_1)
            SLB_0.append(SLB_1)
            SHB_0.append(SHB_1)

        L_2   = Med(To_list(np.transpose(np.matrix(L_0))))
        H_2   = Med(To_list(np.transpose(np.matrix(H_0))))
        W_2   = Med(To_list(np.transpose(np.matrix(W_0))))
        LB_2  = Med(To_list(np.transpose(np.matrix(LB_0))))
        HB_2  = Med(To_list(np.transpose(np.matrix(HB_0))))
        WB_2  = Med(To_list(np.transpose(np.matrix(WB_0))))
        SL_2  = Med(To_list(np.transpose(np.matrix(SL_0))))
        SH_2  = Med(To_list(np.transpose(np.matrix(SH_0))))
        SLB_2 = Med(To_list(np.transpose(np.matrix(SLB_0))))
        SHB_2 = Med(To_list(np.transpose(np.matrix(SHB_0))))


        data0['Imbalance'] = {'A_L':L_2,'A_H':H_2,'W':W_2,'S_L':SL_2,'S_H':SH_2}
        data0['Balance'] = {'A_L':LB_2,'A_H':HB_2,'W':WB_2,'S_L':SLB_2,'S_H':SHB_2}

        return data0


    def FCP(self,R_List,P,List_C,W,TYPE = False):
        R1 = np.matrix(R_List[0])
        R2 = np.matrix(R_List[1])

        if not TYPE:
            List = []

            for i in range(self.L):

                List_ = []
                for item in List_C:

                    if W*i <= item < W*(i+1):
                        List_.append(item-W*i)
                List.append(List_)
        else:
            List = List_C


        Path_C  = 0
        for i in (List[0]):
            for j in (List[1]):
                for k in (List[2]):

                    Path_C += P[i]*R1[i,j]*R2[j,k]
        #if TYPE == 'REB':

        return Path_C

    def C_Mix(self,L_M,K,Max_Omega,beta,Transformed_beta):
        A = permutation_matrix(beta,Transformed_beta)
        N = len(L_M)


        List_c1_ = Greedy(L_M,Max_Omega,beta)
        temp = [0]*len(beta)
        for i in List_c1_:
            temp[i] = 1
        List_c11 = To_list(np.matrix(temp).dot(A))
        List_c1 = []
        for i  in range(len(List_c11)):
            if int(List_c11[i]) == 1:
                List_c1.append(i)

        Sim_c1 = Corruption_c(List_c1,N)

        List_c2_ = Random(Max_Omega,beta)
        temp = [0]*len(beta)
        for i in List_c2_:
            temp[i] = 1
        List_c22 = To_list(np.matrix(temp).dot(A))
        List_c2 = []
        for i  in range(len(List_c22)):
            if int(List_c22[i]) == 1:
                List_c2.append(i)
        Sim_c2 = Corruption_c(List_c2,N)

        data0 = {'LP_R':[L_M,Max_Omega,Transformed_beta],'LP_S': None,'G_R':List_c1,'G_S':Sim_c1,'R_R':List_c2,'R_S':Sim_c2}
        return data0


    def FCP_Analysis_1(self,Iterations,K,TTTT,tete):
        self.theta_var = [self.theta_var[tete]]
        data0 = self.data_FCP(Iterations)
        data1 = self.PDFs_FCP(data0)

        data_cc = {}
        for typ in self.Data_type:
            for It in range(Iterations):
                datum_ = data0[typ]['It'+str(It+1)]
                data_c = self.C_Mix(datum_['L_M'],K,self.WW[typ]*self.CF*self.L,datum_['beta'][1],datum_['beta'][1])
                data_cc[typ+'It'+str(It+1)] = data_c

        data_0 = {}
        for typ in ['RIPE']:
            data_1 = {}
            if typ == 'NYM':
                data_Sim = {}
            for mtd in self.Method:
                data_Sim_ = {}
                if not mtd == 'RST':
                    F_LP_0 = []
                    F_LPB_0 = []
                    F_G_0 = []
                    F_GB_0 = []
                    F_R_0 = []
                    F_RB_0 = []
                    for tau in [self.Tau[TTTT]]:
                        F_LP_1 = []
                        F_LPB_1 = []
                        F_G_1 = []
                        F_GB_1 = []
                        F_R_1 = []
                        F_RB_1 = []


                        data_Sim__ = {}
                        for It in range(Iterations):
                            data_c = data_cc[typ+'It'+str(It+1)]
                            O_Mix_ = np.matrix(data0[typ]['It'+str(It+1)]['Omega'] )
                            O_Mix = To_list(O_Mix_)
                            P = dist_List(O_Mix[0])
                            datum = data1['It'+str(It+1)][typ][mtd]['tau'+str(int(10*tau))]

                            R1 =[datum[0][i] for i in range(self.L-1)]
                            RB1 = []
                            for var_i in range(len(self.theta_var)):
                                RB1.append([datum[1][var_i][i] for i in range(self.L-1)])


                            R1_ =[np.matrix(datum[0][i]) for i in range(self.L-1)]
                            RB1_ = []
                            for var_i in range(len(self.theta_var)):
                                RB1_.append([np.matrix(datum[1][var_i][i]) for i in range(self.L-1)])

                            #Greedy_For_Fairness

                            List_C_Mix_LP_Im = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,R1_,self.L)
                            O_Mix = To_list(O_Mix_)
                            List_C_Mix_LP_Ba0 = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,RB1_[0],self.L)
                            #List_C_Mix_LP_Ba1 = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,RB1_[1],self.L)

                            #List_C_Mix_LP_Ba2 = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,RB1_[2],self.L)

                            #List_C_Mix_LP_Ba3 = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,RB1_[3],self.L)

                            #List_C_Mix_LP_Ba4 = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,RB1_[4],self.L)

                            List_C_Mix_LP =[List_C_Mix_LP_Ba0[JJ][II] +JJ*self.WW[typ]  for JJ in range(len(List_C_Mix_LP_Ba0)) for II in range(len(List_C_Mix_LP_Ba0[JJ]))]

                            data_Sim__['It'+str(It+1)] = Corruption_c(List_C_Mix_LP,self.L*self.WW[typ])

                            F_LP_1.append(self.FCP(R1,P,List_C_Mix_LP_Im,self.WW[typ],True))

                            F_LPB_1.append(self.FCP(RB1[0],P,List_C_Mix_LP_Ba0,self.WW[typ],True))


                            F_G_1.append(self.FCP(R1,P,data_c['G_R'],self.WW[typ]))

                            F_GB_1.append(self.FCP(RB1[0],P,data_c['G_R'],self.WW[typ]))

                            F_R_1.append(self.FCP(R1,P,data_c['R_R'],self.WW[typ]))
                            F_RB_1.append(self.FCP(RB1[0],P,data_c['R_R'],self.WW[typ]))


                        F_LP_0.append(Medd([F_LP_1])[0])
                        F_LPB_0.append(Medd([F_LPB_1])[0])

                        F_G_0.append(Medd([F_G_1])[0])
                        F_GB_0.append(Medd([F_GB_1])[0])

                        F_R_0.append(Medd([F_R_1])[0])
                        F_RB_0.append(Medd([F_RB_1])[0])

                        data_Sim_['tau'+str(int(10*tau))] = data_Sim__
                    data_1[mtd] = {'F_LP':F_LP_0,'F_LPB0':F_LPB_0,'F_G':F_G_0,'F_GB0':F_GB_0,'F_R':F_R_0,'F_RB0':F_RB_0}

                else:

                    F_LP_0 = []
                    F_LPB_0 = []
                    F_G_0 = []
                    F_GB_0 = []
                    F_R_0 = []
                    F_RB_0 = []
                    TF_LP_0 = []
                    TF_LPB_0 = []
                    TF_G_0 = []
                    TF_GB_0 = []
                    TF_R_0 = []
                    TF_RB_0 = []


                    for tau in [self.Tau[TTTT]]:
                        F_LP_1 = []
                        F_LPB_1 = []
                        F_G_1 = []
                        F_GB_1 = []
                        F_R_1 = []
                        F_RB_1 = []

                        data_Sim__ = {}

                        for It in range(Iterations):
                            data_c = data_cc[typ+'It'+str(It+1)]
                            O_Mix_ = np.matrix(data0[typ]['It'+str(It+1)]['Omega'])
                            O_Mix = To_list(O_Mix_)
                            P = dist_List(O_Mix[0])
                            datum = data1['It'+str(It+1)][typ][mtd]['tau'+str(int(10*tau))]

                            R1 =[datum[0][i] for i in range(self.L-1)]
                            #RB1 =[datum[1][i] for i in range(self.L-1)]
                            RB1 = []
                            for var_i in range(len(self.theta_var)):
                                RB1.append([datum[1][var_i][i] for i in range(self.L-1)])

                            R1_ =[np.matrix(datum[0][i]) for i in range(self.L-1)]
                            #RB1_ =[np.matrix(datum[1][i]) for i in range(self.L-1)]
                            RB1_ = []
                            for var_i in range(len(self.theta_var)):
                                RB1_.append([np.matrix(datum[1][var_i][i]) for i in range(self.L-1)])

                            #Greedy_For_Fairness

                            List_C_Mix_LP_Im = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,R1_,self.L)
                            O_Mix = To_list(O_Mix_)
                            List_C_Mix_LP_Ba0 = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,RB1_[0],self.L)


                            List_C_Mix_LP =[List_C_Mix_LP_Ba0[JJ][II] +JJ*self.WW[typ]  for JJ in range(len(List_C_Mix_LP_Ba0)) for II in range(len(List_C_Mix_LP_Ba0[JJ]))]

                            data_Sim__['It'+str(It+1)] = Corruption_c(List_C_Mix_LP,self.L*self.WW[typ])

                            F_LP_1.append(self.FCP(R1,P,List_C_Mix_LP_Im,self.WW[typ],True))


                            F_G_1.append(self.FCP(R1,P,data_c['G_R'],self.WW[typ]))
                            F_R_1.append(self.FCP(R1,P,data_c['R_R'],self.WW[typ]))

                            F_LPB_1.append(self.FCP(RB1[0],P,List_C_Mix_LP_Ba0,self.WW[typ],True))


                            F_GB_1.append(self.FCP(RB1[0],P,data_c['G_R'],self.WW[typ]))

                            F_RB_1.append(self.FCP(RB1[0],P,data_c['R_R'],self.WW[typ]))

                        F_LP_0.append(Medd([F_LP_1])[0])
                        F_LPB_0.append(Medd([F_LPB_1])[0])
                        F_G_0.append(Medd([F_G_1])[0])
                        F_GB_0.append(Medd([F_GB_1])[0])
                        F_R_0.append(Medd([F_R_1])[0])
                        F_RB_0.append(Medd([F_RB_1])[0])


                        data_Sim_['tau'+str(int(10*tau))] = data_Sim__

                    for t in [self.T[TTTT]]:
                        TF_LP_1 = []
                        TF_LPB_1 = []
                        TF_G_1 = []
                        TF_GB_1 = []
                        TF_R_1 = []
                        TF_RB_1 = []


                        for It in range(Iterations):
                            data_c = data_cc[typ+'It'+str(It+1)]
                            O_Mix_ = np.matrix(data0[typ]['It'+str(It+1)]['Omega'])
                            O_Mix = To_list(O_Mix_)
                            P = dist_List(O_Mix[0])
                            datum = data1['It'+str(It+1)][typ][mtd]['T'+str(int(t))]

                            R1 =[datum[0][i] for i in range(self.L-1)]
                            #RB1 =[datum[1][i] for i in range(self.L-1)]
                            RB1 = []
                            for var_i in range(len(self.theta_var)):
                                RB1.append([datum[1][var_i][i] for i in range(self.L-1)])

                            R1_ =[np.matrix(datum[0][i]) for i in range(self.L-1)]
                            #RB1_ =[np.matrix(datum[1][i]) for i in range(self.L-1)]
                            RB1_ = []
                            for var_i in range(len(self.theta_var)):
                                RB1_.append([np.matrix(datum[1][var_i][i]) for i in range(self.L-1)])

                            #Greedy_For_Fairness

                            List_C_Mix_LP_Im = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,R1_,self.L)
                            O_Mix = To_list(O_Mix_)
                            #List_C_Mix_LP_Ba = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,RB1_,self.L)

                            List_C_Mix_LP_Ba0 = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,RB1_[0],self.L)


                            TF_LP_1.append(self.FCP(R1,P,List_C_Mix_LP_Im,self.WW[typ],True))

                            TF_G_1.append(self.FCP(R1,P,data_c['G_R'],self.WW[typ]))
                            TF_R_1.append(self.FCP(R1,P,data_c['R_R'],self.WW[typ]))


                            TF_LPB_1.append(self.FCP(RB1[0],P,List_C_Mix_LP_Ba0,self.WW[typ],True))


                            TF_GB_1.append(self.FCP(RB1[0],P,data_c['G_R'],self.WW[typ]))

                            TF_RB_1.append(self.FCP(RB1[0],P,data_c['R_R'],self.WW[typ]))


                        TF_LP_0.append(Medd([TF_LP_1])[0])
                        TF_LPB_0.append(Medd([TF_LPB_1])[0])
                        TF_G_0.append(Medd([TF_G_1])[0])
                        TF_GB_0.append(Medd([TF_GB_1])[0])
                        TF_R_0.append(Medd([TF_R_1])[0])
                        TF_RB_0.append(Medd([TF_RB_1])[0])


                    d1 = {'F_LP':F_LP_0,'F_LPB0':F_LPB_0,'F_G':F_G_0,'F_GB0':F_GB_0,'F_R':F_R_0,'F_RB0':F_RB_0}

                    d2 = {'F_LP':TF_LP_0,'F_LPB0':TF_LPB_0,'F_G':TF_G_0,'F_GB0':TF_GB_0,'F_R':TF_R_0,'F_RB0':TF_RB_0}

                    data_1[mtd] = {'tau':d1,'T':d2}

            data_0[typ] = data_1

        data_1 = {}


        Final_data0 = {'Analytical':data_0,'Sim':data_1}


        return Final_data0


    def FCP_Analysis(self,Iterations,K,TTTT,tete):
        self.theta_var = [self.theta_var[tete]]
        data0 = self.data_FCP(Iterations)
        data1 = self.PDFs_FCP(data0)

        data_cc = {}
        for typ in ['NYM']:
            for It in range(Iterations):
                datum_ = data0[typ]['It'+str(It+1)]
                data_c = self.C_Mix(datum_['L_M'],K,self.WW[typ]*self.CF*self.L,datum_['beta'][0],datum_['beta'][0])
                data_cc[typ+'It'+str(It+1)] = data_c

        data_0 = {}
        for typ in ['NYM']:
            data_1 = {}
            if typ == 'NYM':
                data_Sim = {}
            for mtd in self.Method:
                data_Sim_ = {}
                if not mtd == 'RST':
                    F_LP_0 = []
                    F_LPB_0 = []
                    F_G_0 = []
                    F_GB_0 = []
                    F_R_0 = []
                    F_RB_0 = []
                    for tau in [self.Tau[TTTT]]:
                        F_LP_1 = []
                        F_LPB_1 = []
                        F_G_1 = []
                        F_GB_1 = []
                        F_R_1 = []
                        F_RB_1 = []


                        data_Sim__ = {}
                        for It in range(Iterations):
                            data_c = data_cc[typ+'It'+str(It+1)]
                            O_Mix_ = np.matrix(data0[typ]['It'+str(It+1)]['Omega'] )
                            O_Mix = To_list(O_Mix_)
                            P = dist_List(O_Mix[0])
                            datum = data1['It'+str(It+1)][typ][mtd]['tau'+str(int(10*tau))]

                            RB1_ = []
                            for var_i in range(len(self.theta_var)):
                                RB1_.append([np.matrix(datum[1][var_i][i]) for i in range(self.L-1)])


                            List_C_Mix_LP_Ba0 = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,RB1_[0],self.L)


                            List_C_Mix_LP =[List_C_Mix_LP_Ba0[JJ][II] +JJ*self.WW[typ]  for JJ in range(len(List_C_Mix_LP_Ba0)) for II in range(len(List_C_Mix_LP_Ba0[JJ]))]

                            data_Sim__['It'+str(It+1)] = Corruption_c(List_C_Mix_LP,self.L*self.WW[typ])


                        data_Sim_['tau'+str(int(10*tau))] = data_Sim__
                    data_1[mtd] = {'F_LP':F_LP_0,'F_LPB0':F_LPB_0,'F_G':F_G_0,'F_GB0':F_GB_0,'F_R':F_R_0,'F_RB0':F_RB_0}

                else:

                    F_LP_0 = []
                    F_LPB_0 = []
                    F_G_0 = []
                    F_GB_0 = []
                    F_R_0 = []
                    F_RB_0 = []


                    for tau in [self.Tau[TTTT]]:
                        F_LP_1 = []
                        F_LPB_1 = []
                        F_G_1 = []
                        F_GB_1 = []
                        F_R_1 = []
                        F_RB_1 = []

                        data_Sim__ = {}

                        for It in range(Iterations):
                            data_c = data_cc[typ+'It'+str(It+1)]
                            O_Mix_ = np.matrix(data0[typ]['It'+str(It+1)]['Omega'])
                            O_Mix = To_list(O_Mix_)
                            P = dist_List(O_Mix[0])
                            datum = data1['It'+str(It+1)][typ][mtd]['tau'+str(int(10*tau))]

                            R1 =[datum[0][i] for i in range(self.L-1)]
                            #RB1 =[datum[1][i] for i in range(self.L-1)]
                            RB1 = []
                            for var_i in range(len(self.theta_var)):
                                RB1.append([datum[1][var_i][i] for i in range(self.L-1)])

                            RB1_ = []
                            for var_i in range(len(self.theta_var)):
                                RB1_.append([np.matrix(datum[1][var_i][i]) for i in range(self.L-1)])

                            O_Mix = To_list(O_Mix_)
                            List_C_Mix_LP_Ba0 = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,RB1_[0],self.L)

                            List_C_Mix_LP =[List_C_Mix_LP_Ba0[JJ][II] +JJ*self.WW[typ]  for JJ in range(len(List_C_Mix_LP_Ba0)) for II in range(len(List_C_Mix_LP_Ba0[JJ]))]

                            data_Sim__['It'+str(It+1)] = Corruption_c(List_C_Mix_LP,self.L*self.WW[typ])


                        data_Sim_['tau'+str(int(10*tau))] = data_Sim__


                data_Sim[mtd] = data_Sim_
            data_0[typ] = data_1


        data_1 = {}
        for mtd in self.Method:

            F_LP_0 = []
            F_G_0 = []
            F_R_0 = []

            for tau in [self.Tau[TTTT]]:

                F_LP_1 = []
                F_G_1 = []
                F_R_1 = []


                for It in range(Iterations):
                    data_c = data_cc['NYM'+'It'+str(It+1)]


                    O_Mix = data0['NYM']['It'+str(It+1)]['Omega']
                    P = dist_List(O_Mix[0])
                    datum = data1['It'+str(It+1)]['NYM'][mtd]['tau'+str(int(10*tau))]

                    L1=[[[0.001]*self.WW['NYM']]*self.WW['NYM'] for i in range(self.L-1)]
                    R1 =[To_list(datum[0][i]) for i in range(self.L-1)]

                    Corrupted_Mix_LP = data_Sim[mtd]['tau'+str(int(10*tau))]['It'+str(It+1)]
                    Corrupted_Mix_G = data_c['G_S']
                    Corrupted_Mix_R = data_c['R_S']

                    _,Ent_LP = self.Sim(L1,R1,P,self.nn,self.WW['NYM'],Corrupted_Mix_LP)
                    _,Ent_G = self.Sim(L1,R1,P,self.nn,self.WW['NYM'],Corrupted_Mix_G)
                    _,Ent_R = self.Sim(L1,R1,P,self.nn,self.WW['NYM'],Corrupted_Mix_R)

                    F_LP_1 += Ent_LP
                    F_G_1 += Ent_G
                    F_R_1 += Ent_R
                F_LP_0.append(F_LP_1)
                F_G_0.append(F_G_1)
                F_R_0.append(F_R_1)

            data_1[mtd] = {'LP_H':F_LP_0,'G_H':F_G_0,'R_H':F_R_0}

        Final_data0 = {'Analytical':{},'Sim':data_1}


        return Final_data0


    def FCP_Budget_(self,Iterations,tau,fcfc,tete):
        self.theta_var = [self.theta_var[tete]]
        data0 = self.data_FCP(Iterations)
        data1 = self.PDFs_FCP(data0)
        CF = [0.1,0.15,0.2,0.25,0.3,0.35]

        data_cc = {}
        for typ in self.Data_type:
            for It in range(Iterations):
                datum_ = data0[typ]['It'+str(It+1)]
                data_c = self.C_Mix(datum_['L_M'],5,self.WW[typ]*self.CF*self.L,datum_['beta'][0],datum_['beta'][1])
                data_cc[typ+'It'+str(It+1)] = data_c

        data_0 = {}
        for typ in ['RIPE']:
            data_1 = {}
            if typ == 'NYM':
                data_Sim = {}
            for mtd in self.Method:
                data_Sim_ = {}
                if not mtd == 'RST':
                    F_LP_0 = []
                    F_LPB_0 = []
                    F_G_0 = []
                    F_GB_0 = []
                    F_R_0 = []
                    F_RB_0 = []

                    for cf in [CF[fcfc]]:
                        self.CF = cf
                        None
                        F_LP_1 = []
                        F_LPB_1 = []
                        F_G_1 = []
                        F_GB_1 = []
                        F_R_1 = []
                        F_RB_1 = []

                        data_Sim__ = {}
                        for It in range(Iterations):
                            data_c = data_cc[typ+'It'+str(It+1)]
                            O_Mix_ = np.matrix(data0[typ]['It'+str(It+1)]['Omega'] )
                            O_Mix = To_list(O_Mix_)
                            P = dist_List(O_Mix[0])
                            datum = data1['It'+str(It+1)][typ][mtd]['tau'+str(int(10*tau))]

                            R1 =[datum[0][i] for i in range(self.L-1)]
                            #RB1 =[datum[1][i] for i in range(self.L-1)]
                            RB1 = []
                            for var_i in range(len(self.theta_var)):
                                RB1.append([datum[1][var_i][i] for i in range(self.L-1)])

                            R1_ =[np.matrix(datum[0][i]) for i in range(self.L-1)]
                            #RB1_ =[np.matrix(datum[1][i]) for i in range(self.L-1)]
                            RB1_ = []
                            for var_i in range(len(self.theta_var)):
                                RB1_.append([np.matrix(datum[1][var_i][i]) for i in range(self.L-1)])
                            #Greedy_For_Fairness

                            List_C_Mix_LP_Im = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,R1_,self.L)
                            O_Mix = To_list(O_Mix_)
                            #List_C_Mix_LP_Ba = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,RB1_,self.L)
                            List_C_Mix_LP_Ba0 = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,RB1_[0],self.L)


                            List_C_Mix_LP =[List_C_Mix_LP_Ba0[JJ][II] +JJ*self.WW[typ]  for JJ in range(len(List_C_Mix_LP_Ba0)) for II in range(len(List_C_Mix_LP_Ba0[JJ]))]

                            data_Sim__['It'+str(It+1)] = Corruption_c(List_C_Mix_LP,self.L*self.WW[typ])

                            F_LP_1.append(self.FCP(R1,P,List_C_Mix_LP_Im,self.WW[typ],True))

                            #F_LPB_1.append(self.FCP(RB1,P,List_C_Mix_LP_Ba,self.WW[typ],True))

                            F_G_1.append(self.FCP(R1,P,data_c['G_R'],self.WW[typ]))
                            #F_GB_1.append(self.FCP(RB1,P,data_c['G_R'],self.WW[typ]))
                            F_R_1.append(self.FCP(R1,P,data_c['R_R'],self.WW[typ]))
                            #F_RB_1.append(self.FCP(RB1,P,data_c['R_R'],self.WW[typ]))


                            F_LPB_1.append(self.FCP(RB1[0],P,List_C_Mix_LP_Ba0,self.WW[typ],True))


                            F_GB_1.append(self.FCP(RB1[0],P,data_c['G_R'],self.WW[typ]))

                            F_RB_1.append(self.FCP(RB1[0],P,data_c['R_R'],self.WW[typ]))


                        F_LP_0.append(Medd([F_LP_1])[0])
                        F_LPB_0.append(Medd([F_LPB_1])[0])
                        F_G_0.append(Medd([F_G_1])[0])
                        F_GB_0.append(Medd([F_GB_1])[0])
                        F_R_0.append(Medd([F_R_1])[0])
                        F_RB_0.append(Medd([F_RB_1])[0])


                        data_Sim_['tau'+str(int(10*tau))] = data_Sim__
                    data_1[mtd] = {'F_LP':F_LP_0,'F_LPB0':F_LPB_0,'F_G':F_G_0,'F_GB0':F_GB_0,'F_R':F_R_0,'F_RB0':F_RB_0}


                else:

                    F_LP_0 = []
                    F_LPB_0 = []
                    F_G_0 = []
                    F_GB_0 = []
                    F_R_0 = []
                    F_RB_0 = []
                    TF_LP_0 = []
                    TF_LPB_0 = []
                    TF_G_0 = []
                    TF_GB_0 = []
                    TF_R_0 = []
                    TF_RB_0 = []

                    for cf in [CF[fcfc]]:
                        self.CF = cf
                        F_LP_1 = []
                        F_LPB_1 = []
                        F_G_1 = []
                        F_GB_1 = []
                        F_R_1 = []
                        F_RB_1 = []

                        data_Sim__ = {}

                        for It in range(Iterations):
                            data_c = data_cc[typ+'It'+str(It+1)]
                            O_Mix_ = np.matrix(data0[typ]['It'+str(It+1)]['Omega'])
                            O_Mix = To_list(O_Mix_)
                            P = dist_List(O_Mix[0])
                            datum = data1['It'+str(It+1)][typ][mtd]['tau'+str(int(10*tau))]

                            R1 =[datum[0][i] for i in range(self.L-1)]
                            #RB1 =[datum[1][i] for i in range(self.L-1)]
                            RB1 = []
                            for var_i in range(len(self.theta_var)):
                                RB1.append([datum[1][var_i][i] for i in range(self.L-1)])
                            R1_ =[np.matrix(datum[0][i]) for i in range(self.L-1)]
                            #RB1_ =[np.matrix(datum[1][i]) for i in range(self.L-1)]
                            RB1_ = []
                            for var_i in range(len(self.theta_var)):
                                RB1_.append([np.matrix(datum[1][var_i][i]) for i in range(self.L-1)])
                            #Greedy_For_Fairness

                            List_C_Mix_LP_Im = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,R1_,self.L)
                            O_Mix = To_list(O_Mix_)
                            #List_C_Mix_LP_Ba = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,RB1_,self.L)

                            List_C_Mix_LP_Ba0 = Greedy_For_Fairness(self.CF*self.L*self.WW[typ],O_Mix,RB1_[0],self.L)


                            List_C_Mix_LP =[List_C_Mix_LP_Ba0[JJ][II] +JJ*self.WW[typ]  for JJ in range(len(List_C_Mix_LP_Ba0)) for II in range(len(List_C_Mix_LP_Ba0[JJ]))]

                            data_Sim__['It'+str(It+1)] = Corruption_c(List_C_Mix_LP,self.L*self.WW[typ])

                            F_LP_1.append(self.FCP(R1,P,List_C_Mix_LP_Im,self.WW[typ],True))

                            #F_LPB_1.append(self.FCP(RB1,P,List_C_Mix_LP_Ba,self.WW[typ],True))


                            F_G_1.append(self.FCP(R1,P,data_c['G_R'],self.WW[typ]))
                            #F_GB_1.append(self.FCP(RB1,P,data_c['G_R'],self.WW[typ]))
                            F_R_1.append(self.FCP(R1,P,data_c['R_R'],self.WW[typ]))
                            #F_RB_1.append(self.FCP(RB1,P,data_c['R_R'],self.WW[typ]))

                            F_LPB_1.append(self.FCP(RB1[0],P,List_C_Mix_LP_Ba0,self.WW[typ],True))


                            F_GB_1.append(self.FCP(RB1[0],P,data_c['G_R'],self.WW[typ]))

                            F_RB_1.append(self.FCP(RB1[0],P,data_c['R_R'],self.WW[typ]))

                        F_LP_0.append(Medd([F_LP_1])[0])
                        F_LPB_0.append(Medd([F_LPB_1])[0])
                        F_G_0.append(Medd([F_G_1])[0])
                        F_GB_0.append(Medd([F_GB_1])[0])
                        F_R_0.append(Medd([F_R_1])[0])
                        F_RB_0.append(Medd([F_RB_1])[0])


                        data_Sim_['tau'+str(int(10*tau))] = data_Sim__


                    d1 = {'F_LP':F_LP_0,'F_LPB0':F_LPB_0,'F_G':F_G_0,'F_GB0':F_GB_0,'F_R':F_R_0,'F_RB0':F_RB_0}


                    data_1[mtd] = d1
            data_0[typ] = data_1


        return data_0


#Example


########################################Execution###################################################################


#data0 = Sim.Basic_Analysis()


#data0 = Sim.data_generator(1)


#data = Sim.PDFs(data0)


#data0 = Sim.data_RIPE(2)


