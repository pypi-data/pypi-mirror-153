from utils import *
import pandas as pd
import numpy as np
from collections import defaultdict
from matplotlib.lines import Line2D
from evaluate import evaluation
from tcrpeg.TCRpeg import TCRpeg
import os
from scipy.stats import pearsonr as pr

Plot = plotting()
# model = TCRpeg(hidden_size=64,num_layers = 3,load_data=False,embedding_path='data/embedding_32.txt')
# model.create_model(load=True,path='../../nlp_vae/results/models/11_22_2021/19:35:40/only_decoder_11_22_2021-19:35:40_40.pth')
# tcrpeg_path = '../../nlp_vae/results/models/12_20_2021/17:00:47/none_12_20_2021-17:00:47_20.pth'
# t_model = TCRpeg(hidden_size=256,num_layers = 3,load_data=False,embedding_path='data/embedding_32.txt',vj=True)
# t_model.create_model(load=True,vj=True,path=tcrpeg_path)

#eva = evaluation(model=model,frac=0.1)
def compute_ld(seqs):
    '''
    
    '''
    l1 = len(seqs)
    seqs = [s for s in seqs if Plot.valid_seq(s)]
    lens = [len(seq) for seq in seqs]
    len2count = defaultdict(int)
    print('diff:', l1 - len(seqs))
    for i in range(len(lens)):    
        len2count[lens[i]] += 1
    for key in len2count.keys():
        len2count[key] /= len(lens)
    return len2count

def compute_laa(seqs):
    aa2pos_dic = [defaultdict(int) for _ in range(20)]
    seqs = [s for s in seqs if Plot.valid_seq(s)]
    for i in range(len(seqs)):
        seq1 = seqs[i]
        for j,aa in enumerate(seq1):
            #if aa == 'e' or 
            aa2pos_dic[Plot.aa2idx[aa]][j+1] += 1 #remember to modify
    x_axis = list(range(1,31))
    for i in range(20):
        dic = aa2pos_dic[i]
        y = [dic[k] for k in x_axis]
        sum_ = sum(y)
        y_nor = [yy/sum_ for yy in y]
        #dic[i] = [yy/sum_ for yy in y]
        aa2pos_dic[i] = {x_axis[i]:y_nor[i] for i in range(len(x_axis))}
        # print(dic[i])
        # print(aa2pos_dic[i])
    
    return aa2pos_dic

def compute_v(vs):
    vs_dic = defaultdict(int)
    for i in range(len(vs)):
        vs_dic[vs[i]] += 1
    x_axis = Plot.vs
    y1 = [vs_dic[x]/len(vs) for x in x_axis]
    return {x_axis[i]:y1[i] for i in range(len(x_axis))}

def compute_j(js):
    vs_dic = defaultdict(int)
    for i in range(len(js)):
        vs_dic[js[i]] += 1
    x_axis = Plot.js
    
    y1 = [vs_dic[x]/len(js) for x in x_axis]
    
    
    return {x_axis[i]:y1[i] for i in range(len(x_axis))}

d = pd.read_csv('../../nlp_vae/data/whole_seqs_test_nn_sonnia.tsv',sep='\t')
#len2count_total = defaultdict(list)

ss,vs,js = d['seq'].values,d['v'].values,d['j'].values
v_dic_data = compute_v(vs)
j_dic_data = compute_j(js)

#record kl
kl_peg_aa,kl_sonnia_aa,kl_tcrvae_aa = [[]]*20,[[]]*20,[[]]*20
kl_peg_l,kl_sonnia_l,kl_tcrvae_l = [],[],[]
kl_peg_v,kl_sonnia_v,kl_tcrvae_v = [],[],[]
kl_peg_j,kl_sonnia_j,kl_tcrvae_j = [],[],[]

##length dis
total_lendis = dict()
total_aasdis = dict()
total_vsdis = dict()
total_jsdis = dict()

dirs_base = '../../test_projects/results/generation_vj/'
dirs = [dirs_base + x for x in os.listdir(dirs_base) if 'peg' in x and '200000' in x]
assert len(dirs) == 5
len2count_total = defaultdict(list)
aa2count_total = [defaultdict(list) for _ in range(20)]
v_total = defaultdict(list)
j_total = defaultdict(list)
for i in range(5):
    #data_path = '../../nlp_vae/results/gens/gens_200000/vae_200000.csv'
    data_path = dirs[i]
    print(data_path)
    d = pd.read_csv(data_path,names=['seqs','v','j'])
    ss,vs,js = d['seqs'].values,d['v'].values,d['j'].values
    len2count = compute_ld(ss)
    aa2pos_dic = compute_laa(ss)
    j_dic = compute_j(js)
    for key in j_dic.keys():
        j_total[key].append(j_dic[key])
    for a in range(20):
        aa2pos = aa2pos_dic[a]
        for key in aa2pos.keys():
            aa2count_total[a][key].append(aa2pos[key])
    v_dic = compute_v(vs)
    for key in v_dic.keys():
        v_total[key].append(v_dic[key])
    for l in range(2,31):
        len2count_total[l].append(len2count[l]) #to change
for i in range(20):
    aa2count = aa2count_total[i]
    for key in aa2count.keys():
        array = aa2count[key]
        aa2count[key] = (np.mean(array),np.std(array))

v_list = list(v_total.keys())
ks = []
for i in range(5):
    y1 = [v_dic_data[v] for v in v_list]
    y2 = [v_total[v][i] for v in v_list]
    # ks.append(kl_divergence(y1,y2,True))
    ks.append(pr(y1,y2)[0])
print(np.mean(ks))
print(np.std(ks))

j_list = list(j_total.keys())
ks = []
for i in range(5):
    y1 = [j_dic_data[v] for v in j_list]
    y2 = [j_total[v][i] for v in j_list]
    # ks.append(kl_divergence(y1,y2,True))
    ks.append(pr(y1,y2)[0])
print(np.mean(ks))
print(np.std(ks))

v_dis_input = ([np.mean(v_total[x]) for x in Plot.vs],[np.std(v_total[x]) for x in Plot.vs])
j_dis_input = ([np.mean(j_total[x]) for x in Plot.js],[np.std(j_total[x]) for x in Plot.js])
total_lendis['tcrpeg'] = len2count_total
total_aasdis['tcrpeg'] = aa2count_total
total_vsdis['tcrpeg'] = v_dis_input
total_jsdis['tcrpeg']= j_dis_input
###
dirs_base = '../../test_projects/results/generation_vj/'
dirs = [dirs_base + x for x in os.listdir(dirs_base) if 'sonnia' in x and '20000' in x]
assert len(dirs) == 5
len2count_total = defaultdict(list)
aa2count_total = [defaultdict(list) for _ in range(20)]
v_total = defaultdict(list)
j_total = defaultdict(list)
for i in range(5):
    #data_path = '../../nlp_vae/results/gens/gens_200000/vae_200000.csv'
    data_path = dirs[i]
    print(data_path)
    d = pd.read_csv(data_path,names=['seqs','v','j'])
    ss,vs,js = d['seqs'].values,d['v'].values,d['j'].values
    len2count = compute_ld(ss)
    aa2pos_dic = compute_laa(ss)
    v_dic = compute_v(vs)
    j_dic = compute_j(js)
    for key in j_dic.keys():
        j_total[key].append(j_dic[key])
    for key in v_dic.keys():
        v_total[key].append(v_dic[key])
    for a in range(20):
        aa2pos = aa2pos_dic[a]
        for key in aa2pos.keys():
            aa2count_total[a][key].append(aa2pos[key])
    for l in range(2,31):
        len2count_total[l].append(len2count[l]) #to change
for i in range(20):
    aa2count = aa2count_total[i]
    for key in aa2count.keys():
        array = aa2count[key]
        aa2count[key] = (np.mean(array),np.std(array))

v_list = list(v_total.keys())
ks = []
for i in range(5):
    y1 = [v_dic_data[v] for v in v_list]
    y2 = [v_total[v][i] for v in v_list]
    #ks.append(kl_divergence(y1,y2,True))
    ks.append(pr(y1,y2)[0])
print(np.mean(ks))
print(np.std(ks))

j_list = list(j_total.keys())
ks = []
for i in range(5):
    y1 = [j_dic_data[v] for v in j_list]
    y2 = [j_total[v][i] for v in j_list]
    #ks.append(kl_divergence(y1,y2,True))
    ks.append(pr(y1,y2)[0])
print(np.mean(ks))
print(np.std(ks))

v_dis_input = ([np.mean(v_total[x]) for x in Plot.vs],[np.std(v_total[x]) for x in Plot.vs])
j_dis_input = ([np.mean(j_total[x]) for x in Plot.js],[np.std(j_total[x]) for x in Plot.js])
total_lendis['sonnia'] = len2count_total
total_aasdis['sonnia'] = aa2count_total
total_vsdis['sonnia'] = v_dis_input
total_jsdis['sonnia'] = j_dis_input
###
dirs_base = '../../test_projects/results/generation_vj/'
dirs = [dirs_base + x for x in os.listdir(dirs_base) if 'vae' in x and '20k' in x]
assert len(dirs) == 5
len2count_total = defaultdict(list)
aa2count_total = [defaultdict(list) for _ in range(20)]
v_total = defaultdict(list)
j_total = defaultdict(list)
for i in range(5):
    #data_path = '../../nlp_vae/results/gens/gens_200000/vae_200000.csv'
    data_path = dirs[i]
    print(data_path)
    d = pd.read_csv(data_path)
    ss,vs,js = d['seqs'].values,d['v'].values,d['j'].values
    len2count = compute_ld(ss)
    aa2pos_dic = compute_laa(ss)
    v_dic = compute_v(vs)
    j_dic = compute_j(js)
    for key in j_dic.keys():
        j_total[key].append(j_dic[key])
    for key in v_dic.keys():
        v_total[key].append(v_dic[key])
    for a in range(20):
        aa2pos = aa2pos_dic[a]
        for key in aa2pos.keys():
            aa2count_total[a][key].append(aa2pos[key])
    for l in range(2,31):
        len2count_total[l].append(len2count[l]) #to change

v_list = list(v_total.keys())
ks = []
for i in range(5):
    y1 = [v_dic_data[v] for v in v_list]
    y2 = [v_total[v][i] for v in v_list]
    #ks.append(kl_divergence(y1,y2,True))
    ks.append(pr(y1,y2)[0])
print(np.mean(ks))
print(np.std(ks))

j_list = list(j_total.keys())
ks = []
for i in range(5):
    y1 = [j_dic_data[v] for v in j_list]
    y2 = [j_total[v][i] for v in j_list]
    #ks.append(kl_divergence(y1,y2,True))
    ks.append(pr(y1,y2)[0])
print(np.mean(ks))
print(np.std(ks))

v_dis_input = ([np.mean(v_total[x]) for x in Plot.vs],[np.std(v_total[x]) for x in Plot.vs])
j_dis_input = ([np.mean(j_total[x]) for x in Plot.js],[np.std(j_total[x]) for x in Plot.js])
for i in range(20):
    aa2count = aa2count_total[i]
    for key in aa2count.keys():
        array = aa2count[key]
        aa2count[key] = (np.mean(array),np.std(array))
total_lendis['tcrvae'] = len2count_total
total_aasdis['tcrvae'] = aa2count_total
total_vsdis['tcrvae'] = v_dis_input
total_jsdis['tcrvae'] = j_dis_input
###
d = pd.read_csv('../../nlp_vae/data/whole_seqs_test_nn_sonnia.tsv',sep='\t')
#len2count_total = defaultdict(list)

ss,vs,js = d['seq'].values,d['v'].values,d['j'].values
aa2pos_dic = compute_laa(ss)
len2count = compute_ld(ss)
v_dic = compute_v(vs)
j_dic = compute_j(js)
vs_ = [v_dic[x] for x in Plot.vs]
js_ = [j_dic[x] for x in Plot.js]
data_v = (vs_,vs_)
data_j = (js_,js_)
data = [len2count[l] for l in range(2,31)]

# #length
seqs1 = np.array([np.mean(total_lendis['tcrpeg'][i]) for i in range(2,31)])
errs1 = np.array([(np.std(total_lendis['tcrpeg'][i]) ) for i in range(2,31)])
seqs2 = np.array([np.mean(total_lendis['sonnia'][i]) for i in range(2,31)])
errs2 = np.array([(np.std(total_lendis['sonnia'][i]) ) for i in range(2,31)])
seqs3 = np.array([np.mean(total_lendis['tcrvae'][i]) for i in range(2,31)])
errs3 = np.array([(np.std(total_lendis['tcrvae'][i]) ) for i in range(2,31)])
Plot.length_dis(data,(seqs1,errs1),(seqs2,errs2),(seqs3,errs3),list(range(2,31)),fig_name='length_20k')

# #aas
# #print(total_aasdis['tcrpeg'])
# Plot.aas_dis(aa2pos_dic,total_aasdis['tcrpeg'],total_aasdis['sonnia'],total_aasdis['tcrvae'],'AAs_20k')


# # # #vs,js
#Plot.v_dis(data_v,total_vsdis['tcrpeg'],total_vsdis['sonnia'],total_vsdis['tcrvae'],'vs_20k_whole')
# Plot.j_dis(data_j,total_jsdis['tcrpeg'],total_jsdis['sonnia'],total_jsdis['tcrvae'],'js_20k')

# #prob plot
# _,_,p_data,p_tcrpeg = eva.eva_prob('../../nlp_vae/data/pdf_test_sonnia.csv')
# print('done calculating')

# fig=plt.figure(figsize=(6,4),dpi=200)
# ax1=plt.subplot(111)
# ax1.set_ylim([-8,-1])
# ax1.set_xlim([-4.8,-1.5])
# ax1.locator_params(nbins=4)
# Plot.density_scatter(np.log10(p_data),np.log10(p_tcrpeg),bins = [10,50],ax=ax1,fig_name='test_prob')













