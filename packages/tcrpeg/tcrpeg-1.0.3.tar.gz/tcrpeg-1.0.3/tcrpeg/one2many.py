from tcrpeg.TCRpeg import TCRpeg
from tcrpeg.classification import classification
import pandas as pd
import numpy as np
import os
from sklearn.metrics import roc_auc_score
from sklearn.metrics import average_precision_score as AUPRC


# g_model = TCRpeg(hidden_size=128,num_layers = 3,load_data=False,embedding_path='data/embedding_32.txt',dropout=0.1)
# g_model.create_model(load=True,path='results/aug/14:32:04/model.pth')
# for num_gens in [2000,6000,10000,14000,18000,25000,30000]:
#     gens = g_model.generate_tcrpeg(num_gens,1000)
#     gens = [x for x in gens if classification.valid_seq(x)]

#     tumor_train = pd.read_csv('data/classification/tumor_train_caTCR.txt',names=['seq'])['seq'].values
#     tumor_test = pd.read_csv('data/classification/tumor_test_caTCR.txt',names=['seq'])['seq'].values
#     normal_train = pd.read_csv('data/classification/normal_train_caTCR.txt',names=['seq'])['seq'].values
#     normal_test = pd.read_csv('data/classification/normal_test_caTCR.txt',names=['seq'])['seq'].values
#     xtrain,ytrain = list(tumor_train)+list(normal_train), [1]*len(tumor_train) + [0] * len(normal_train)
#     xtest,ytest = list(tumor_test)+list(normal_test), [1]*len(tumor_test) + [0] * len(normal_test)
#     xtrain  = xtrain + list(gens)
#     ytrain = ytrain + [1] * len(gens)

#     t_model = TCRpeg(hidden_size=128,num_layers = 3,load_data=False,embedding_path='data/embedding_32.txt')
#     t_model.create_m2oModel()
#     t_model.train_many2one(xtrain,ytrain,25, 8, 1e-3, info=None, model_name=None,record_dir=None)
#     y_pres_whole,ytest = t_model.evaluate_many2one(xtest,ytest,100)
#     print(num_gens)
#     print(roc_auc_score(ytest,y_pres_whole))



np.random.seed(0)
time=0
data = pd.read_csv('../../nlp_vae/data/sars2/cdrs.csv')
cdrs = data['seq'].values
np.random.shuffle(cdrs)
# train = np.array(cdrs[:700])
# test = np.array(cdrs[700:])
test = np.array(cdrs[time*137:(time+1)*137])
train = np.array(list(set(list(cdrs)) - set(list(test))))
data_control = pd.read_csv('../../nlp_vae/data/sars2/control.csv')
cdrs_control = data_control['seq'].values
np.random.shuffle(cdrs_control)
# train_control = cdrs_control[:7000]
# test_control = cdrs_control[7000:]
test_control = np.array(cdrs_control[time*1370:(time+1)*1370])
train_control = np.array(list(set(list(cdrs_control)) - set(list(test_control))))
#train_whole = list(cdrs) + list(cdrs_control)
train_whole = list(train) + list(train_control)
test_whole = list(test) + list(test_control)

t_model = TCRpeg(hidden_size=32,num_layers = 3,load_data=False,embedding_path='data/embedding_32.txt',dropout=0.4)
t_model.create_m2oModel()
t_model.train_many2one(train_whole,[1]*len(train) + [0] * len(train_control),20, 8, 1e-3, info=None, model_name=None,record_dir=None)
y_pres_whole,ytest = t_model.evaluate_many2one(test_whole,[1] * len(test) + [0] * len(test_control),10)
print(roc_auc_score(ytest,y_pres_whole))
print(AUPRC(ytest,y_pres_whole))