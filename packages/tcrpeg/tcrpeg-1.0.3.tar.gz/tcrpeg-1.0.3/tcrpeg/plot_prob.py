from utils import *
import pandas as pd
import numpy as np
from collections import defaultdict
from matplotlib.lines import Line2D
from evaluate import evaluation
from tcrpeg.TCRpeg import TCRpeg
import os
from scipy.stats import pearsonr as pr

np.random.seed(0)
Plot = plotting()
model = TCRpeg(hidden_size=64,num_layers = 3,load_data=False,embedding_path='data/embedding_32.txt')
# path = '../../nlp_vae/results/models/11_22_2021/19:35:40/only_decoder_11_22_2021-19:35:40_40.pth'
path = 'results/models/15:07:30/model.pth'
model.create_model(load=True,path=path)

eva = evaluation(model=model,frac=0.1)

#prob plot
ks = []
_,_,p_data,p_tcrpeg = eva.eva_prob('../../nlp_vae/data/pdf_test_sonnia.csv',whole=False)
print('done calculating')

fig=plt.figure(figsize=(5,3),dpi=200)
ax1=plt.subplot(111)
ax1.set_ylim([-21,0])
ax1.set_xlim([-5.5,-2.5])
ax1.locator_params(nbins=4)
ax1.set_xlabel(r'$log_{10}P_{data}$')
ax1.set_ylabel(r'$log_{10}P_{infer}$')
ax1.plot([-5.5, -2.5], [-5.5, -2.5], color='k', linestyle='-', linewidth=2)
#Plot.density_scatter(np.log10(p_data),np.log10(p_tcrpeg),bins = [10,50],ax=ax1,fig_name='prob_tcrpeg',method='TCRpeg')
Plot.density_scatter(np.log10(p_data),np.log10(p_tcrpeg),bins = [10,50],ax=ax1,fig_name='prob_tcrpeg',method='TCRpeg')
ks.append(pr(p_data,p_tcrpeg)[0])
for i in range(4):
    _,_,p_data,p_tcrpeg = eva.eva_prob('../../nlp_vae/data/pdf_test_sonnia.csv',whole=False)
    ks.append(pr(p_data,p_tcrpeg)[0])
mean,std = round(np.mean(ks),4),round(np.std(ks),4)
#mean = 0.896
ax1.text(0.65, 0.32, r'r = %0.3f $\pm$ %0.3f' % (mean, std) , ha='center', va='center',transform = ax1.transAxes,size=10,color='k')
plt.tight_layout()
plt.savefig('results/pictures/prob_tcrpeg_20000.jpg',dpi=200)

# #sonnia
# ks = []
# d_sonnia = pd.read_csv('results/probs/pdf_test_sonnia_20000_0.csv')
# count,p_sonnia = d_sonnia['count'].values,d_sonnia['p_sonnia'].values
# p_sonnia += 1e-25 #to avoid 0
# p_data_sonnia,p_sonnia = count / np.sum(count), p_sonnia/np.sum(p_sonnia)
# print(kl_divergence(p_data_sonnia,p_sonnia))
# print(pr(p_data_sonnia,p_sonnia)[0])
# fig=plt.figure(figsize=(5,3),dpi=200)
# ax1=plt.subplot(111)
# ax1.set_ylim([-21,0])
# ax1.set_xlim([-5.5,-2.5])
# ax1.locator_params(nbins=4)
# ax1.set_xlabel(r'$log_{10}P_{data}$')
# ax1.set_ylabel(r'$log_{10}P_{infer}$')
# ax1.plot([-5.5, -2.5], [-5.5, -2.5], color='k', linestyle='-', linewidth=2)
# Plot.density_scatter(np.log10(p_data_sonnia),np.log10(p_sonnia) ,bins = [10,50],ax=ax1,method='soNNia')
# ks.append(pr(p_data_sonnia,p_sonnia)[0])
# for i in range(4):
#     d_sonnia = pd.read_csv('results/probs/pdf_test_sonnia_{}.csv'.format(i+1))
#     count,p_sonnia = d_sonnia['count'].values,d_sonnia['p_sonnia'].values
#     p_sonnia += 1e-25 #to avoid 0
#     p_data_sonnia,p_sonnia = count / np.sum(count), p_sonnia/np.sum(p_sonnia)
#     ks.append(pr(p_data_sonnia,p_sonnia)[0])
# mean,std = round(np.mean(ks),4),round(np.std(ks),4)
# ax1.text(0.65, 0.32, r'r = %0.3f $\pm$ %0.3f' % (mean, std) , ha='center', va='center',transform = ax1.transAxes,size=10,color='k')
# plt.tight_layout()
# plt.savefig('results/pictures/prob_sonnia_200000.jpg',dpi=200)

# #tcrvae
# ks = []
# d_vae = pd.read_csv('results/probs/pdf_test_tcrvae_20k_0.csv')
# count,p_tcrvae = d_vae['count'].values,d_vae['p_tcrvae'].values
# p_tcrvae += 1e-25 #to avoid 0
# p_data_tcrvae,p_tcrvae = count / np.sum(count), p_tcrvae/np.sum(p_tcrvae)
# print(kl_divergence(p_data_tcrvae,p_tcrvae))
# ks.append(pr(p_data_tcrvae,p_tcrvae)[0])
# print(pr(p_data_tcrvae,p_tcrvae)[0])
# fig=plt.figure(figsize=(5,3),dpi=200)
# ax1=plt.subplot(111)
# ax1.set_ylim([-21,0])
# ax1.set_xlim([-5.5,-2.5])
# ax1.locator_params(nbins=4)
# ax1.plot([-5.5, -2.5], [-5.5, -2.5], color='k', linestyle='-', linewidth=2)
# ax1.set_xlabel(r'$log_{10}P_{data}$')
# ax1.set_ylabel(r'$log_{10}P_{infer}$')
# Plot.density_scatter(np.log10(p_data_tcrvae),np.log10(p_tcrvae),bins = [10,50],ax=ax1,method='TCRvae')
# for i in range(4):
#     d_vae = pd.read_csv('results/probs/pdf_test_tcrvae_{}.csv'.format(i+1))
#     count,p_tcrvae = d_vae['count'].values,d_vae['p_tcrvae'].values
#     p_tcrvae += 1e-25 #to avoid 0
#     p_data_tcrvae,p_tcrvae = count / np.sum(count), p_tcrvae/np.sum(p_tcrvae)
#     ks.append(pr(p_data_tcrvae,p_tcrvae)[0])
# mean,std = round(np.mean(ks),4),round(np.std(ks),4)
# ax1.text(0.65, 0.32, r'r = %0.3f $\pm$ %0.3f' % (mean, std) , ha='center', va='center',transform = ax1.transAxes,size=10,color='k')
# plt.tight_layout()
# plt.savefig('results/pictures/prob_tcrvae_200000.jpg',dpi=200)