# -*- coding: utf-8 -*-

"""
Discrete-event mix-network simulation.

This module constructs the SimPy environment, mix nodes, and message process,
then returns latency and entropy measurements.
"""

import math
import random
import statistics

import numpy as np
import simpy

from Message_Genartion_and_mix_net_processing_ import Message_Genartion_and_mix_net_processing
from Mix_Node_ import Mix
from NYM import MixNet



# Import library for making the simulation, making random choices,
#creating exponential delays, and defining matrixes.


def Analytical(nn):
    a = 1/(nn+1)
    b = nn*a
    s = 0
    for i in range(10000):
        s = s - (a*(b**i))*(math.log((a*(b**i))))/(math.log(math.exp(1)))


    return s


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

class Simulation(object):

    def __init__(self,Targets,run,delay1,delay2,N,L ):
        self.d1 = delay1
        self.d2 = delay2

        self.N_target = Targets
        self.N = N

        self.run = run
        self.L = L
        self.W = round(self.N/self.L)


    def Simulator(self,corrupted_Mix,Mix_dict,nn):
        Mixes = [] #All mix nodes

        env = simpy.Environment()    #simpy environment
        capacity=[]
        Capp = 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
        for j in range(self.N):# Generating capacities for mix nodes
            c = simpy.Resource(env,capacity = Capp)
            capacity.append(c)
        for i in range(self.N):#Generate enough instantiation of mix nodes
            ll = i +1
            X = corrupted_Mix['PM%d' %ll]
            x = Mix(env,'M%02d' %i,capacity[i],X,self.N_target,self.d1)
            Mixes.append(x)


        MNet = MixNet(env,Mixes,self.L)  #Generate an instantiation of the mix net
        random.seed(42)

        Process = Message_Genartion_and_mix_net_processing(env,Mixes,Capp,Mix_dict,MNet,self.N_target,self.d2,self.W,nn)


        env.process(Process.Prc())  #process the simulation

        env.run(until = self.run)  #Running time


        Latencies = MNet.LL

        Distributions = np.matrix(MNet.EN)
        DT = np.transpose(Distributions)
        ENT = []

        for i in range(self.N_target):
            llll = DT[i,:].tolist()[0]
            ENT.append(Ent(llll))
        return Latencies,ENT


