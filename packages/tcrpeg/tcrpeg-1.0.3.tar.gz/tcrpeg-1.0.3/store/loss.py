from utils import *
import pandas as pd
import numpy as np
from collections import defaultdict
from matplotlib.lines import Line2D
from evaluate import evaluation
from tcrpeg.TCRpeg import TCRpeg
import os
from scipy.stats import pearsonr as pr

path = '../../nlp_vae/data/whole_seqs_train_nn_sonnia.tsv'
# data = pd.read_csv(path, sep="\t",nrows=int(5e6))['seq'].values
#data = pd.read_csv(path, sep="\t").sample(n=int(200000),random_state=0)
#seqs,vs,js = data['seq'].values,data['v'].values,data['j'].values
model = TCRpeg(hidden_size=64,num_layers = 3,load_data=False,embedding_path='data/embedding_32.txt')
#model.aas_seqs_train= seqs
#model.vs_train,model.js_train = model.gene2embs(vs,'v'),model.gene2embs(js,'j')
model.create_model(vj=True,load=True,path='results/models/15:15:18/model.pth')
#model.train_tcrpeg_vj(30,32,5e-4,info='64_3_30_32_5e-4_200000_vj',record_dir='results/models')
for i in range(5):
    model.generate_tcrpeg_vj(200000, 2000,record_path='../../test_projects/results/generation_vj/tcrpeg_200000_{}.txt'.format(str(i)))
