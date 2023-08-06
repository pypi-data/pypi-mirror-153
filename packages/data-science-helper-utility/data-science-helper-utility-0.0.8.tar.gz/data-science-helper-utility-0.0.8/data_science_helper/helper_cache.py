# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 08:25:11 2021

@author: User
"""
import numpy as np
import pandas as pd

from data_science_helper import helper_general as hg

#import core_helper.helper_general as hg
#hg.set_base_path()

def get_key_cache(list_values):
    #``^[a-zA-Z_][a-zA-Z0-9_]*$``
    key='_'.join([str(elem) for elem in list_values])
    key=key.replace(" ", "")
    key="key_"+key
    return key

def get_cache(filename,key):
    try: 
        path_cache = hg.get_base_path()+'\\cache'
        path_cache = path_cache+'\\'+filename+".h5" 
        print("path_cache : "+path_cache)
        df_ = pd.read_hdf(path_cache,key)  
        return df_ 
    except:
        print("No hay cache disponible para los parametros ingresados")
        return None        
    
    
def save_cache(df,filename,key):
    print("guardando cache")
    path_cache = hg.get_base_path()+'\\cache'
    hg.validar_directorio(path_cache) 
    path_cache = path_cache+'\\'+filename+".h5"   
    print("path_cache : "+path_cache)
    df.to_hdf(path_cache, key=key, mode='a')