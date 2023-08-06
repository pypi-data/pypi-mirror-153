# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 08:46:06 2021

@author: User
"""
import pandas as pd
import numpy as np
import data_science_helper.helper_output as ho

def drop_cls_unique_value(df):
    ho.print_message("drop_cls_unique_value: Eliminando columnas con un unico valor")
    l=[]
    for col in df.columns:
        if len(df[col].unique()) == 1:
            l.append(col)            
            df.drop(col,inplace=True,axis=1)
    ho.print_items(l,prefix="drop",excepto=[])        
    return df

def drop_corr_columns(X_t,umbral=0.98):
    ho.print_message("drop_corr_columns: Eliminando columnas correlacionales entre si, con umbral {}".format(umbral))
    
    cor_matrix = X_t.corr().abs()
    upper_tri = cor_matrix.where(np.triu(np.ones(cor_matrix.shape),k=1).astype(np.bool))
    to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > umbral)]

    ho.print_items(to_drop,prefix="drop",excepto=[])

    X_t.drop(to_drop, inplace=True, axis=1)
    return X_t


def drop_nan_columns(X_t,p_min_val = .01): #defecto 
    
    temp1 = X_t.columns    
    thresh = len(X_t) * p_min_val
    ho.print_message("drop_nan_columns: elimina columnas con menos de {}% ({}) registros validos".format(p_min_val*100, thresh))
    X_t.dropna(thresh = thresh, axis = 1, inplace = True)
    temp2 = X_t.columns     
    l = list(set(temp1) - set(temp2))
    
    ho.print_items(l,prefix="drop",excepto=[])


    return X_t
