from tcrpeg.TCRpeg import TCRpeg
from tcrpeg.classification import classification
import pandas as pd
import numpy as np
import os
from sklearn.metrics import roc_auc_score

# data = pd.read_csv('../../nlp_vae/data/sub_tasks/caTCR/whole_seqs_train_caTCR.txt',names=['seq'])['seq'].values
# t_model = TCRpeg(hidden_size=512,num_layers = 3,load_data=True,embedding_path='data/embedding_32.txt',path_train=data,dropout=0.1)
# t_model.create_model()
# t_model.train_tcrpeg(40,16,5e-4,info='512_3l_40e_5e-4_16b_whole_train_caTCR',record_dir='results/caTCR')
t_model = TCRpeg(hidden_size=512,num_layers = 3,load_data=False,embedding_path='data/embedding_32.txt',dropout=0.1)
t_model.create_model(load=True,path='results/caTCR/23:02:07/model.pth')

for iteration in range(5):
    tcrpeg_c = classification(t_model,512*3,dropout=0.2,model_size='large')
    tumor_train = pd.read_csv('data/classification/tumor_train_caTCR.txt',names=['seq'])['seq'].values
    tumor_test = pd.read_csv('data/classification/tumor_test_caTCR.txt',names=['seq'])['seq'].values
    normal_train = pd.read_csv('data/classification/normal_train_caTCR.txt',names=['seq'])['seq'].values
    normal_test = pd.read_csv('data/classification/normal_test_caTCR.txt',names=['seq'])['seq'].values
    x_train = list(tumor_train) + list(normal_train)
    y_train = [1]*len(tumor_train) + [0] * len(normal_train)
    x_test = list(tumor_test) + list(normal_test)
    y_test = [1] * len(tumor_test) + [0]*len(normal_test)
    tcrpeg_c.train(x_train,y_train,30,8,1e-3,val_split=0,save_name='caTCR/caTCR_large_{}'.format(str(iteration)))
    auc,aup,y_pres,y_trues = tcrpeg_c.evaluate(x_test,y_test,100,record_path='results/caTCR_large_2.txt')
    with open('results/caTCR/predictions/pres_large_2_{}.txt'.format(str(iteration)),'w') as f:
        for i in range(len(y_pres)):
            f.write(str(y_pres[i])+','+str(y_trues[i]) + '\n')
    _,_,y_pres,y_trues = tcrpeg_c.evaluate(x_train,y_train,100,record_path='results/caTCR_large_test_2.txt')
# for iteration in range(5):
#     tcrpeg_c = classification(t_model,512*3,dropout=0.2,model_size='medium')
#     tumor_train = pd.read_csv('data/classification/tumor_train_caTCR.txt',names=['seq'])['seq'].values
#     tumor_test = pd.read_csv('data/classification/tumor_test_caTCR.txt',names=['seq'])['seq'].values
#     normal_train = pd.read_csv('data/classification/normal_train_caTCR.txt',names=['seq'])['seq'].values
#     normal_test = pd.read_csv('data/classification/normal_test_caTCR.txt',names=['seq'])['seq'].values
#     x_train = list(tumor_train) + list(normal_train)
#     y_train = [1]*len(tumor_train) + [0] * len(normal_train)
#     x_test = list(tumor_test) + list(normal_test)
#     y_test = [1] * len(tumor_test) + [0]*len(normal_test)
#     tcrpeg_c.train(x_train,y_train,30,8,1e-3,save_name='caTCR/caTCR_{}'.format(str(iteration)))
#     auc,aup,y_pres,y_trues = tcrpeg_c.evaluate(x_test,y_test,100,record_path='results/caTCR_testing.txt')
#     with open('results/caTCR/predictions/pres_{}.txt'.format(str(iteration)),'w') as f:
#         for i in range(len(y_pres)):
#             f.write(str(y_pres[i])+','+str(y_trues[i]) + '\n')

