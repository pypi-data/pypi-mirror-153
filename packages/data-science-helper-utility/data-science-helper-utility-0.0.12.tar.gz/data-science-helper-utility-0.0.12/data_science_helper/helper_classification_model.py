# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 15:44:39 2021

@author: User
"""
#import core_helper.helper_general as hg
#hg.set_base_path()

from data_science_helper import helper_general as hg


import json
import os
import math
import sys
import math
import os
import pandas as pd
import numpy as np
import time
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import lightgbm as lgb 
#import core_helper.helper_plot as hp
#import src.Prj_Core.core_helper.helper_plot as hp
from data_science_helper import helper_plot as hp


#import model.general as g
#import src.Prj_Core.core_helper.model.general as g
from data_science_helper.model import general as g
from data_science_helper.model import neg_bagging_fraction__lgb_model as nbf_lgb_model
from data_science_helper.model import scale_pos_weight__lgb_model as spw_lgb_model
from data_science_helper.model import custom_bagging__lgb_model as cb_lgb_model



#import src.Prj_Core.core_helper.model.neg_bagging_fraction__lgb_model as nbf_lgb_model
#import src.Prj_Core.core_helper.model.scale_pos_weight__lgb_model as spw_lgb_model
#import src.Prj_Core.core_helper.model.custom_bagging__lgb_model as cb_lgb_model

#import model.neg_bagging_fraction__lgb_model as nbf_lgb_model
#import model.scale_pos_weight__lgb_model as spw_lgb_model
#import model.custom_bagging__lgb_model as cb_lgb_model

def modelar_clasificacion_binaria(strategy="", X_train=None,y_train=None,X_test=None,y_test=None,params=None,metric='average_precision',api="train_api",url=None,print_consola=True):
    start = time.time()
            
    args = {'X_train':X_train, 'y_train': y_train, 'X_test': X_test, 'y_test': y_test, 'params':params, "metric":metric,"api":api , "url":url }    
    
    if (strategy=="neg_bagging_fraction__lgb_model"):
        model , y_prob_uno   = nbf_lgb_model.modelar(**args)
    if (strategy=="scale_pos_weight__lgb_model"):
        model , y_prob_uno   = spw_lgb_model.modelar(**args)
    if (strategy=="custom_bagging__lgb_model"):
        model , y_prob_uno   = cb_lgb_model.modelar(X_train,y_train,X_test,y_test,url)

    kpis = generar_reporte(model,y_prob_uno,X_test,y_test,url,print_consola)
    print("Time elapsed: ", time.time() - start)
    
    return model , y_prob_uno  , kpis


def modelar_clasificacion_binaria_rscv(strategy, X_train,y_train=None,X_test=None,y_test=None,score_rs=None,params=None,param_dist=None, n_iter=None,n_jobs=None,url=None,print_consola=True):
    if url is not None:
        hg.validar_directorio(url)     

    if (strategy=="neg_bagging_fraction__lgb_model"):
        results, model , predicted_probas, params, best_params = nbf_lgb_model.modelar_rscv(X_train,y_train,X_test,y_test,score_rs,params,param_dist,n_iter,n_jobs,url)
        
    if (strategy=="scale_pos_weight__lgb_model"):
        results, model , predicted_probas, params, best_params = spw_lgb_model.modelar_rscv(X_train,y_train,X_test,y_test,score_rs,params,param_dist,n_iter,n_jobs,url)
       
    if (strategy=="custom_bagging__lgb_model"):
        results, model , predicted_probas, params, best_params = spw_lgb_model.modelar_rscv(X_train,y_train,X_test,y_test,score_rs,params,param_dist,n_iter,n_jobs,url)
       
    kpis = generar_reporte(model,predicted_probas,X_test,y_test,url,print_consola)
    
    return results, model , predicted_probas, params, best_params ,kpis
    

def generar_reporte(model,y_prob_uno, X_test, y_test,url,print_consola):    
    kpis = hp.print_kpis_rendimiento_modelo(y_test,y_prob_uno,url,print_consola)   
    if  isinstance(model, list)==False:
        if (print_consola):
            hp.print_shap_plot(model, X_test, url)      
    g.generate_summary_evaluation(X_test,y_prob_uno,y_test,url) 
    return kpis
    
    
def predecir_clasificacion_binaria(model, X=None, umbral=0.5):
    print("inicio predecir_clasificacion_binaria")
    
    if type(model)==lgb.basic.Booster:
        y_prob_uno = model.predict(X, num_iteration=model.best_iteration)      
        
    elif  isinstance(model, list)==False:    
        predicted_probas = model.predict_proba(X)
        y_prob_uno = predicted_probas[:,1]
    else:
        print("modelo es una lista")
        y_pred,y_prob_uno , predicted_probas = cb_lgb_model.predict_proba(model, X)
    
    y_pred_uno = np.where(y_prob_uno >= umbral, 1, 0).tolist()
    print("fin  predecir_clasificacion_binaria")
    return y_pred_uno, y_prob_uno



def get_result_df(KPIs_list):
    df = pd.DataFrame(columns=["Macro Región","Modelo","T Train","T Test",'Precision', 'Recall', 'F1','Average Precision','ROC AUC'])
    for idx, result  in enumerate(KPIs_list):
        mr = result[0]
        mod = result[1]
        
        t_train = result[2]
        t_test = result[3]
        
        Ks = result[4]
        result_rd = [mr,mod,t_train,t_test]+[round(num, 3) for num in list(Ks)]
        df.loc[idx] = result_rd

        #df.loc[i] = list(KPIs)

    return df

def get_kpi_df_nacional(PATH_RESULT="resultado",grupos_grados=None,lista_mr=None):
    df_resumen = None
    #grupos_grados = {"1 prim": [4],"2 prim": [5], "3-5 prim": [6,7,8], "6 prim": [9], "1-4 sec": [10,11,12,13],"5 sec": [14]}
    #lista_mr = ["centro","norte","sur","oriente","lima"]
    
    list_df = []
    for key, grupo_grado  in grupos_grados.items():
        path = "{}/{}/{}".format(PATH_RESULT,key,"resultados.xlsx")
    
        df = pd.read_excel (path,index_col=0)
        idx = df.groupby(['Macro Región'])['Average Precision'].transform(max) == df['Average Precision']
        df = df[idx].copy()
        df["key_grupo_grado"] = key
        list_df.append(df)
    
    df_resumen = pd.concat(list_df)
    return df_resumen


def get_test_size(X_t):
    Total_X_t =  X_t.shape[0]
    Total_Test = 20000 # Cantidad minima de Test
    test_size = round(Total_Test/Total_X_t,5)
    
    min_test_size = 0.20
    if(test_size > min_test_size):
        test_size = 0.20    
    print("test_size : ", test_size)
    return test_size

def export_resultado_final_nacional(alto=0.75,medio=0.5,grupos_grados=None,lista_mr=None,path="resultado",
                                    delta_path=None,modelos=[]):
    if (grupos_grados is None):
        msg = "ERROR: No se ha especificado el parametro 'grupos_grados'"      
        raise Exception(msg)   
        
    if (lista_mr is None):
        msg = "ERROR: No se ha especificado el parametro 'lista_mr', que contiene la lista de macro regiones"      
        raise Exception(msg)   

    hg.validar_directorio(path)    
    if delta_path is not None:
        hg.validar_directorio(delta_path) 
        
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d%m%Y_%H%M%S")
    #"norte","sur"
    #grupos_grados = { "3-5 prim": [6,7,8]}
    #lista_mr = ["norte"]
    df_resumen = get_kpi_df_nacional(path+"/02.Modelo",grupos_grados)
        
    dt = {'COD_MOD':str,'COD_MOD_T':str,'ANEXO':int,'ANEXO_T':int,'EDAD':int,
      'N_DOC':str,'COD_MOD_T_MENOS_1':str,
      'ANEXO_T_MENOS_1':int,'NUMERO_DOCUMENTO_APOD':str,'ID_PERSONA':int}
    
    list_result = []
    
    if len(modelos)==0:
        modelos = ["neg_bagging_fraction__lgb_model","scale_pos_weight__lgb_model"] 
    
    columns = ['ID_PERSONA'] + modelos
    
    for key, grupo_grado  in grupos_grados.items():
        
        for macro_region in lista_mr:
            #print("obteniendo best model : ",macro_region," - ",key)
            best_model = df_resumen[(df_resumen.key_grupo_grado==key) & (df_resumen['Macro Región']==macro_region)]
            if best_model.shape[0]==0:
                msg = "ERROR: El archivo resultados.xlsx para el grupo de grados '"+key+"' no tiene resultados para la macro region: "+macro_region      
                raise Exception(msg)   
                
            best_model = best_model.Modelo.iloc[0]
            print(best_model," - ",macro_region," - ",key)
            if delta_path is None:
                specific_url = '{}/{}/{}/{}/{}'.format(path,"01.data_input",key,macro_region,"X_t_mas_1.csv")
            else:
                specific_url = '{}/{}/{}/{}/{}'.format(delta_path,"01.data_input",key,macro_region,"X_t_mas_1.csv")
                
            df=pd.read_csv(specific_url,dtype=dt, encoding="utf-8",usecols=columns) 
            df['RISK_SCORE'] = df[best_model] 
            list_result.append(df)
            
          
    df_nacional = pd.concat(list_result)
    df_nacional.drop_duplicates(subset ="ID_PERSONA",  keep = "first", inplace = True)
      
    df_nacional['PREDICCION']=None
    df_nacional.loc[(df_nacional['RISK_SCORE']>=alto) & (df_nacional['RISK_SCORE']<=1), 'PREDICCION'] = 3
    df_nacional.loc[(df_nacional['RISK_SCORE']>=medio) & (df_nacional['RISK_SCORE']<alto), 'PREDICCION'] = 2
    df_nacional.loc[df_nacional['RISK_SCORE']<medio, 'PREDICCION'] = 1
    df_nacional.PREDICCION = df_nacional.PREDICCION.astype(int)      
    
    cls_export = ["ID_PERSONA","RISK_SCORE",'PREDICCION']
    print("Total de registros : ",df_nacional.shape)
    if delta_path is None:
        url = "{}/{}/".format(path,"03.data_output")
        hg.validar_directorio(url)  
        filename = "nacional_{}.dta".format(dt_string)
        df_nacional[cls_export].to_stata(url+filename) 
    else:
        url = "{}/{}/".format(delta_path,"02.data_output")
        hg.validar_directorio(url) 
        filename = "nacional_{}.dta".format(dt_string)         
        df_nacional[cls_export].to_stata(url+filename)
    return df_nacional




def show_barplot_resultado_final_nacional(grupos_grados=None, lista_mr = None, scores = [] ,path = None,show=False):
    df_resumen = get_kpi_df_nacional(PATH_RESULT=path,grupos_grados=grupos_grados,lista_mr=lista_mr)
    
    list_result_total = []
    for macro_region in lista_mr:
        list_mr = []
        for score in scores:
            for key, grupo_grado  in grupos_grados.items():
                directory = path+"/"+str(key)
                hg.validar_directorio(directory) 
                final_path = directory+ "/resultados.xlsx"
                
                df = pd.read_excel(final_path, index_col=0)  
               
                best_model = df_resumen[(df_resumen.key_grupo_grado==key) & (df_resumen['Macro Región']==macro_region)]
                if best_model.shape[0]==0:
                    msg = "ERROR: El archivo resultados.xlsx para el grupo de grados '"+key+"' no tiene resultados para la macro region: "+macro_region      
                    raise Exception(msg)   
    
                valor = best_model[score].values[0]
                
                df_mr_grado = pd.DataFrame() 
                df_mr_grado['Valor'] = [valor] 
                df_mr_grado['Indicador'] = [score] 
                df_mr_grado['Grados'] = [key]        
                df_mr_grado['MR'] = [macro_region]
    
                list_mr.append(df_mr_grado)
        df_mr = pd.concat(list_mr)
        show_barplot_rf_n(df_mr,macro_region,path,show)
        list_result_total.append(df_mr)
    
    df_result_total = pd.concat(list_result_total)
    show_barplot_rf_n(df_result_total,"Nacional",path,show)
    return df_result_total

def show_barplot_rf_n(df,titulo_top_left="",dir_name=None,show=False):
    fig = plt.figure(figsize=(15, 6))
    ax = sns.barplot(x='Grados',y='Valor',data=df, hue='Indicador')
    
    for p in ax.patches:    
        height = p.get_height()
        #print(height)
        if math.isnan(height):
            height = 0
        #height = round(height,0)
        ax.text(p.get_x()+p.get_width()/2.,
                height ,
                '{:0.2f}'.format(height),
                ha="center") 
    plt.suptitle(titulo_top_left.upper()+' - Robustez por Grado', fontsize=20)
    ax.legend(ncol = 3, loc = 'best', bbox_to_anchor=(0.65, -0.1))
    
    
    if show :
        plt.show()
       
    filename =titulo_top_left+'_barplot.png'
    if len(dir_name.strip())==0 :
        full_dirname = filename
    else:
        if os.path.isdir(dir_name)==False:
            os.makedirs(dir_name)
        full_dirname = os.path.join(dir_name, filename)         
            
    plt.savefig(full_dirname, bbox_inches='tight')
    plt.close()

'''            
def split_x_y(ID_GRADO,macro_region,modalidad="EBR"):

    lista_regiones = get_macro_region(macro_region)
    list_join_n=[]
    list_join_n_mas_1=[]
    for region in lista_regiones:

        url_dir = "{}/{}/".format(region,ID_GRADO)
        print(url_dir)
        try:
            df_join_n , df_join_n_mas_1 = get_saved_join_data(url_dir,modalidad=modalidad)
        except:
            continue
        
        #df_join_n , df_join_n_mas_1 = get_saved_join_data(url_dir,modalidad=modalidad)
        df_join_n['REGION']= region
        df_join_n_mas_1['REGION']= region
        
        ############tempEEE#######
        df_join_n['D_REGION']= region
        df_join_n_mas_1['D_REGION']= region
        ########################
        
        
        print(region)
        print(df_join_n.DESERCION.value_counts())
        list_join_n.append(df_join_n)
        list_join_n_mas_1.append(df_join_n_mas_1)

    df_join_n = pd.concat(list_join_n)
    df_join_n_mas_1 = pd.concat(list_join_n_mas_1)

    fe_df(df_join_n,df_join_n_mas_1)

    X_train, X_test, y_train, y_test , X_t, X_t_eval, y_eval , ID_P_T,ID_P_T_MAS_1, y = tranform_data(df_join_n,df_join_n_mas_1,False)
    

    return X_train, X_test, y_train, y_test , X_t, X_t_eval, y_eval ,  ID_P_T,ID_P_T_MAS_1 , y
   

def get_saved_join_data(url_dir,sub_dir="data",modalidad="EBR"):
    
    if not url_dir:
        url_dir="../02.PreparacionDatos/03.Fusion/reporte_modelo/"+sub_dir+"/"
    else:
        url_dir = '{}/{}'.format("../02.PreparacionDatos/03.Fusion/reporte_modelo/"+sub_dir,url_dir)
        if not os.path.exists(url_dir):
            os.makedirs(url_dir)
        print("reporte generado en : "+url_dir)
    
    if (modalidad=="EBR"):
        specific_url = url_dir+"data.csv"
        specific_url_eval = url_dir+"data_eval.csv"
    else:
        specific_url = url_dir+"data_{}.csv".format(modalidad)
        specific_url_eval = url_dir+"data_eval_{}.csv".format(modalidad)        
    
    dt = {'COD_MOD':str,'COD_MOD_T':str,'ANEXO':int,'ANEXO_T':int,'EDAD':int,
          'N_DOC':str,'COD_MOD_T_MENOS_1':str,
          'ANEXO_T_MENOS_1':int,'NUMERO_DOCUMENTO_APOD':str,'ID_PERSONA':int}

    df=pd.read_csv(specific_url,dtype=dt, encoding="utf-8") 
    df_eval=pd.read_csv(specific_url_eval,dtype=dt, encoding="utf-8") 
    
    return df,df_eval

 ''' 