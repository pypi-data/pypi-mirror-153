import pandas as pd
import numpy as np
from utils import *
import os
#need 22 x 5

# d1 = pd.read_csv('results/TCRGP/baseline.txt',names=['es','aucs','aups','none'])
# es,aups = d1['es'].values,d1['aups'].values
# a1 = []
# for i in range(5):
#     a1.append(list(aups[i*22:(i+1)*22]))

# d2 = pd.read_csv('results/TCRGP/tcrpeg_fc.txt',names=['es','aucs','aups','none'])
# aups = d2['aups'].values
# a2 = []
# for i in range(5):
#     a2.append(list(aups[i*22:(i+1)*22]))

# es = es[:22]
# a1,a2 = np.array(a1).T,np.array(a2).T
# Plot = plotting()
# df = Plot.plot_violin(a2,a1,list(es),'results/pictures/tcrgp')
# Plot.plot_sup(a2,a1,'results/pictures/sup_auc')

# #aug for baseline
# d1 = pd.read_csv('results/TCRGP/baseline.txt',names=['es','aucs','aups','none'])
# es,aups = d1['es'].values,d1['aups'].values
# a1 = []
# Plot = plotting()
# for i in range(5):
#     a1.append(list(aups[i*22:(i+1)*22]))
# a1 = np.array(a1).T
# nums = [20,40,60,80,100]
# es = es[:22]
# for num in nums:
#     a2 = []
#     d2 = pd.read_csv('results/TCRGP/aug/baseline/baseline_{}.txt'.format(num),names=['es','aucs','aups','none'])
#     aups = d2['aups'].values

#     for i in range(5):
#         a2.append(list(aups[i*22:(i+1)*22]))
#     a2 = np.array(a2).T
#     df = Plot.plot_violin(a2,a1,list(es),'results/pictures/tcrgp_baseline_{}'.format(num),method1='Augmentation Size - {}'.format(num),method2='Without Augmentation')
#     Plot.plot_sup(a2,a1,'results/pictures/sup_auc_baseline_{}'.format(num),xlabel='Without augmentation',ylabel='Augmentation size - {}'.format(num))

#aug for fc
d1 = pd.read_csv('results/TCRGP/tcrpeg_fc.txt',names=['es','aucs','aups','none'])
es,aups = d1['es'].values,d1['aups'].values
a1 = []
Plot = plotting()
for i in range(5):
    a1.append(list(aups[i*22:(i+1)*22]))
a1 = np.array(a1).T
nums = [20,40,60,80,100]
es = es[:22]
for num in nums:
    a2 = []
    d2 = pd.read_csv('results/TCRGP/aug/fc/tcrpeg_fc_{}.txt'.format(num),names=['es','aucs','aups','none'])
    aups = d2['aups'].values

    for i in range(5):
        a2.append(list(aups[i*22:(i+1)*22]))
    a2 = np.array(a2).T
    df = Plot.plot_violin(a2,a1,list(es),'results/pictures/tcrgp_fc_{}'.format(num),method1='Augmentation Size - {}'.format(num),method2='Without Augmentation')
    Plot.plot_sup(a2,a1,'results/pictures/sup_auc_fc_{}'.format(num),xlabel='Without augmentation',ylabel='Augmentation size - {}'.format(num))
