# -*- coding: utf-8 -*-
#import core_helper.helper_general as hg
#hg.set_base_path()

from data_science_helper import helper_general as hg

#import general as g
#import src.Prj_Core.core_helper.model.general as g
from data_science_helper.model import general as g

#import lgb_model as l
#import src.Prj_Core.core_helper.model.lgb_model as l
from data_science_helper.model import lgb_model as l

import math
from imblearn.under_sampling import RandomUnderSampler
import numpy as np
import pandas as pd
#import core_helper.helper_plot as  hp
from data_science_helper import helper_plot as hp


#import src.Prj_Core.core_helper.model.general as g
import time

def modelar(X_train,y_train,X_test,y_test,url):
    start = time.time()
    list_m = custom_bagging_model(X_train,y_train,X_test,y_test,K=1) 
    g.save_model(list_m,url)
    y_pred,y_prob_uno , predicted_probas = predict_proba(list_m,X_test)
        
    #kpis = hp.print_kpis_rendimiento_modelo(y_test,predicted_probas,url)  
    #g.get_summary_evaluation2(X_test,predicted_probas,y_test,url)
    
    #y_pred_t,y_prob_uno_t , predicted_probas_t = cbm_predict(list_m,X_t)
    #y_pred_t_mas_1,y_prob_uno_t_mas_1 , predicted_probas_t_mas_1 = cbm_predict(list_m,X_t_mas_1)
    
    return list_m , predicted_probas

'''
def custom_bagging_pipeline_model(X_train,y_train,X_test,y_test,X_t,X_t_mas_1,url):
    start = time.time()
    list_m = custom_bagging_model(X_train,y_train,X_test,y_test,K=1) 
    y_pred,y_prob_uno , predicted_probas = predict_proba(list_m,X_test)
    
    
    kpis = hp.print_kpis_rendimiento_modelo(y_test,predicted_probas,url)  
    g.get_summary_evaluation2(X_test,predicted_probas,y_test,url)
    
    y_pred_t,y_prob_uno_t , predicted_probas_t = predict_proba(list_m,X_t)
    y_pred_t_mas_1,y_prob_uno_t_mas_1 , predicted_probas_t_mas_1 = predict_proba(list_m,X_t_mas_1)
    
    return kpis , predicted_probas , y_prob_uno_t, y_prob_uno_t_mas_1
'''


def predict_proba(list_model,X_test):
    list_y_prob = []
    for model in list_model:
        #y_pred = model.predict(X_test)
        predicted_probas = model.predict_proba(X_test)        
        list_y_prob.append(predicted_probas[:,1])
    y_prob_uno  = np.mean(list_y_prob, axis=0)
    y_prob_cero = [1-x for x in y_prob_uno]
    predicted_probas = np.vstack((y_prob_cero, y_prob_uno)).T
    y_pred = np.round(y_prob_uno, 0)
    return y_pred,y_prob_uno , predicted_probas
 


def custom_bagging_model(X_train,y_train,X_test,y_test,score_rs='average_precision',params=None,alpha=None, 
                         n_iter_rscv=None,K = 1):
    
    
    #MIN_N_TRAIN = 10000 #numero minimo de registros para que lgb no sobre ajuste

    N_p = y_train[y_train==1].count()
    N_n = y_train[y_train==0].count()
    
    MIN_N_TRAIN = get_Total_min_to_train(N_p)
    
    fn_eval = g.get_fn_eval(score_rs)
    fit_params = l.get_fit_params(X_train,y_train,X_test,y_test,fn_eval)
        
    alpha=(MIN_N_TRAIN-N_p)/(N_n) 
    N_n_res = int(round(alpha*N_n,0))
    
    list_model = []

    lambda_ = N_p/N_n

    T = int(round(math.log(0.05)/math.log(1-K*alpha)))
    T,K = get_T_reducido(K,alpha)
    print("T: ",T,"k:",K)

    for i in range(T):
        print("model :",i)

        rus = RandomUnderSampler(random_state=i,sampling_strategy={1:N_p ,0: N_n_res},replacement=False) #majority
        X_res, y_res = rus.fit_resample(X_train, y_train)
        print("total: ",len(y_res),", Class_1: ",y_res[y_res==1].count(),", Class_0: ",y_res[y_res==0].count())
       

        if n_iter_rscv is None:
            if params is None:
                params = l.get_default_params()   
                
            params['pos_bagging_fraction']=1
            params['neg_bagging_fraction']=1
            params['scale_pos_weight']=(K*alpha*N_n)/N_p
            
            model = l.lgb_model(X_res,y_res,X_test,y_test,score_rs=score_rs,params=params)  
        else:
            results, model = l.lgb_model_rscv(X_res, y_res, X_test, y_test,score_rs=score_rs, n_iter=n_iter_rscv)   

        list_model.append(model)
  
    return list_model



def get_Total_min_to_train(N_p):
    T_minimo = 10000 
    
    while N_p>=T_minimo:
      T_minimo = T_minimo + 30000

    return T_minimo



def get_T_reducido(K,alpha):
    T = get_T(K,alpha)   
    
    if(T>20):
        K = K +1
        T = get_T(K,alpha)
        
        if(T>20):
            K = K +1
            T = get_T(K,alpha)
            
            if(T>20):
                K = K +1
                T = get_T(K,alpha)
        
        return T, K 
    else:
        return T, K
    
    

def get_T(K,alpha):
    T = int(round(math.log(0.05)/math.log(1-K*alpha)))
    return T
