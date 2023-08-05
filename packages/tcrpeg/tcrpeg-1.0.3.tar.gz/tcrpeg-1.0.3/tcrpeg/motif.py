import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# dirs = os.listdir('results/motifs/')
# d1 = ['results/motifs/' + d for d in dirs if '_1_' in d]
# d2 = ['results/motifs/'+d for d in dirs if 'means_1_' in d]

# motif1 = list('CASQDLNTGELFF'[1:-1])
# motif1_num = list(range(len(motif1)))

# a1 = []
# for i in range(5):
#     print(d1[i])
#     d = pd.read_csv('results/motifs/_1_{}.txt'.format(str(i)),names=['values'])['values'].values
#     a1.append(d)

# a2 = []
# for i in range(5):
#     d = pd.read_csv('results/motifs/means_1_{}.txt'.format(str(i)),names=['values'])['values'].values
#     a2.append(d)

# fig = plt.figure(figsize=(10,5))
# print(len(np.std(a1,0)))
# print(len(motif1_num))
# plt.errorbar(motif1_num,np.mean(a1,0),yerr=np.std(a1,0),fmt='-o',color='b',label='TCRpeg-c',capsize=5)
# plt.errorbar(motif1_num,np.mean(a2,0),yerr=np.std(a2,0),fmt='-o',color='r',label='TCRGP',capsize=5)
# plt.xticks(motif1_num,motif1,size=12)
# plt.ylabel('Prediction score',size=15)
# plt.legend(loc='lower left',fontsize=15)
# plt.tight_layout()
# plt.savefig('results/pictures/motif1.jpg',dpi=200)


# # d1 = ['results/motifs/' + d for d in dirs if '_5_' in d]
# # print(d1)
# # d2 = ['results/motifs/'+d for d in dirs if 'means_5_' in d]

# motif1 = list('CASSPDIEAFF'[1:-1])
# motif1_num = list(range(len(motif1)))

# a1 = []
# for i in range(5):
#     d = pd.read_csv('results/motifs/_5_{}.txt'.format(str(i)),names=['values'])['values'].values
#     a1.append(d)

# a2 = []
# for i in range(5):
#     d = pd.read_csv('results/motifs/means_5_{}.txt'.format(str(i)),names=['values'])['values'].values
#     a2.append(d)

# fig = plt.figure(figsize=(10,5))
# print(len(np.std(a1,0)))
# print(len(motif1_num))
# plt.errorbar(motif1_num,np.mean(a1,0),yerr=np.std(a1,0),fmt='-o',color='b',label='TCRpeg-c',capsize=5)
# plt.errorbar(motif1_num,np.mean(a2,0),yerr=np.std(a2,0),fmt='-o',color='r',label='TCRGP',capsize=5)
# plt.xticks(motif1_num,motif1,size=12)
# plt.ylabel('Prediction score',size=15)
# plt.legend(loc='lower left',fontsize=15)
# plt.tight_layout()
# plt.savefig('results/pictures/motif5.jpg',dpi=200)


###new motif
motif1 = list('CSAKDRGSQETQYF'[1:-1])
motif1_num = list(range(len(motif1)))
a1 = []
for i in range(5):
    d = pd.read_csv('results/motifs/_ETQYF_{}.txt'.format(str(i)),names=['values'])['values'].values
    a1.append(d)
fig = plt.figure(figsize=(10,5))
print(len(np.std(a1,0)))
print(len(motif1_num))
plt.errorbar(motif1_num,np.mean(a1,0),yerr=np.std(a1,0),fmt='-o',color='b',label='TCRpeg-c',capsize=5)
plt.xticks(motif1_num,motif1,size=12)
plt.ylabel('Prediction score',size=15)
#plt.legend(loc='lower left',fontsize=15)
plt.tight_layout()
plt.savefig('results/pictures/motif_ETQYF.jpg',dpi=200)

motif1 = list('CSARDFLGGYTF'[1:-1])
motif1_num = list(range(len(motif1)))
a1 = []
for i in range(5):
    d = pd.read_csv('results/motifs/_GYTF_{}.txt'.format(str(i)),names=['values'])['values'].values
    a1.append(d)
fig = plt.figure(figsize=(10,5))
print(len(np.std(a1,0)))
print(len(motif1_num))
plt.errorbar(motif1_num,np.mean(a1,0),yerr=np.std(a1,0)/np.sqrt(5),fmt='-o',color='b',label='TCRpeg-c',capsize=5)
plt.xticks(motif1_num,motif1,size=12)
plt.ylabel('Prediction score',size=15)
#plt.legend(loc='lower left',fontsize=15)
plt.tight_layout()
plt.savefig('results/pictures/motif_GYTF.jpg',dpi=200)
