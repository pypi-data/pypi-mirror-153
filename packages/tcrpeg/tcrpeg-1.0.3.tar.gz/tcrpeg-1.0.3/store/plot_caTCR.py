import pandas as pd
import numpy as np
from utils import *
import os
from collections import defaultdict
from sklearn.metrics import PrecisionRecallDisplay
from sklearn.metrics import precision_recall_curve as pccurve

#plot for auc
dirs = os.listdir('results/caTCR/predictions/')
#dirs = os.listdir('results/sars2/')
dirs_1 = [d for d in dirs if 'auc' in d]
a1 = []
y_trues1 = []
for i in range(5):
    d_peg = pd.read_csv('results/caTCR/predictions/pres_large_2_cross_{}.txt'.format(str(i)),names=['y_pres','y_trues'])
    #d_peg = pd.read_csv('results/sars2/auc_{}.txt'.format(str(i)),names = ['y_trues','y_pres'])
    a1.append(list(d_peg['y_pres'].values))
    y_trues1.append(list(d_peg['y_trues'].values))

# dirs_2 = ['results/caTCR/predictions/' + x for x in dirs if 'deepcat' in x]
# #dirs_2 = [d for d in dirs if 'scores' in d]
# a2= []
# y_trues2 = []
# for d in dirs_2:
#     #d_cat = pd.read_csv('results/sars2/'+ d,names=['y_trues','y_pres'])
#     d_cat = pd.read_csv(d,names=['y_pres','y_trues'])
#     a2.append(list(d_cat['y_pres'].values))
#     y_trues2.append(list(d_cat['y_trues'].values))

# Plot = plotting()
# Plot.plot_auc(a1,a2,y_trues1,y_trues2,name2 = 'DeepCAT',save_name='results/pictures/auc_test_deepcat')


# print(len(y_trues1))
# print(len(y_trues2))
# # Plot.plot_auc(a1,a2,y_trues1,y_trues2,name2 = 'TCRGP')
# Plot.plot_prc(a1,a2,y_trues1,y_trues2,name2 = 'TCRGP')


# display = PrecisionRecallDisplay.from_predictions(y_trues1, d_peg['y_pres'].values, name="LinearSVC")
# display = PrecisionRecallDisplay.from_predictions(y_trues1, d_cat['y_pres'].values, name="JYP")
# plt.xlabel('jyp')
# plt.show()

#Plot.plot_prc(a1,a2,y_trues1,y_trues2,name2='TCRGP',save_name='results/pictures/aup_sars')


# nums = [2000,6000,10000,12000,14000,16000,18000,20000,25000,30000]
# res = defaultdict(list)
# base = 'results/aug_deepcat/'
# for i in range(5):
#     for num in nums:
#         d_cat = pd.read_csv(base + '{}_num_augmented_{}.txt'.format(i+1,num),names=['y_pres','y_trues'])
#         res[num].append(list(d_cat['y_pres'].values))
# y_trues = d_cat['y_trues'].values
# input_ = []
# for num in nums:
#     input_.append(res[num])
# # input_.append(a2)
# # nums.append(0)
# #Plot.plot_auc_aug(input_,y_trues,nums,'results/pictures/auc_aug')
# a2 = [roc_auc_score(y_trues,a) for a in a2]
# input_ = [[roc_auc_score(y_trues,y_pre) for y_pre in temps] for temps in input_]
# Plot.augmentation(nums,input_,a2,save_name='results/pictures/aug_line')


# dirs = os.listdir('results/caTCR/predictions/')
# dirs = [x for x in dirs if 'pres_large' in dirs]
# a2 = []
# y_trues1 = []
# for i in range(5):
#     d_peg = pd.read_csv('results/caTCR/predictions/pres_large_2_cross_{}.txt'.format(str(i)),names=['y_pres','y_trues'])
#     a2.append(list(d_peg['y_pres'].values))
#     y_trues1.append(list(d_peg['y_trues'].values))

Plot = plotting()
# Plot.plot_auc(a1,a2,y_trues1,y_trues2,'results/pictures/auc')
nums = [8000,12000,14000,16000,18000,20000,22000,24000]
file_nums = [int(n/0.4) for n in nums]
res = defaultdict(list)
base = 'results/aug2/predictions/'
res_y = defaultdict(list)
for i in range(5):
    for num in file_nums:
        d_cat = pd.read_csv(base + '{}_pres_large_cross_last_{}.txt'.format(i,num),names=['y_pres','y_trues'])
        res[int(num * 0.4)].append(list(d_cat['y_pres'].values))
        res_y[int(num * 0.4)].append(list(d_cat['y_trues'].values))
input_ = []
input_y = []
for num in nums:
    input_.append(res[num])
    input_y.append(res_y[num])
input_.append(a1)
input_y.append(y_trues1)
nums.append(0)
Plot.plot_auc_aug(input_,input_y,nums)
# a2 = [roc_auc_score(y_trues,a) for a in a2]
# input_ = [[roc_auc_score(y_trues,y_pre) for y_pre in temps] for temps in input_]
# # print(len(input_))
# # print(len(input_[0]))
# Plot.augmentation(nums,input_,a2,save_name='results/pictures/aug_line_tcrpegc')
