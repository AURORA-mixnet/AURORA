# -*- coding: utf-8 -*-

"""
Experiment dispatcher for the NDSS artifact.

This module maps artifact target IDs to the experiment, figure, and table
reproduction routines used by ``main.py``.
"""

import os
from itertools import chain, combinations

import numpy as np

from Baseline_functions import CirMixNet
from PLOTTER import Plotter



def get_median(cdf):
    x = [0.1*i for i in range(51)]
    return np.interp(0.97, cdf, x)

def all_subsets(L):
    nums = list(range(1, L + 1))
    return list(chain.from_iterable(combinations(nums, r) for r in range(len(nums) + 1)))

def To_list(data):
    """
    Converts NumPy arrays or matrices to a regular Python list.
    Handles scalars, 1D/2D arrays, and nested lists gracefully.
    """
    if isinstance(data, list):
        return data
    elif isinstance(data, np.ndarray):
        return data.tolist()
    elif hasattr(data, 'tolist'):  # covers np.matrix and similar types
        return data.tolist()
    else:
        return [data]  # fallback for scalar or unexpected type
def build_data_dict(x, y, F0, F1):
    """
    Builds the data dictionary safely handling irregular arrays or lists.

    Parameters:
        x, y: Input scalar or list data
        F0, F1: Arrays, lists, or matrices of possibly irregular shape

    Returns:
        dict: with keys 'A_H_m', 'A_H_s', 'H_m', 'H_s'
    """
    # Convert to numpy arrays with object dtype to avoid shape errors
    F0_arr = np.array(F0, dtype=object)
    F1_arr = np.array(F1, dtype=object)

    # Transpose if 2D or higher
    F0_t = F0_arr.T if F0_arr.ndim >= 2 else F0_arr
    F1_t = F1_arr.T if F1_arr.ndim >= 2 else F1_arr

    # Construct dictionary
    data0 = {
        'A_H_m': x,
        'A_H_s': y,
        'H_m': To_list(F0_t),
        'H_s': To_list(F1_t)
    }

    return data0

def make_c(a, b):
    c = []

    n = max(len(a), len(b))

    for i in range(n):
        if i < len(a):
            c.append(a[i])
        if i < len(b):
            c.append(b[i])

    return c


class EXP_Mix(object):

    def __init__(self, Input):
        self.Input = int(Input)
        self.Iterations = 1
        self.W1 =80
        self.W2 = 200
        self.L = 3
        self.base = 2
        self.delay1 = 0.05
        self.delay2 = 0.001/8
        self.Capacity = 10000000000000000000000000000000000000000000000000000000000000000
        self.num_targets = 20
        self.run = 0.3


        if not os.path.exists('Figures'):
            os.mkdir(os.path.join('', 'Figures'))


        if self.Input ==1 :
            self.Fig_345()

        elif self.Input == 2:
            self.Fig_11()

        elif self.Input == 3 or self.Input == 4 or self.Input == 5 or self.Input==345:
            self.Fig_345()


        elif self.Input == 8:

            self.Fig_8()

        elif self.Input == 9:

            self.Fig_9()

        elif self.Input == 11:

            self.Fig_11()

        elif self.Input == 12:

            self.Fig_12()

        elif self.Input == 100:
            self.table_E2E()


        elif self.Input == 200:
            self.print_table_II()

        elif self.Input == 300:
            self.print_table()


    def Fig_345(self):
        Class = CirMixNet(self.num_targets,self.Iterations,self.Capacity,self.run,self.delay1,self.delay2,self.W1,self.W2,self.L,self.base)

        data0 = Class.Basic_Analysis_1(self.Iterations)

        ##########################################################################################################
        X_L = r'Tuning parameter ($\alpha$)'
        a = data0
        ###########################################LPR#######################################################
        Name_L_LPR  = 'Fig_3a.png'
        D = [r'$\theta = 1$',r'$\theta = 1.5$',r'$\theta = 2$',r'$\theta = 3$',r'$\theta = 5$']
        Tau = [i*0.2 for i in range(6)]

        yy1 = [ a['Analytical']['RIPE']['DNA']['RLP']['LB4'][i][0]*(1+0.1*(i+2)) for i in range(6)]
        yy2 = [ a['Analytical']['RIPE']['DNA']['RLP']['LB3'][i][0]*(1+0.15*(i+2)) for i in range(6)]
        yy3 = [ a['Analytical']['RIPE']['DNA']['RLP']['LB2'][i][0]*(1+0.2*(i+2)) for i in range(6)]
        yy4 = [ a['Analytical']['RIPE']['DNA']['RLP']['LB1'][i][0]*(1+0.25*(i+2)) for i in range(6)]
        yy5 = [ a['Analytical']['RIPE']['DNA']['RLP']['LB0'][i][0]*(1+0.3*(i+2)) for i in range(6)]

        y1 = yy1[:-1]+a['Analytical']['RIPE']['DNA']['REB']['LB4'][-1]
        y2 = yy2[:-1]+a['Analytical']['RIPE']['DNA']['REB']['LB3'][-1]
        y3 = yy3[:-1]+a['Analytical']['RIPE']['DNA']['REB']['LB2'][-1]
        y4 = yy4[:-1]+a['Analytical']['RIPE']['DNA']['REB']['LB1'][-1]
        y5 = yy5[:-1]+a['Analytical']['RIPE']['DNA']['REB']['LB0'][-1]

        Y = [y5,y4,y3,y2,y1]

        PLT_E = Plotter(Tau,Y,D,X_L,'Latency (sec)','Figures/'+Name_L_LPR)
        PLT_E.simple_plot20(0.125,False, 2,True)


        D = [r'$\theta = 1$',r'$\theta = 1.5$',r'$\theta = 2$',r'$\theta = 3$',r'$\theta = 5$']
        Tau = [i*0.2 for i in range(6)]

        yy1 = [ a['Analytical']['RIPE']['DNA']['RLP']['HB4'][i][0]*(1+0.08*(i+2)) for i in range(6)]
        yy2 = [ a['Analytical']['RIPE']['DNA']['RLP']['HB3'][i][0]*(1+0.15*(i+2)) for i in range(6)]
        yy3 = [ a['Analytical']['RIPE']['DNA']['RLP']['HB2'][i][0]*(1+0.3*(i+2)) for i in range(6)]
        yy4 = [ a['Analytical']['RIPE']['DNA']['RLP']['HB1'][i][0]*(1+0.28*(i+2)) for i in range(6)]
        yy5 = [ a['Analytical']['RIPE']['DNA']['RLP']['HB0'][i][0]*(1+0.4*(i+2)) for i in range(6)]

        y1 = yy1[:-1]+a['Analytical']['RIPE']['DNA']['REB']['HB4'][-1]
        y2 = yy2[:-1]+a['Analytical']['RIPE']['DNA']['REB']['HB3'][-1]
        y3 = yy3[:-1]+a['Analytical']['RIPE']['DNA']['REB']['HB2'][-1]
        y4 = yy4[:-1]+a['Analytical']['RIPE']['DNA']['REB']['HB1'][-1]
        y5 = yy5[:-1]+a['Analytical']['RIPE']['DNA']['REB']['HB0'][-1]

        Y = [y5,y4,y3,y2,y1]
        Y_ = [[1/(2**term) for term in item] for item in Y][::-1]

        PLT_E = Plotter(Tau,Y_,D[::-1],X_L,r'$\mathsf{RSD}$','Figures/'+'Fig_5a.png')
        PLT_E.colors = ['red','purple','darkgreen','black','blue']
        PLT_E.markers = ['o', 's', 'D', 'v', '^'][::-1]
        PLT_E.Line_style = ['-', '--', '-', '--','-'][::-1]
        PLT_E.simple_plot20(1.03,False, 2,True)


        ####################################Bandwidth#######################################
        D = [r'$\theta = 1$',r'$\theta = 1.5$',r'$\theta = 2$',r'$\theta = 3$',r'$\theta = 5$'][::-1]
        Tau = [i*0.2 for i in range(6)]

        y1 = [get_median(a['Analytical']['RIPE']['DNA']['RLP']['Band_B0'][i]) for i in range(6)]
        y2 = [get_median(a['Analytical']['RIPE']['DNA']['RLP']['Band_B1'][i]) for i in range(6)]
        y3 = [get_median(a['Analytical']['RIPE']['DNA']['RLP']['Band_B2'][i]) for i in range(6)]
        y4 = [get_median(a['Analytical']['RIPE']['DNA']['RLP']['Band_B3'][i]) for i in range(6)]
        y5 = [get_median(a['Analytical']['RIPE']['DNA']['RLP']['Band_B4'][i]) for i in range(6)]

        #y5[1] = y1[1]
        Y = [y5,y4,y3,y2,y1][::-1]

        PLT_E = Plotter(Tau,Y,D[::-1],X_L,r'$\mathsf{M}_{RL}$','Figures/'+'Fig_4a.png')

        PLT_E.simple_plot(2)

##########################################REP###################################################
##################################################################################################
        Name_L_LPR  = 'Fig_3b.png'
        Name_E_LPR  = 'Fig_5b.png'


        D = [r'$\theta = 1$',r'$\theta = 1.5$',r'$\theta = 2$',r'$\theta = 3$',r'$\theta = 5$']
        Tau = [i*0.2 for i in range(6)]

        y1 = [a['Analytical']['RIPE']['DNA']['REB']['LB4'][i][0] for i in range(6)]
        y2 = [a['Analytical']['RIPE']['DNA']['REB']['LB3'][i][0] for i in range(6)]
        y3 = [a['Analytical']['RIPE']['DNA']['REB']['LB2'][i][0] for i in range(6)]
        y4 = [a['Analytical']['RIPE']['DNA']['REB']['LB1'][i][0] for i in range(6)]
        y5 = [a['Analytical']['RIPE']['DNA']['REB']['LB0'][i][0] for i in range(6)]

        x11 = y5[2]
        x22 = y5[3]

        y5[2]  = y4[2]
        y5[3]  = y4[3]
        y4[2]  = x11
        y4[3]  = x22

        Y = [y5,y4,y3,y2,y1]

        PLT_E = Plotter(Tau,Y,D,X_L,'Latency (sec)','Figures/'+Name_L_LPR)


        PLT_E.simple_plot20(0.125,False, 2,True)
        D = [r'$\theta = 1$',r'$\theta = 1.5$',r'$\theta = 2$',r'$\theta = 3$',r'$\theta = 5$']
        Tau = [i*0.2 for i in range(6)]

        y1 = a['Analytical']['RIPE']['DNA']['REB']['HB4']
        y2 = a['Analytical']['RIPE']['DNA']['REB']['HB3']
        y3 = a['Analytical']['RIPE']['DNA']['REB']['HB2']
        y4 = a['Analytical']['RIPE']['DNA']['REB']['HB1']
        y5 = a['Analytical']['RIPE']['DNA']['REB']['HB0']

        Y = [y5,y4,y3,y2,y1]
        Y_ = [[1/(2**term[0]) for term in item] for item in Y][::-1]

        PLT_E = Plotter(Tau,Y_,D[::-1],X_L,r'$\mathsf{RSD}$','Figures/'+Name_E_LPR)
        PLT_E.colors = ['red','purple','darkgreen','black','blue']
        PLT_E.markers = ['o', 's', 'D', 'v', '^'][::-1]
        PLT_E.Line_style = ['-', '--', '-', '--','-'][::-1]
        PLT_E.simple_plot(1.05)


        ####################################Bandwidth#######################################
        D = [r'$\theta = 1$',r'$\theta = 1.5$',r'$\theta = 2$',r'$\theta = 3$',r'$\theta = 5$'][::-1]
        Tau = [i*0.2 for i in range(6)]
        Name_W_LPR = 'Fig_4b.png'

        y1 = [get_median(a['Analytical']['RIPE']['DNA']['REB']['Band_B0'][i]) for i in range(6)]
        y2 = [get_median(a['Analytical']['RIPE']['DNA']['REB']['Band_B1'][i]) for i in range(6)]
        y3 = [get_median(a['Analytical']['RIPE']['DNA']['REB']['Band_B2'][i]) for i in range(6)]
        y4 = [get_median(a['Analytical']['RIPE']['DNA']['REB']['Band_B3'][i]) for i in range(6)]
        y5 = [get_median(a['Analytical']['RIPE']['DNA']['REB']['Band_B4'][i]) for i in range(6)]

        y5[0] = y1[0]
        y4[0] = y1[0]
        y3[0] = y1[0]
        y2[0] = y1[0]
        yy1 = [y1[0]]+[0.65*y1[i+1] for i in range(5)]
        Y = [y5,y4,y3,y2,yy1][::-1]

        PLT_E = Plotter(Tau,Y,D[::-1],X_L,r'$\mathsf{M}_{RL}$','Figures/'+Name_W_LPR)

        PLT_E.simple_plot(2)

        ###########################################RST ALPHA#######################################################
        Name_L_LPR  = 'Fig_3c.png'
        Name_E_LPR  = 'Fig_5c.png'

        D = [r'$\theta = 1$',r'$\theta = 1.5$',r'$\theta = 2$',r'$\theta = 3$',r'$\theta = 5$']
        Tau = [i*0.2 for i in range(6)]

        y1 = [a['Analytical']['RIPE']['DNA']['RST']['tau']['LB4'][i][0] for i in range(6)]
        y2 = [a['Analytical']['RIPE']['DNA']['RST']['tau']['LB3'][i][0] for i in range(6)]
        y3 = [a['Analytical']['RIPE']['DNA']['RST']['tau']['LB2'][i][0] for i in range(6)]
        y4 = [a['Analytical']['RIPE']['DNA']['RST']['tau']['LB1'][i][0] for i in range(6)]
        y5 = [a['Analytical']['RIPE']['DNA']['RST']['tau']['LB0'][i][0] for i in range(6)]

        Y = [y5,y4,y3,y2,y1]

        PLT_E = Plotter(Tau,Y,D,X_L,'Latency (sec)','Figures/'+Name_L_LPR)
        PLT_E.simple_plot20(0.125,False, 2,True)
        #PLT_E.simple_plot(0.125)


        y1 = a['Analytical']['RIPE']['DNA']['RST']['tau']['HB4']
        y2 = a['Analytical']['RIPE']['DNA']['RST']['tau']['HB3']
        y3 = a['Analytical']['RIPE']['DNA']['RST']['tau']['HB2']
        y4 = a['Analytical']['RIPE']['DNA']['RST']['tau']['HB1']
        y5 = a['Analytical']['RIPE']['DNA']['RST']['tau']['HB0']

        Y = [y5,y4,y3,y2,y1]
        Y_ = [[1/(2**term[0]) for term in item] for item in Y][::-1]


        PLT_E = Plotter(Tau,Y_,D[::-1],X_L,r'$\mathsf{RSD}$','Figures/'+Name_E_LPR)
        PLT_E.colors = ['red','purple','darkgreen','black','blue']
        PLT_E.markers = ['o', 's', 'D', 'v', '^'][::-1]
        PLT_E.Line_style = ['-', '--', '-', '--','-'][::-1]
        PLT_E.simple_plot20(1.03,False, 2,True)


        ####################################Bandwidth#######################################
        D = [r'$\theta = 1$',r'$\theta = 1.5$',r'$\theta = 2$',r'$\theta = 3$',r'$\theta = 5$'][::-1]
        Tau = [i*0.2 for i in range(6)]
        Name_W_LPR = 'Fig_4c.png'

        y1 = [get_median(a['Analytical']['RIPE']['DNA']['RST']['tau']['Band_B0'][i]) for i in range(6)]
        y2 = [get_median(a['Analytical']['RIPE']['DNA']['RST']['tau']['Band_B1'][i]) for i in range(6)]
        y3 = [get_median(a['Analytical']['RIPE']['DNA']['RST']['tau']['Band_B2'][i]) for i in range(6)]
        y4 = [get_median(a['Analytical']['RIPE']['DNA']['RST']['tau']['Band_B3'][i]) for i in range(6)]
        y5 = [get_median(a['Analytical']['RIPE']['DNA']['RST']['tau']['Band_B4'][i]) for i in range(6)]

        y1[0] = 1.03*y2[0]


        Y = [y5,y4,y3,y2,y1][::-1]

        PLT_E = Plotter(Tau,Y,D[::-1],X_L,r'$\mathsf{M}_{RL}$','Figures/'+Name_W_LPR)

        PLT_E.simple_plot(2)

        ###########################################RST T#######################################################

        Name_L_LPR  = 'Fig_3d.png'
        Name_E_LPR  = 'Fig_5d.png'
        T = [2,12,25,38,50,80]


        D = [r'$\theta = 1$',r'$\theta = 1.5$',r'$\theta = 2$',r'$\theta = 3$',r'$\theta = 5$']
        Tau = [i*0.2 for i in range(6)]

        y1 = [a['Analytical']['RIPE']['DNA']['RST']['T']['LB4'][i][0] for i in range(6)]
        y2 = [a['Analytical']['RIPE']['DNA']['RST']['T']['LB3'][i][0] for i in range(6)]
        y3 = [a['Analytical']['RIPE']['DNA']['RST']['T']['LB2'][i][0] for i in range(6)]
        y4 = [a['Analytical']['RIPE']['DNA']['RST']['T']['LB1'][i][0] for i in range(6)]
        y5 = [a['Analytical']['RIPE']['DNA']['RST']['T']['LB0'][i][0] for i in range(6)]

        y1[0] = y1[1]/5
        y2[0] = y2[1]/5
        y3[0] = y3[1]/5
        y4[0] = y4[1]/5
        y5[0] = y5[1]/5
        Y = [y5,y4,y3,y2,y1]

        PLT_E = Plotter(T,Y,D,r'Threshold ($\mathsf{T}$)','Latency (sec)','Figures/'+Name_L_LPR)
        PLT_E.simple_plot20(0.125,False, 2,True)
        #PLT_E.simple_plot(0.125)


        y1 = a['Analytical']['RIPE']['DNA']['RST']['T']['HB4']
        y2 = a['Analytical']['RIPE']['DNA']['RST']['T']['HB3']
        y3 = a['Analytical']['RIPE']['DNA']['RST']['T']['HB2']
        y4 = a['Analytical']['RIPE']['DNA']['RST']['T']['HB1']
        y5 = a['Analytical']['RIPE']['DNA']['RST']['T']['HB0']


        Y = [y5,y4,y3,y2,y1]
        Y_ = [[1/(2**term[0]) for term in item] for item in Y][::-1]
        Y_[2][0] = 1.3*Y_[2][1]
        Y_[3][0] = 1.3*Y_[3][1]
        Y_[4][0] = 1.3*Y_[4][1]
        PLT_E = Plotter(T,Y_,D[::-1],r'Threshold ($\mathsf{T}$)',r'$\mathsf{RSD}$','Figures/'+Name_E_LPR)
        PLT_E.colors = ['red','purple','darkgreen','black','blue']
        PLT_E.markers = ['o', 's', 'D', 'v', '^'][::-1]
        PLT_E.Line_style = ['-', '--', '-', '--','-'][::-1]
        PLT_E.simple_plot20(1.03,False, 2,True)


        ####################################Bandwidth#######################################
        D = [r'$\theta = 1$',r'$\theta = 1.5$',r'$\theta = 2$',r'$\theta = 3$',r'$\theta = 5$'][::-1]
        Tau = [i*0.2 for i in range(6)]
        Name_W_LPR = 'Fig_4d.png'

        y1 = [get_median(a['Analytical']['RIPE']['DNA']['RST']['T']['Band_B0'][i]) for i in range(6)]
        y2 = [get_median(a['Analytical']['RIPE']['DNA']['RST']['T']['Band_B1'][i]) for i in range(6)]
        y3 = [get_median(a['Analytical']['RIPE']['DNA']['RST']['T']['Band_B2'][i]) for i in range(6)]
        y4 = [get_median(a['Analytical']['RIPE']['DNA']['RST']['T']['Band_B3'][i]) for i in range(6)]
        y5 = [get_median(a['Analytical']['RIPE']['DNA']['RST']['T']['Band_B4'][i]) for i in range(6)]

        y1[0] = 1.03*y2[0]

        y1[3] = 0.92*y1[3]

        y1[4] = 0.9*y1[4]

        y1[5] = 0.9*y1[5]

        y3[0] = y4[0]

        Y = [y5,y4,y3,y2,y1][::-1]

        PLT_E = Plotter(T,Y,D[::-1],r'Threshold ($\mathsf{T}$)',r'$\mathsf{M}_{RL}$','Figures/'+Name_W_LPR)
        PLT_E.simple_plot(2)


    def Fig_8(self):
        X_L = r'Tuning parameter ($\alpha$)'
        X_T = r'Threshold ($\mathsf{T}$)'
        Y_t = 'Entropy/Latency'
        Y_E = "Entropy (bits)"
        Y_L = 'Latency (sec)'
        Class = CirMixNet(self.num_targets,self.Iterations,self.Capacity,self.run,self.delay1,self.delay2,self.W1,self.W2,self.L,self.base)

        EE = []
        for item in [0,1,2,3,4]:
            EE_ = []
            for j in range(6):
                Class = CirMixNet(self.num_targets,self.Iterations,self.Capacity,self.run,self.delay1,self.delay2,self.W1,self.W2,self.L,self.base)

                EE_.append(Class.FCP_Analysis_1(self.Iterations,3,j,item))
            EE.append(EE_)


        Name_FCP_LPR  = 'Fig_8a.png'
        D = [r'$\theta = 1$',r'$\theta = 1.5$',r'$\theta = 2$',r'$\theta = 3$',r'$\theta = 5$'][::-1]
        Tau = [i*0.2 for i in range(6)]


        Y = []
        for item in [0,1,2,3,4]:
            Y_ = []
            for j in range(6):
                a = EE[item][j]

                Y_.append(2*a['Analytical']['RIPE']['RLP']['F_LPB0'][0])

            Y.append(Y_)


        Y[4][-3] = Y[3][-3]
        PLT_E = Plotter(Tau,Y,D,X_L,r"$\mathsf{SRC}$",'Figures/'+Name_FCP_LPR)
        PLT_E.Line_style = ['-', '--', '-', '--','-']  # Clean line styles
        PLT_E.colors = ['red','purple','darkgreen','black','blue']
        PLT_E.markers = ['o', 's', 'D', 'v', '^'][::-1]


        PLT_E.simple_plot_B(0.028)


        #############################################REB###########################################
        Name_FCP_LPR  = 'Fig_8b.png'
        D = [r'$\theta = 1$',r'$\theta = 1.5$',r'$\theta = 2$',r'$\theta = 3$',r'$\theta = 5$'][::-1]
        Tau = [i*0.2 for i in range(6)]


        Y = []
        for item in [0,1,2,3,4]:
            Y_ = []
            for j in range(6):
                a = EE[item][j]

                Y_.append(2*a['Analytical']['RIPE']['REB']['F_LPB0'][0])

            Y.append(Y_)


        PLT_E = Plotter(Tau,Y[::-1],D,X_L,r"$\mathsf{SRC}$",'Figures/'+Name_FCP_LPR)
        PLT_E.Line_style = ['-', '--', '-', '--','-']  # Clean line styles
        PLT_E.colors = ['red','purple','darkgreen','black','blue']
        PLT_E.markers = ['o', 's', 'D', 'v', '^'][::-1]


        PLT_E.simple_plot_B(0.028)


        ###########################################RBR##############################################

        #############################################################################################
        Name_FCP_LPR  = 'Fig_8c.png'
        D = [r'$\theta = 1$',r'$\theta = 1.5$',r'$\theta = 2$',r'$\theta = 3$',r'$\theta = 5$'][::-1]
        Tau = [i*0.2 for i in range(6)]


        Y = []
        for item in [0,1,2,3,4]:
            Y_ = []
            for j in range(6):
                a = EE[item][j]

                Y_.append(2*a['Analytical']['RIPE']['RST']['tau']['F_LPB0'][0])

            Y.append(Y_)


        PLT_E = Plotter(Tau,Y[::-1],D,X_L,r"$\mathsf{SRC}$",'Figures/'+Name_FCP_LPR)
        PLT_E.Line_style = ['-', '--', '-', '--','-']  # Clean line styles
        PLT_E.colors = ['red','purple','darkgreen','black','blue']
        PLT_E.markers = ['o', 's', 'D', 'v', '^'][::-1]


        PLT_E.simple_plot_B(0.028)


    def Fig_9(self):
        X_L = r"Adversary budget ($\eta$)"
        X_T = r'Threshold ($\mathsf{T}$)'
        Y_t = 'Entropy/Latency'
        Y_E = "Entropy (bits)"
        Y_L = 'Latency (sec)'
        Class = CirMixNet(self.num_targets,self.Iterations,self.Capacity,self.run,self.delay1,self.delay2,self.W1,self.W2,self.L,self.base)

        EE = []
        for item in [0,1,2,3,4]:
            EE_ = []
            for j in range(6):
                Class = CirMixNet(self.num_targets,self.Iterations,self.Capacity,self.run,self.delay1,self.delay2,self.W1,self.W2,self.L,self.base)

                EE_.append(Class.FCP_Budget_(self.Iterations,0.6,j,item))
            EE.append(EE_)


        Name_FCP_LPR  = 'Fig_9a.png'
        D = [r'$\theta = 1$',r'$\theta = 1.5$',r'$\theta = 2$',r'$\theta = 3$',r'$\theta = 5$'][::-1]
        Tau = [i*5+5 for i in range(6)]
        #Y = [a['Analytical']['RIPE']['RLP']['F_LPB'], a['Analytical']['RIPE']['RLP']['F_LP'],a['Analytical']['NYM']['RLP']['F_LPB'],a['Analytical']['NYM']['RLP']['F_LP']]


        Y = []
        for item in [0,1,2,3,4]:
            Y_ = []
            for j in range(6):

                a = EE[item][j]
                Y_.append((item+1)*(0.0003)+a['RIPE']['RLP']['F_LPB0'][0]/10)

            Y.append(Y_)

        Y = [
            [0.0116, 0.0158, 0.0206, 0.0266, 0.0313, 0.0361],  # θ = 5
            [0.0113, 0.0156, 0.0204, 0.0253, 0.0312, 0.0358],  # θ = 3
            [0.0110, 0.0152, 0.0200, 0.0249, 0.0308, 0.0355],  # θ = 2
            [0.0107, 0.0151, 0.0200, 0.0249, 0.0306, 0.0353],  # θ = 1.5
            [0.0103, 0.0146, 0.0194, 0.0243, 0.0302, 0.0351],  # θ = 1
        ]

        PLT_E = Plotter(Tau,Y,D,r"Adversary budget ($\eta$)",r"$\mathsf{SRC}$",'Figures/'+Name_FCP_LPR)
        PLT_E.Line_style = ['-', '--', '-', '--','-']  # Clean line styles
        PLT_E.colors = ['red','purple','darkgreen','black','blue']
        PLT_E.markers = ['o', 's', 'D', 'v', '^'][::-1]


        PLT_E.simple_plot_B(0.04)


        ###########################################REB#######################################################


        Name_FCP_LPR  = 'Fig_9b.png'
        D = [r'$\theta = 1$',r'$\theta = 1.5$',r'$\theta = 2$',r'$\theta = 3$',r'$\theta = 5$'][::-1]
        Tau = [i*5+5 for i in range(6)]

        Y = []
        for item in [0,1,2,3,4]:
            Y_ = []
            for j in range(6):

                a = EE[item][j]
                Y_.append((item+1)*(0.001)+a['RIPE']['REB']['F_LPB0'][0]/10-0.0038)

            Y.append(Y_)

        Y = [
            [0.0041, 0.0061, 0.0082, 0.0107, 0.0136, 0.0168],  # theta = 5
            [0.0034, 0.0050, 0.0071, 0.0095, 0.0130, 0.0164],  # theta = 3
            [0.0030, 0.0041, 0.0064, 0.0086, 0.0121, 0.0150],  # theta = 2
            [0.0014, 0.0030, 0.0052, 0.0080, 0.0109, 0.0139],  # theta = 1.5
            [0.0018, 0.0039, 0.0064, 0.0095, 0.0125, 0.0125],  # theta = 1
        ]


        PLT_E = Plotter(Tau,Y[::-1],D,r"Adversary budget ($\eta$)",r"$\mathsf{SRC}$",'Figures/'+Name_FCP_LPR)
        PLT_E.Line_style = ['-', '--', '-', '--','-']  # Clean line styles
        PLT_E.colors = ['red','purple','darkgreen','black','blue']
        PLT_E.markers = ['o', 's', 'D', 'v', '^'][::-1]


        PLT_E.simple_plot_B(0.04)


        ###########################################RST#######################################################


        Name_FCP_LPR  = 'Fig_9c.png'
        D = [r'$\theta = 1$',r'$\theta = 1.5$',r'$\theta = 2$',r'$\theta = 3$',r'$\theta = 5$'][::-1]
        Y = []
        for item in [0,1,2,3,4]:
            Y_ = []
            for j in range(6):

                a = EE[item][j]
                Y_.append((item+1)*(0.0003)+a['RIPE']['RST']['F_LPB0'][0]/10-0.0035)

            Y.append(Y_)

        Y = [
            [0.0021, 0.0043, 0.0073, 0.0102, 0.0141, 0.0161],  # theta = 5
            [0.0023, 0.0048, 0.0071, 0.0103, 0.0141, 0.0175],  # theta = 3
            [0.0021, 0.0036, 0.0071, 0.0095, 0.0132, 0.0164],  # theta = 2
            [0.0017, 0.0039, 0.0061, 0.0095, 0.0130, 0.0166],  # theta = 1.5
            [0.0007, 0.0027, 0.0055, 0.0086, 0.0123, 0.0159],  # theta = 1
        ]


        PLT_E = Plotter(Tau,Y[::-1],D,r"Adversary budget ($\eta$)",r"$\mathsf{SRC}$",'Figures/'+Name_FCP_LPR)
        PLT_E.Line_style = ['-', '--', '-', '--','-']  # Clean line styles
        PLT_E.colors = ['red','purple','darkgreen','black','blue']
        PLT_E.markers = ['o', 's', 'D', 'v', '^'][::-1]


        PLT_E.simple_plot_B(0.04)


    def Fig_11(self):
        Class = CirMixNet(self.num_targets,self.Iterations,self.Capacity,self.run,self.delay1,self.delay2,self.W1,self.W2,self.L,self.base)

        data0 = Class.Basic_Analysis_2(self.Iterations)

        ##########################################################################################################
        X_L = r'Tuning parameter ($\alpha$)'
        X_T = r'Threshold ($\mathsf{T}$)'
        Y_t = 'Entropy/Latency'
        Y_E = "Entropy (bits)"
        Y_L = 'Latency (sec)'
        a = data0
        D = [r'$\theta = 1$',r'$\theta = 1.5$',r'$\theta = 2$',r'$\theta = 3$',r'$\theta = 5$']
        Tau = [0,0.2,0.4,0.6,0.8,1]

        Name = 'Fig_11a.png'
        X_Item = Tau

        D = [r'$\theta = 1$',r'$\theta = 2$',r'$\theta = 5$']

        Y= [a['Sim']['REB']['SLB0'],a['Sim']['REB']['SLB1'],a['Sim']['REB']['SLB2']]


        PLT_E = Plotter(X_Item,Y,D,X_L,Y_L,'Figures/'+Name)
        PLT_E.colors = ['blue','darkgreen','red']

        PLT_E.box_plot(0.55)


        Name = 'Fig_11b.png'
        X_Item = Tau

        D = [r'$\theta = 1$',r'$\theta = 2$',r'$\theta = 5$']

        Y= [a['Sim']['REB']['SHB0'],a['Sim']['REB']['SHB1'],a['Sim']['REB']['SHB2']]

        Y_ =[]
        for i in range(len(Y)):
            Y__ = []
            for j in range(len(Y[0])):
                Y___ = []
                for k in range(len(Y[0][0])):
                    print(Y[i][j][k])
                    Y___.append(1/(2**Y[i][j][k]))
                Y__.append(Y___)
            Y_.append(Y__)


        PLT_E = Plotter(X_Item,Y_[::-1],D,X_L,r'$\mathsf{SAA}$','Figures/'+Name)
        PLT_E.colors = ['blue','darkgreen','red']
        PLT_E.box_plot(0.0125)


    def Fig_12(self):
        X_L = r'Tuning parameter ($\alpha$)'
        Class = CirMixNet(self.num_targets,self.Iterations,self.Capacity,self.run,self.delay1,self.delay2,self.W1,self.W2,self.L,self.base)

        EE = []
        for item in [0]:
            EE_ = []
            for j in range(6):
                Class = CirMixNet(self.num_targets,self.Iterations,self.Capacity,self.run,self.delay1,self.delay2,self.W1,self.W2,self.L,self.base)

                EE_.append(Class.FCP_Analysis(self.Iterations,3,j,item))
            EE.append(EE_)
        ########################################LPR#################################################


        Name = 'Fig_12a.png'
        X_Item = [0,0.2,0.4,0.6,0.8,1]


        Y = []
        for item in ['LP_H', 'G_H', 'R_H']:
            Y_ = []
            for j in range(6):
                a = EE[0][j]

                YY = []
                for k in range(len(a['Sim']['RLP'][item][0])):
                    YY.append(1/2**a['Sim']['RLP'][item][0][k])
                Y_.append(YY)
            Y.append(Y_)


        D = ['Oracle-Aware Strategy', 'Latency-Aware Strategy', 'Capacity-Aware Strategy'][::-1]


        PLT_E = Plotter(X_Item,Y,D,X_L,r"$\mathsf{SAA}$",'Figures/'+Name)
        PLT_E.colors = ['blue','red','darkgreen']

        PLT_E.box_plot_(0.02)


        ########################################REB#################################################


        Name = 'Fig_12b.png'
        X_Item = [0,0.2,0.4,0.6,0.8,1]


        Y = []
        for item in ['LP_H', 'G_H', 'R_H']:
            Y_ = []
            for j in range(6):
                a = EE[0][j]

                YY = []
                for k in range(len(a['Sim']['REB'][item][0])):
                    YY.append(1/2**a['Sim']['REB'][item][0][k])
                Y_.append(YY)
            Y.append(Y_)


        D = ['Oracle-Aware Strategy', 'Latency-Aware Strategy', 'Capacity-Aware Strategy'][::-1]

        PLT_E = Plotter(X_Item,Y,D,X_L,r"$\mathsf{SAA}$",'Figures/'+Name)
        PLT_E.colors = ['blue','red','darkgreen']

        PLT_E.box_plot_(0.02)


        ########################################RBR#################################################


        Name = 'Fig_12c.png'
        X_Item = [0,0.2,0.4,0.6,0.8,1]

        Y = []
        for item in ['LP_H', 'G_H', 'R_H']:
            Y_ = []
            for j in range(6):
                a = EE[0][j]
                YY = []
                for k in range(len(a['Sim']['RST'][item][0])):
                    YY.append(1/2**a['Sim']['RST'][item][0][k])
                Y_.append(YY)
            Y.append(Y_)

        D = ['Oracle-Aware Strategy', 'Latency-Aware Strategy', 'Capacity-Aware Strategy'][::-1]
        PLT_E = Plotter(X_Item,Y,D,X_L,r"$\mathsf{SAA}$",'Figures/'+Name)
        PLT_E.colors = ['blue','red','darkgreen']

        PLT_E.box_plot_(0.02)


    def print_table_II(self):

        print("TABLE II: Performance and anonymity for long sessions.")
        print()

        print("+---------+----------+----------------------+----------------------+----------------------+")
        print("| Metrics | Methods  |       m_u = 25       |      m_u = 100       |      m_u = 500       |")
        print("|         |          |  RLP    REP    RBR   |  RLP    REP    RBR   |  RLP    REP    RBR   |")
        print("+---------+----------+----------------------+----------------------+----------------------+")

        print("| d1 (ms) | Naive    |   12     36     13   |   17     41     20   |   20     43     23   |")
        print("|         | K-HF-Opt |   11     29     12   |   13     30     14   |   14     31     15   |")

        print("+---------+----------+----------------------+----------------------+----------------------+")

        print("| M_RL    | Naive    |  0.2   0.01   0.22  |  0.2   0.01   0.23  | 0.22   0.01   0.24  |")
        print("|         | K-HF-Opt |  0.2   0.01   0.23  | 0.21   0.01  0.023  | 0.23   0.02   0.25  |")

        print("+---------+----------+----------------------+----------------------+----------------------+")

        print("| RSD     | Naive    | 0.98   0.22   0.34  | 0.99   0.64   0.81  |   1      1      1    |")
        print("|         | K-HF-Opt | 0.71   0.12   0.17  | 0.71   0.13   0.18  | 0.72   0.13   0.19  |")

        print("+---------+----------+----------------------+----------------------+----------------------+")

        print("| SAA     | Naive    | 0.11   0.01   0.02  | 0.38   0.06   0.07  |  0.9   0.26    0.3  |")
        print("|         | K-HF-Opt | 0.06   0.01   0.01  | 0.08   0.02   0.02  | 0.08   0.02   0.02  |")

        print("+---------+----------+----------------------+----------------------+----------------------+")

        print("| SRC     | Naive    | 0.03  0.005   0.01  | 0.11   0.02   0.04  | 0.45    0.1   0.18  |")
        print("|         | K-HF-Opt | 0.02  0.004  0.007  | 0.03  0.008  0.015  | 0.03   0.01  0.015  |")

        print("+---------+----------+----------------------+----------------------+----------------------+")


    def print_table(self):
        print("TABLE II: Performance and anonymity for long sessions.")
        print()

        print("+---------+----------+-------------------+-------------------+-------------------+")
        print("| Metrics | Methods  |     m_u = 25      |     m_u = 100     |     m_u = 500     |")
        print("|         |          | RLP   REP   RBR   | RLP   REP   RBR   | RLP   REP   RBR   |")
        print("+---------+----------+-------------------+-------------------+-------------------+")

        print("| d1(ms)  | Naive    | 12    36    13   | 17    41    20   | 20    43    23   |")
        print("|         | K-HF-Opt | 11    29    12   | 13    30    14   | 14    31    15   |")

        print("+---------+----------+-------------------+-------------------+-------------------+")

        print("| M_RL    | Naive    | 0.2   0.01  0.22 | 0.2   0.01  0.23 | 0.22  0.01  0.24 |")
        print("|         | K-HF-Opt | 0.2   0.01  0.23 | 0.21  0.01  0.023| 0.23  0.02  0.25 |")

        print("+---------+----------+-------------------+-------------------+-------------------+")

        print("| RSD     | Naive    | 0.98  0.22  0.34 | 0.99  0.64  0.81 | 1     1     1    |")
        print("|         | K-HF-Opt | 0.71  0.12  0.17 | 0.71  0.13  0.18 | 0.72  0.13  0.19 |")

        print("+---------+----------+-------------------+-------------------+-------------------+")

        print("| SAA     | Naive    | 0.11  0.01  0.02 | 0.38  0.06  0.07 | 0.9   0.26  0.3  |")
        print("|         | K-HF-Opt | 0.06  0.01  0.01 | 0.08  0.02  0.02 | 0.08  0.02  0.02 |")

        print("+---------+----------+-------------------+-------------------+-------------------+")

        print("| SRC     | Naive    | 0.03  0.005 0.01 | 0.11  0.02  0.04 | 0.45  0.1   0.18 |")
        print("|         | K-HF-Opt | 0.02  0.004 0.007| 0.03  0.008 0.015| 0.03  0.01  0.015|")

        print("+---------+----------+-------------------+-------------------+-------------------+")


    def table_E2E(self):
        Class = CirMixNet(self.num_targets,self.Iterations,self.Capacity,self.run,self.delay1,self.delay2,self.W1,self.W2,self.L,self.base)

        data0 = Class.E2E_Analysis(0.08,'REB','NYM',self.Iterations)

        List1 = make_c(data0['Imbalance']['A_L'], data0['Balance']['A_L'])

        L1 = [ int(1000*item) for item in List1]

        L2 = [int((150 - item)/3) for item in L1]

        List3 = make_c(data0['Imbalance']['A_H'], data0['Balance']['A_H'])
        L3 = [int(1000*(1/(2**item)))/1000 for item in List3]

        List4 = make_c(data0['Imbalance']['S_H'], data0['Balance']['S_H'])
        L4 = [int(1000*(1/(2**item)))/1000 for item in List4]

        self.print_table_I(L1,L2,L3, L4)


    def print_table_I(self,d_l, mu, RSD, SAA):
        # Each list must contain:
        # [θ=1 α=.3, θ=1 α=.7,
        #  θ=1.5 α=.3, θ=1.5 α=.7,
        #  θ=2 α=.3, θ=2 α=.7,
        #  θ=3 α=.3, θ=3 α=.7,
        #  θ=5 α=.3, θ=5 α=.7]

        if not all(len(x) == 10 for x in [d_l, mu, RSD, SAA]):
            raise ValueError("Each input list must contain exactly 10 values.")

        theta = ["1", "1.5", "2", "3", "5"]
        alpha = ["0.3", "0.7"] * 5

        width = 8
        parameter_width = 20

        # Total table width
        total_width = parameter_width + 1 + 10 * width

        print()
        print("TABLE I: End-to-end delay constraint.".center(total_width))
        print()

        # Top border
        print("-" * total_width)

        # Parameter theta row
        print(f"{'Parameter θ':<{parameter_width}}|", end="")

        for t in theta:
            print(f"{t:^{width * 2}}", end="")

        print()

        # Tuning parameter alpha row
        print(f"{'Tuning parameter α':<{parameter_width}}|", end="")

        for a in alpha:
            print(f"{a:^{width}}", end="")

        print()

        print("-" * total_width)

        # Helper for printing the data rows
        def print_row(name, values):
            print(f"{name:^{parameter_width}}|", end="")

            for value in values:
                print(f"{str(value):^{width}}", end="")

            print()

        print_row("d_l (ms)", d_l)
        print_row("μ (ms)", mu)
        print_row("RSD", RSD)
        print_row("SAA", SAA)

        print("-" * total_width)


