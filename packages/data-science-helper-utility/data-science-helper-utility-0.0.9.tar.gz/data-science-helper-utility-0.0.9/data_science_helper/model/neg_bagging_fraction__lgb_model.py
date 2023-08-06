# -*- coding: utf-8 -*-
from data_science_helper import helper_general as hg

#import core_helper.helper_general as hg
#hg.set_base_path()
#import lgb_model as l
#import src.Prj_Core.core_helper.model.lgb_model as l
from data_science_helper.model import lgb_model as l

#import general as g
#import src.Prj_Core.core_helper.model.general as g
from data_science_helper.model import general as g

import time
#import core_helper.helper_plot as  hp
from data_science_helper import helper_plot as hp

def get_neg_bagging_fraction_params(y_train,params):
    
    N_p = y_train[y_train==1].count()
    N_n = y_train[y_train==0].count()
    #T_minimo= 43000
    T_minimo = get_Total_min_to_train(N_p)
    print("T_minimo : ",T_minimo)
    print("N_p : ",N_p)
    print("N_n : ",N_n)
    
    alpha = (T_minimo-N_p)/N_n
    if params is None:
        params = l.get_default_params()
        
    params['pos_bagging_fraction'] = 1
    params['neg_bagging_fraction'] = alpha
    params['scale_pos_weight'] = (alpha*N_n)/N_p
    return params


def modelar(X_train=None,y_train=None,X_test=None,y_test=None,params=None,metric='average_precision',api="train_api",url=None):
    start = time.time()
    model = None
    params = get_neg_bagging_fraction_params(y_train,params)
    
    if api=="train_api":
        params.update({"metric":metric})
        model = l.lgb_model_train(X_train,y_train,X_test,y_test,params=params)
        y_prob_uno = model.predict(X_test, num_iteration=model.best_iteration) 
        
    elif api=="skl_api":
        model = l.lgb_model_skl(X_train,y_train,X_test,y_test,params=params,metric=metric)        
        predicted_probas = model.predict_proba(X_test) 
        y_prob_uno = predicted_probas[:,1]
        
    if url is not None:
        g.save_model(model,url)
        g.save_json(params,url+"/params.json")
    
    
    if model is None:
        raise Exception("Modelo no implementado")
    
    return model , y_prob_uno 



def modelar_rscv(X_train,y_train=None,X_test=None,y_test=None,score_rs=None,params=None,param_dist=None, n_iter=None,n_jobs=None,url=None):
    start = time.time()
    
    params = get_neg_bagging_fraction_params(y_train,params)  

    results, model , best_params = l.lgb_model_rscv(X_train,y_train,X_test,y_test,score_rs,params,param_dist, n_iter,n_jobs)
    g.save_model(model,url)
    results.to_excel(url+"/rscv_iteraciones.xlsx")    
    predicted_probas = model.predict_proba(X_test) 

    return  results, model , predicted_probas, params, best_params




def get_Total_min_to_train(N_p):
    T_minimo = 10000 
    
    while N_p>=T_minimo:
      T_minimo = T_minimo + 30000

    return T_minimo
    
