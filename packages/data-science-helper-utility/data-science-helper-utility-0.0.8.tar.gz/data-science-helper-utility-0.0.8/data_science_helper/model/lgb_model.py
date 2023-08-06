# -*- coding: utf-8 -*-

#import core_helper.helper_general as hg
#hg.set_base_path()

from data_science_helper import helper_general as hg

import lightgbm as lgb 
from scipy.stats import uniform as sp_uniform
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV

#import general as g
#import core_helper.model.general as g
#import src.Prj_Core.core_helper.model.general as g
from data_science_helper.model import general as g

def get_pipeline():
    '''
    lgb_pipe = pipeline.Pipeline([
        #
        #  metric="None", first_metric_only=True -> ignora binary_logloss en early_stopping_rounds
        ('clf', lgb.LGBMClassifier(metric="None", first_metric_only=True, importance_type="gain",n_jobs=4))
        ])        

    '''
    lgb_pipe = lgb.LGBMClassifier(metric="None", 
                                  first_metric_only=True, 
                                  importance_type="gain",
                                  use_missing=True,
                                  zero_as_missing=False,
                                  n_jobs=4)
    return lgb_pipe




def get_possible_params():
     
    lgb_param_random = {
        'num_leaves':list(range(7, 50)),
        'feature_fraction':sp_uniform(loc=0.2, scale=0.8),
        'bagging_fraction':sp_uniform(loc=0.2, scale=0.8),   
        'learning_rate': [0.1,0.07,0.05,0.025,0.015,0.01,0.0085,0.007,0.005],
        'max_depth': [-1,1,3,5,10,15],              
    }

    return  lgb_param_random


def get_default_params():
    params = {}    
    params['metric']="None" 
    params['first_metric_only']=True 
    params['importance_type']="gain"
    params['use_missing']=True 
    params['zero_as_missing']=False 
    params['n_jobs']=4
    params['random_state']=1
    params['num_leaves']=15 
    params['feature_fraction']=0.7
    params['bagging_fraction']=0.7
    params['n_estimators']=10000 # optimizacion automatica con : early stopping
    params['objective']="binary" 
    params['bagging_freq']=1
    params['boosting_type']='gbdt'
    params['reg_alpha']=0
    params['reg_lambda']=0
        
    return params


def lgb_model(X_train,y_train,X_test,y_test,score_rs='average_precision',params=None):

    fn_eval = g.get_fn_eval(score_rs)
    fit_params = get_fit_params(X_train,y_train,X_test,y_test,fn_eval)
  
                       
    model = lgb.LGBMClassifier(**params)
    print('---------- definicion del modelo ----------------')
    print(model)
    print('-------------------------------------------------')
    
    model.fit(X_train,y_train,**fit_params)
   
    return model


def lgb_model_rscv(X_train, y_train, X_test, y_test,score_rs='average_precision', params=None, param_dist=None,n_iter=None,n_jobs = None):
    
    print("++++++++++++++++++++++++ INICIO - ESTIMAR MODELO ++++++++++++++++++++++++")   
    fn_eval = g.get_fn_eval(score_rs)
    fit_params = get_fit_params(X_train,y_train,X_test,y_test,fn_eval)          

    cv_ = g.get_kfold()          
    model = lgb.LGBMClassifier(**params)       
    print("------------------  n_jobs= ",n_jobs," -------------------")    
    print('------------------------ params -------------')
    print(params)
    print('------------------------------------------------')
    
    print('RandomizedSearchCV -> Multiples Hyperparametros')
    grid_obj = RandomizedSearchCV(estimator=model,
                                  param_distributions=param_dist,
                                  cv=cv_,
                                  n_iter=n_iter,
                                  refit=False,
                                  return_train_score=False,
                                  scoring = score_rs,
                                  n_jobs = n_jobs,
                                  verbose= True,          
                                  random_state=375)

    print('------------X_train-------------')
    print(X_train.shape)
    print(y_train.value_counts())
    print('---------------------------------')
    grid_obj.fit(X_train, y_train,**fit_params)

    #estimator = grid_obj.best_estimator_
    
    estimator = lgb.LGBMClassifier(**params)
    estimator.set_params(**grid_obj.best_params_) 
    estimator.fit(X_train,y_train,**fit_params)
    
    results = pd.DataFrame(grid_obj.cv_results_)
    best_params = grid_obj.best_params_  
    
    print('------------mejores hyperparametros-------------')
    print(best_params)
    print('------------------------------------------------')
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++") 
    return results, estimator , best_params

def get_fit_params(X_train,y_train,X_test, y_test,fn_eval):
 
    fit_params={"early_stopping_rounds":800, 
                "eval_metric" : fn_eval, 
                "eval_set" : [(X_train,y_train),(X_test,y_test)],
                'eval_names': ['train','test'],
                #"eval_set" : [(X_train,y_train)],
                #'eval_names': ['train'],               
                'verbose': 200,
                'feature_name': 'auto', # that's actually the default
                'categorical_feature': 'auto' # that's actually the default
               }    
    return fit_params