# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 00:44:58 2022

@author: User
"""

from sklearn.datasets import make_classification
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
from data_science_helper.model import neg_bagging_fraction__lgb_model as nbf_lgb_model
from data_science_helper import helper_classification_model as hcm
from data_science_helper import helper_general as hg
import lightgbm as lgb 
import scikitplot as skplt
import matplotlib.pyplot as plt

#REVIASR !!!
#https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8017582

weights = [0.98]
features, output = make_classification(n_samples=30000, n_features=10, n_classes=2, random_state=123,weights=weights)


X = pd.DataFrame(features, columns=["F1", "F2", "F3", "F4", "F5","F6", "F7", "F8", "F9", "F10"])

y = pd.Series(output)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

y.value_counts()


#X_train,y_train=None,X_test=None,y_test=None,params=None,metric='average_precision',api="train",url=None





paerams_modelar = {'X_train':X_train, 'y_train': y_train, 'X_test': X_test, 'y_test': y_test, 
                   'params':None, "metric":'average_precision',"api":"train_api" , "url":None 
                   }

mod , predicted_probas   = nbf_lgb_model.modelar(**paerams_modelar)


path = hg.get_base_path()+"/test/modelo"

paerams_modelar_kcm = {"strategy":"neg_bagging_fraction__lgb_model",
                       "print_consola":True,
                       'X_train':X_train, 'y_train': y_train, 'X_test': X_test, 'y_test': y_test, 
                       'params':None, "metric":'average_precision',"api":"train_api" , "url":path 
                   }


model , predicted_probas  , KPIs = hcm.modelar_clasificacion_binaria(**paerams_modelar_kcm)


predicted_probas_neg = 1-predicted_probas
 
combined = np.vstack((predicted_probas_neg,predicted_probas )).T

    

#skplt.metrics.plot_roc(y_test, y_probs,classes_to_plot=[1])    
skplt.metrics.plot_roc(y_test, combined,classes_to_plot=[1],plot_micro=False,plot_macro=False)            
plt.show()


indices_to_plot = np.in1d([0,1], [1])
for i, to_plot in enumerate(indices_to_plot):
    print(to_plot)
    
    
predicted_probas


type(model)

type(model)==lgb.basic.Booster

lgb.create_tree_digraph(model, tree_index=0)


df_model = model.trees_to_dataframe()
