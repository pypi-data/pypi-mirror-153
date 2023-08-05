from tcrpeg.TCRpeg import TCRpeg
from tcrpeg.classification import classification
import pandas as pd
import numpy as np
import os
import argparse
from sklearn.model_selection import KFold
parser = argparse.ArgumentParser(description='')
parser.add_argument('--n',type=int,help='index of restart')
args = parser.parse_args()
#this is for tcrpeg

##train a model on positive data
# data = pd.read_csv('../../nlp_vae/data/sub_tasks/caTCR/normal_train_12_16.txt',names=['seq'])['seq'].values
# t_model = TCRpeg(hidden_size=128,num_layers = 3,load_data=True,embedding_path='data/embedding_32.txt',path_train=data,dropout=0.1)
# t_model.create_model()
# t_model.train_tcrpeg(40,16,5e-4,info='128_3l_40e_5e-4_16b_normal_train',record_dir='results/aug')

# t_model = TCRpeg(hidden_size=128,num_layers = 3,load_data=False,embedding_path='data/embedding_32.txt',dropout=0.1)
# t_model.create_model(load=True,path='results/aug/14:32:04/model.pth')
#num_aug = [10000,20000,30000,40000,50000,75000,100000]
num_aug = [45000,50000]
#num_aug = [8000,10000,15000,20000]
#num_aug = [n*2 for n in num_aug]
#num_aug = [12000]
# e_model = TCRpeg(hidden_size=512,num_layers = 3,load_data=False,embedding_path='data/embedding_32.txt',dropout=0.1)
# e_model.create_model(load=True,path='results/caTCR/23:02:07/model.pth')
tumor_train = pd.read_csv('data/classification/tumor_train_caTCR.txt',names=['seq'])['seq'].values
tumor_test = pd.read_csv('data/classification/tumor_test_caTCR.txt',names=['seq'])['seq'].values
tumor_whole = list(tumor_train) + list(tumor_test)
normal_train = pd.read_csv('data/classification/normal_train_caTCR.txt',names=['seq'])['seq'].values
normal_test = pd.read_csv('data/classification/normal_test_caTCR.txt',names=['seq'])['seq'].values
normal_whole = list(normal_train) + list(normal_test)
whole = list(tumor_whole) + list(normal_whole)
y_whole = [1] * len(tumor_whole) + [0] * len(normal_whole)
kf = KFold(n_splits=5,random_state=0,shuffle=True)
xx = list(range(len(whole)))
whole,y_whole = np.array(whole),np.array(y_whole)
kkk = 0
for train_idx,test_idx in kf.split(xx):
    x_train,x_test = whole[train_idx], whole[test_idx]
    y_train,y_test = y_whole[train_idx], y_whole[test_idx]
    tumor_train_idx,normal_train_idx = [k for k in range(len(y_train)) if y_train[k]==1],[k for k in range(len(y_train)) if y_train[k]==0]
    tumor_train,normal_train = x_train[tumor_train_idx],x_train[normal_train_idx]
    t_model = TCRpeg(hidden_size=128,num_layers = 3,load_data=True,embedding_path='data/embedding_32.txt',path_train=tumor_train,dropout=0.1)
    t_model.create_model()
    t_model.train_tcrpeg(40,16,5e-4)
    t_model2 = TCRpeg(hidden_size=128,num_layers = 3,load_data=True,embedding_path='data/embedding_32.txt',path_train=normal_train,dropout=0.1)
    t_model2.create_model()
    t_model2.train_tcrpeg(40,16,5e-4)
    #used the former 0.6 in augmentation
    for num_gens in num_aug:
        gens = t_model.generate_tcrpeg(num_gens,1000)
        gens = [x for x in gens if classification.valid_seq(x)]
        gens2 = t_model2.generate_tcrpeg(num_gens,1000)
        gens2 = [x for x in gens2 if classification.valid_seq(x)]
        prob_a = t_model.sampling_tcrpeg_batch(gens,2000)
        sorted_index = np.argsort(-prob_a)
        a_list_sorted = np.array(gens)[sorted_index]
        gens = a_list_sorted[int(len(a_list_sorted) * 0.6):]

        prob_a2 = t_model2.sampling_tcrpeg_batch(gens2,2000)
        sorted_index2 = np.argsort(-prob_a2)
        a_list_sorted2 = np.array(gens2)[sorted_index2]
        gens2 = a_list_sorted2[int(len(a_list_sorted2) * 0.6):]

        x_train  = list(x_train) + list(gens) + list(gens2)
        y_train = list(y_train) + [1] * len(gens) + [0] * len(gens2)

        # x_test = list(tumor_test) + list(normal_test)
        # y_test = [1] * len(tumor_test) + [0]*len(normal_test)
        e_model = TCRpeg(hidden_size=512,num_layers = 3,load_data=True,embedding_path='data/embedding_32.txt',path_train=x_train,dropout=0.1)
        e_model.create_model()
        e_model.train_tcrpeg(40,16,5e-4,info='128_3l_40e_5e-4_16b_tumor_train_aug')
        tcrpeg_c = classification(e_model,512*3,dropout=0.2,model_size='large')
        epoch = 30 
        # tcrpeg_c.train(x_train,y_train,epoch,8,1e-3,val_split=0,save_name='aug/caTCR_large_{}'.format(str(num_gens)))
        tcrpeg_c.train(x_train,y_train,epoch,8,1e-3,val_split=0)
        
        auc,aup,y_pres,y_trues = tcrpeg_c.evaluate(x_test,y_test,100,record_path='results/aug2/aug_cross_last_{}.txt'.format(num_gens))
        with open('results/aug2/predictions/{}_pres_large_cross_last_{}.txt'.format(str(kkk),str(num_gens)),'w') as f:
            for i in range(len(y_pres)):
                f.write(str(y_pres[i])+','+str(y_trues[i]) + '\n')
    kkk += 1

# from tcrpeg.TCRpeg import TCRpeg
# from tcrpeg.classification import classification
# import pandas as pd
# import numpy as np
# import os
# import argparse
# from sklearn.model_selection import KFold
# parser = argparse.ArgumentParser(description='')
# parser.add_argument('--n',type=int,help='index of restart')
# args = parser.parse_args()
# #this is for tcrpeg

# ##train a model on positive data
# # data = pd.read_csv('../../nlp_vae/data/sub_tasks/caTCR/normal_train_12_16.txt',names=['seq'])['seq'].values
# # t_model = TCRpeg(hidden_size=128,num_layers = 3,load_data=True,embedding_path='data/embedding_32.txt',path_train=data,dropout=0.1)
# # t_model.create_model()
# # t_model.train_tcrpeg(40,16,5e-4,info='128_3l_40e_5e-4_16b_normal_train',record_dir='results/aug')

# # t_model = TCRpeg(hidden_size=128,num_layers = 3,load_data=False,embedding_path='data/embedding_32.txt',dropout=0.1)
# # t_model.create_model(load=True,path='results/aug/14:32:04/model.pth')
# #num_aug = [10000,20000,30000,40000,50000,75000,100000]
# num_aug = [2000,4000,6000,8000,10000,15000,20000]
# #num_aug = [12000]
# # e_model = TCRpeg(hidden_size=512,num_layers = 3,load_data=False,embedding_path='data/embedding_32.txt',dropout=0.1)
# # e_model.create_model(load=True,path='results/caTCR/23:02:07/model.pth')
# tumor_train = pd.read_csv('data/classification/tumor_train_caTCR.txt',names=['seq'])['seq'].values
# tumor_test = pd.read_csv('data/classification/tumor_test_caTCR.txt',names=['seq'])['seq'].values
# tumor_whole = list(tumor_train) + list(tumor_test)
# normal_train = pd.read_csv('data/classification/normal_train_caTCR.txt',names=['seq'])['seq'].values
# normal_test = pd.read_csv('data/classification/normal_test_caTCR.txt',names=['seq'])['seq'].values
# normal_whole = list(normal_train) + list(normal_test)
# whole = list(tumor_whole) + list(normal_whole)
# y_whole = [1] * len(tumor_whole) + [0] * len(normal_whole)
# kf = KFold(n_splits=5,random_state=0,shuffle=True)
# xx = list(range(len(whole)))
# whole,y_whole = np.array(whole),np.array(y_whole)
# kkk = 0
# for train_idx,test_idx in kf.split(xx):
#     if kkk >=3:
#         break
#     x_train,x_test = whole[train_idx], whole[test_idx]
#     y_train,y_test = y_whole[train_idx], y_whole[test_idx]
#     tumor_train_idx,normal_train_idx = [k for k in range(len(y_train)) if y_train[k]==1],[k for k in range(len(y_train)) if y_train[k]==0]
#     tumor_train,normal_train = x_train[tumor_train_idx],x_train[normal_train_idx]
#     t_model = TCRpeg(hidden_size=128,num_layers = 3,load_data=True,embedding_path='data/embedding_32.txt',path_train=tumor_train,dropout=0.1)
#     t_model.create_model()
#     t_model.train_tcrpeg(40,16,5e-4)
#     t_model2 = TCRpeg(hidden_size=128,num_layers = 3,load_data=True,embedding_path='data/embedding_32.txt',path_train=normal_train,dropout=0.1)
#     t_model2.create_model()
#     t_model2.train_tcrpeg(40,16,5e-4)
#     for num_gens in num_aug:
#         gens = t_model.generate_tcrpeg(num_gens,1000)
#         gens = [x for x in gens if classification.valid_seq(x)]
#         #gens = gens[:(len(gens)//500)*500]
#         # prob_a = t_model.sampling_tcrpeg_batch(gens,2000)
#         # sorted_index = np.argsort(-prob_a)
#         # a_list_sorted = np.array(gens)[sorted_index]
#         # gens = a_list_sorted[:int(len(a_list_sorted) * 0.2)]
#         gens2 = t_model2.generate_tcrpeg(num_gens,1000)
#         gens2 = [x for x in gens2 if classification.valid_seq(x)]

#         x_train  = list(x_train) + list(gens) + list(gens2)
#         y_train = list(y_train) + [1] * len(gens) + [0] * len(gens2)

#         # x_test = list(tumor_test) + list(normal_test)
#         # y_test = [1] * len(tumor_test) + [0]*len(normal_test)
#         e_model = TCRpeg(hidden_size=512,num_layers = 3,load_data=True,embedding_path='data/embedding_32.txt',path_train=x_train,dropout=0.1)
#         e_model.create_model()
#         e_model.train_tcrpeg(40,16,5e-4,info='128_3l_40e_5e-4_16b_tumor_train_aug')
#         tcrpeg_c = classification(e_model,512*3,dropout=0.2,model_size='large')
#         epoch = 30 
#         # tcrpeg_c.train(x_train,y_train,epoch,8,1e-3,val_split=0,save_name='aug/caTCR_large_{}'.format(str(num_gens)))
#         tcrpeg_c.train(x_train,y_train,epoch,8,1e-3,val_split=0)
        
#         auc,aup,y_pres,y_trues = tcrpeg_c.evaluate(x_test,y_test,100,record_path='results/aug2/aug_cross_{}.txt'.format(num_gens))
#         with open('results/aug2/predictions/{}_pres_large_cross_{}.txt'.format(str(kkk),str(num_gens)),'w') as f:
#             for i in range(len(y_pres)):
#                 f.write(str(y_pres[i])+','+str(y_trues[i]) + '\n')
#     kkk += 1
