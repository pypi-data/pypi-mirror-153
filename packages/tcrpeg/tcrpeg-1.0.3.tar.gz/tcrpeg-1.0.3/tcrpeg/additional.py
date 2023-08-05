from tcrpeg.TCRpeg import TCRpeg
from tcrpeg.classification import classification
import pandas as pd
import numpy as np
import os
from tcrpeg.evaluate import evaluation
from tcrpeg.utils import plotting
from tcrpeg.word2vec import word2vec
from sklearn.model_selection import KFold as kfold

vs_default = ['TRBV10-1','TRBV10-2','TRBV10-3','TRBV11-1','TRBV11-2','TRBV11-3','TRBV12-3','TRBV12-5', 'TRBV13', 'TRBV14', 'TRBV15', 
        'TRBV16', 'TRBV18','TRBV19','TRBV2', 'TRBV20-1', 'TRBV25-1', 'TRBV27', 'TRBV28', 'TRBV29-1', 'TRBV3-1', 'TRBV30',
'TRBV4-1', 'TRBV4-2','TRBV4-3','TRBV6-3',
 'TRBV5-1', 'TRBV5-4', 'TRBV5-5', 'TRBV5-6', 'TRBV5-8','TRBV6-1', 'TRBV6-2','TRBV6-4', 'TRBV6-5','TRBV12-4', 'TRBV6-6','TRBV6-8','TRBV24-1', 'TRBV6-9', 'TRBV7-2', 'TRBV7-3',
  'TRBV7-4', 'TRBV7-6', 'TRBV7-7', 'TRBV7-8', 'TRBV7-9', 'TRBV9']
js_default = ['TRBJ1-1', 'TRBJ1-2', 'TRBJ1-3','TRBJ1-4', 'TRBJ1-5', 'TRBJ1-6','TRBJ2-1', 'TRBJ2-2', 'TRBJ2-3', 'TRBJ2-4', 'TRBJ2-5','TRBJ2-6', 'TRBJ2-7']
v,j = [x[4:] for x in vs_default],[x[4:] for x in js_default]

#get embeddings:
#np.random.seed(0)
# pos = list(pd.read_csv('data/classification/GILGFVFTL/positive.txt',names=['seq'])['seq'].values)
# con = list(pd.read_csv('data/classification/GILGFVFTL/control.txt',names=['seq'])['seq'].values)
whole = (pd.read_csv('data/classification/GLCTLVAML/N_whole.csv')[['CDR3_sequence','V_gene','J_gene']]).values
# whole = np.array(pos + con)
whole_y = np.array([1]* (len(whole)//2) + [0] * (len(whole)//2))
# model = TCRpeg(hidden_size=256,num_layers = 3,load_data=True,embedding_path='data/embedding_32.txt',path_train=whole)
# model.create_model()
# model.train_tcrpeg(epochs=30,batch_size=8,lr=1e-3)
# model.save('results/additional/G.pth')

# pos = list(pd.read_csv('data/classification/NLVPMVATV/positive.txt',names=['seq'])['seq'].values)
# con = list(pd.read_csv('data/classification/NLVPMVATV/control.txt',names=['seq'])['seq'].values)
# whole = pos + con
# model = TCRpeg(hidden_size=256,num_layers = 3,load_data=True,embedding_path='data/embedding_32.txt',path_train=whole)
# model.create_model()
# model.train_tcrpeg(epochs=30,batch_size=8,lr=1e-3)
# model.save('results/additional/N.pth')

kf = kfold(n_splits=5,random_state=0,shuffle=True)
index = 0
for train_idx,test_idx in kf.split(whole):
    test,test_y = whole[test_idx],whole_y[test_idx]
    test = np.array([x[0] for x in test])
    train,train_y = whole[train_idx],whole_y[train_idx]
    # t_model = TCRpeg(hidden_size=256,num_layers = 3,load_data=True,embedding_path='data/embedding_32.txt',path_train=train,vs_list=v,js_list=j,vj=True)
    # t_model.create_model(vj=True)
    # t_model.train_tcrpeg_vj(epochs=30,batch_size=8,lr=1e-3)
    # t_model.save('results/additional/models/N_vj_{}.pth'.format(index))
    #####
    train_pos = [train[i] for i in range(len(train)) if train_y[i] == 1]
    train_neg = [train[i] for i in range(len(train)) if train_y[i] == 0]
    model_pos = TCRpeg(hidden_size=256,num_layers = 3,load_data=True,embedding_path='data/embedding_32.txt',path_train=train_pos,vs_list=v,js_list=j,vj=True)
    model_pos.create_model(vj=True)
    model_pos.train_tcrpeg_vj(epochs=30,batch_size=8,lr=1e-3)
    model_pos.save('results/additional/models/N_pos_vj_{}.pth'.format(index))

    model_neg = TCRpeg(hidden_size=256,num_layers = 3,load_data=True,embedding_path='data/embedding_32.txt',path_train=train_neg,vs_list=v,js_list=j,vj=True)
    model_neg.create_model(vj=True)
    model_neg.train_tcrpeg_vj(epochs=30,batch_size=8,lr=1e-3)
    model_neg.save('results/additional/models/N_neg_vj_{}.pth'.format(index))

    # tcrpeg_c = classification(t_model,256*3,dropout=0.2,model_size='large')
    # tcrpeg_c.train([x[0] for x in train],train_y,25,8,1e-3,val_split=0,save_name=None)
    # auc,aup,y_pres,y_trues = tcrpeg_c.evaluate(test,test_y,100,record_path='results/additional/G_vj_{}.txt'.format(index))
    # with open('results/additional/predictions/pres_large_vj_{}.txt'.format(str(index)),'w') as f:
    #     for i in range(len(y_pres)):
    #         f.write(str(y_pres[i])+','+str(y_trues[i]) + '\n')
    # test_pos = [test[i] for i in range(len(test)) if test_y[i] == 1]
    # test_neg = [test[i] for i in range(len(test)) if test_y[i] == 0]
    # with open('data/classification/GILGFVFTL/deepcat/G_normal_train_{}.txt')

    index += 1


# ./tcrmatch -i data/gens_tcrvae/tcrvae_cdrs_20000.csvtrimmed.txt -t 2 -s 0.9 -d data/cdr3_trimmed.txt > result/tcrvae_20000.txt