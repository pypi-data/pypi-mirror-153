# -*- coding: utf-8 -*-
"""
Created on Tue May 31 14:33:24 2022

@author: User
"""

import numpy as np
import pandas as pd
import optuna

import data_science_helper.helper_classification_model as hcm
import data_science_helper.model.neg_bagging_fraction__lgb_model as nbf_lgb_model


from sklearn.metrics import  roc_auc_score, average_precision_score 
from sklearn.model_selection import StratifiedKFold   
import lightgbm as lgb 

from optuna.trial import Trial
import gc
import warnings
warnings.filterwarnings("ignore")


from sklearn.model_selection import  StratifiedShuffleSplit
from sklearn.metrics import precision_recall_fscore_support

from lightgbm import early_stopping
from lightgbm import log_evaluation
import statistics

def objective_with_prune(trial: Trial, fast_check=True, X=None,y=None,list_kpi=[],log=0):
    folds = 5
    
    test_size = hcm.get_test_size(X)
    if test_size == 0.20:
        kf = StratifiedKFold(n_splits=folds, shuffle=True, random_state=1)
        print("StratifiedKFold")
    else:
        kf = StratifiedShuffleSplit(n_splits=folds, test_size=test_size, random_state=1)
        print("StratifiedShuffleSplit")
    
    X_train = X
    y_train = y    
    
    X_train.reset_index(inplace=True,drop=True)
    y_train.reset_index(inplace=True,drop=True)   
 
    gc.collect()
   
    models = []
    
    list_valid_score = []
    list_valid_score2 = []
    list_train_score = []
    
    list_valid_precision = []
    list_valid_recall = []
    list_valid_f1 = []
    list_valid_average_precision = []
    list_valid_roc_auc = []
    with_bias = False
    
    for train_idx, valid_idx in kf.split(X_train, y_train):
        train_data = X_train.iloc[train_idx,:], y_train[train_idx]
        valid_data = X_train.iloc[valid_idx,:], y_train[valid_idx]

        model, kpi = fit_lgbm_with_pruning(trial, train_data, valid_data,log=log)

        models.append(model)
        gc.collect()
        
        list_valid_precision.append(kpi["valid/precision"])
        list_valid_recall.append(kpi["valid/recall"])
        list_valid_f1.append(kpi["valid/f1"])
        list_valid_average_precision.append(kpi["valid/average_precision"])
        list_valid_roc_auc.append(kpi["valid/roc_auc"])        
        
        
        list_valid_score.append(kpi["valid/average_precision"])
        list_valid_score2.append(kpi["valid/average_precision2"])       
        
        list_train_score.append(kpi["train/average_precision"])
        
        bias = kpi["bias"]
        
        if (bias>0.15):
            with_bias = True
            break
        
        if fast_check:
            break
            
    mean_valid_score = statistics.mean(list_valid_score)
    mean_valid_score2 = statistics.mean(list_valid_score2)

    std_valid_score = statistics.pstdev(list_valid_score)
    
    mean_train_score = statistics.mean(list_train_score)
    std_train_score = statistics.pstdev(list_train_score)
             
    mean_valid_precision = statistics.mean(list_valid_precision)           
    std_valid_precision = statistics.pstdev(list_valid_precision)
    
    mean_valid_recall = statistics.mean(list_valid_recall)           
    std_valid_recall = statistics.pstdev(list_valid_recall)
    
    mean_valid_f1 = statistics.mean(list_valid_f1)           
    std_valid_f1 = statistics.pstdev(list_valid_f1)
    
    mean_valid_average_precision = statistics.mean(list_valid_average_precision) 

    std_valid_average_precision = statistics.pstdev(list_valid_average_precision)
    
    mean_valid_roc_auc = statistics.mean(list_valid_roc_auc)           
    std_valid_roc_auc = statistics.pstdev(list_valid_roc_auc)
       
    bias = abs(mean_train_score - mean_valid_score)
    
    result_iter = {
        'bias': bias,
        'overfitting':with_bias,
        'mean_train_score':mean_train_score,
        'std_train_score':std_valid_score,  
        
        'mean_valid_score':mean_valid_score,
        'mean_valid_score2':mean_valid_score2,
        'std_valid_score':std_train_score,       
          
    }   
    
    if(fast_check):
        split_dic = {}
        key_split = "split_{}".format(1)
        split_dic[key_split] = list_valid_score[0]
        result_iter.update(split_dic)
    else:
        for i in range(folds):
            split_train_dic = {}
            split_valid_dic = {}
            lb_fold = i+1
            
            key_split_train = "split_{}_train_score".format(lb_fold)
            split_train_dic[key_split_train] = list_train_score[i] if with_bias==False else -1
            result_iter.update(split_train_dic)
            
            key_split_valid = "split_{}_valid_score".format(lb_fold)          
            split_valid_dic[key_split_valid] = list_valid_score[i] if with_bias==False else -1
            result_iter.update(split_valid_dic)
        
        
    result_kpis = {   
        
        'mean_valid_precision':mean_valid_precision,
        'std_valid_precision':std_valid_precision,
        'mean_valid_recall':mean_valid_recall,
        'std_valid_recall':std_valid_recall, 
        'mean_valid_f1':mean_valid_f1,
        'std_valid_f1':std_valid_f1 ,
        'mean_valid_average_precision':mean_valid_average_precision,
        'std_valid_average_precision':std_valid_average_precision,       
        'mean_valid_roc_auc':mean_valid_roc_auc,
        'std_valid_roc_auc':std_valid_roc_auc       
    }
    
    result_iter.update(result_kpis)
  
    list_kpi.append(result_iter)
    return mean_valid_score

def fit_lgbm_with_pruning(trial, train, val, devices=(-1,),  cat_features=None, log=0):
    """Train Light GBM model"""    
    X_train, y_train = train
    X_valid, y_valid = val

        
    nb_f = nbf_lgb_model.get_neg_bagging_fraction_params(y_train,{})

    params = {

        "seed": 1,
        'objective': 'binary',       
        "learning_rate": trial.suggest_loguniform("learning_rate", 1e-3, 0.01),               
        "feature_fraction": trial.suggest_float("feature_fraction", 0.05, 0.99, step=0.05),        
        "num_leaves": trial.suggest_int("num_leaves", 31, 2000, step=10),      
        "bagging_fraction": trial.suggest_float("bagging_fraction", 0.05, 0.99, step=0.05),       
        "lambda_l1": trial.suggest_loguniform('lambda_l1', 1e-8, 10.0),
        "lambda_l2": trial.suggest_loguniform("lambda_l2", 1e-8, 10.0),
        "min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 20, 200, step=10),
        "max_depth": trial.suggest_int("max_depth", 3, 15),
        "min_gain_to_split": trial.suggest_float("min_gain_to_split", 0, 15), 
        "n_estimators":10000,        
        "metric": "average_precision",
    }
    
    params.update(nb_f)
        
    device = devices[0]
    if device == -1:
        # use cpu
        pass
    else:
        # use gpu
        print(f'using gpu device_id {device}...')
        params.update({'device': 'gpu', 'gpu_device_id': device})

    #params['seed'] = seed

    early_stop = 400


    d_train = lgb.Dataset(X_train, label=y_train, categorical_feature=cat_features)
    d_valid = lgb.Dataset(X_valid, label=y_valid, categorical_feature=cat_features)

    watchlist = [d_valid]    

    
    pruning_callback_v = optuna.integration.LightGBMPruningCallback(trial, "average_precision",
                                                                  valid_name="data_valid")
    
    model = lgb.train(params,                 
                      train_set=d_train,
                      valid_names = ['data_valid'],
                      valid_sets=watchlist,
                      callbacks=[log_evaluation(log),pruning_callback_v,early_stopping(early_stop)]
                     )

    # predictions
    
    y_pred_prob_train = model.predict(X_train, num_iteration=model.best_iteration)   
    y_pred_prob_valid = model.predict(X_valid, num_iteration=model.best_iteration)   
    
    y_pred_valid = np.rint(y_pred_prob_valid)
    
    train_average_precision = average_precision_score(y_train, y_pred_prob_train)
    
    valid_average_precision2 = model.best_score['data_valid']['average_precision']
    valid_average_precision = average_precision_score(y_valid, y_pred_prob_valid)
    
    precision, recall, f1, support = precision_recall_fscore_support(y_valid, y_pred_valid ,average="binary",pos_label=1)
    roc_auc = roc_auc_score(y_valid, y_pred_prob_valid) 
    

    bias = train_average_precision - valid_average_precision    
 
    kpi = {'train/average_precision': train_average_precision,           
           'valid/average_precision': valid_average_precision,
           'valid/average_precision2': valid_average_precision2,
           'valid/precision': precision,
           'valid/recall': recall,
           'valid/f1': f1,
           'valid/roc_auc': roc_auc,
           'bias':bias
          }
    return model, kpi


def lgb_model_optuna(X_train, y_train,n_trials=2,fast_check=True,score_rs='average_precision', params=None,n_jobs = 6,log=0):
    list_kpi_ = []
    sampler = optuna.samplers.RandomSampler(seed=10)
    pruner=optuna.pruners.MedianPruner(n_warmup_steps=5)
    study = optuna.create_study(pruner=pruner,sampler=sampler,direction="maximize")


    func = lambda trial: objective_with_prune(trial,fast_check=fast_check, X=X_train, y=y_train,list_kpi=list_kpi_,log=log)
    
    study.optimize(func, n_trials=n_trials, n_jobs=n_jobs)

    best_params = study.best_params
    result = pd.DataFrame(list_kpi_)
    
    
    trials_dataframe = study.trials_dataframe()

    return result, best_params, study.best_value , trials_dataframe



def get_best_value_nob(result_,nob_group="0.0-0.15"):
    #result_ = result.copy()
    labels = ["{0} - {1}".format(i, i + 0.1) for i in np.linspace(0,1,10,endpoint=True)] #, labels=labels
    labels = ["0.0-0.15","0.15-0.2","0.2-0.3","0.3-0.4","0.4-0.5","0.5-0.6","0.6-0.7","0.7-0.8","0.8-0.9","0.9-1.0"]
    intervalos = [0. , 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1. ]    
    result_["bias_group"] = pd.cut(result_.bias, intervalos, right=False, labels=labels)
    #result_["bias_group"] = pd.cut(result_.bias, np.linspace(0,1,11,endpoint=True), right=False, labels=labels)
    final_result = result_[(result_.bias_group==nob_group) & (result_.overfitting==False)].sort_values(by=['mean_valid_score'], ascending=False)
    best_value_nob = final_result['mean_valid_score'].iloc[0]
    return best_value_nob

def get_params_by_value(trials_dataframe_,best_value_nob):

    best_trial_nob = trials_dataframe_[trials_dataframe_.value==best_value_nob].copy()
    cls_to_delete = ["number","value","datetime_start","datetime_complete","duration","state"]
    best_trial_nob.drop(columns=cls_to_delete, inplace=True)

    best_trial_nob.columns = best_trial_nob.columns.str.replace('params_', '')
    best_params_nob = best_trial_nob.to_dict(orient='records')[0]

    return best_params_nob