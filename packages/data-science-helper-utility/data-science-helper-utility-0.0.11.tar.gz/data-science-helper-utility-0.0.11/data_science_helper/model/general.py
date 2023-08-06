# -*- coding: utf-8 -*-

from sklearn.metrics import confusion_matrix, roc_auc_score, classification_report,average_precision_score , f1_score
from sklearn.metrics import roc_curve, precision_recall_curve, auc,recall_score,precision_score
import pickle
from sklearn.model_selection import StratifiedKFold
import seaborn as sns
import numpy as np
import pandas as pd
import os
import json
import data_science_helper.helper_general as hg
import lightgbm as lgb 
#hg.set_base_path()

'''   
MR_File_Name = "base.txt"

def set_macro_region(filename):
    global MR_File_Name
    MR_File_Name = filename

def get_macro_region(macro):
    global MR_File_Name
    js_mr = hg.get_base_path()+"/config/macro_region/"+MR_File_Name
    with open(js_mr) as json_file:
        data = json.load(json_file)        
        
    if macro not in data: 
            raise Exception("No existe la clave " + macro + " en el archivo: "+MR_File_Name)
        
    return data[macro]
    
 
    if(macro=="lima"):
        return ['DRE LIMA METROPOLITANA','DRE LIMA PROVINCIAS','DRE CALLAO']
    elif(macro=="norte"):
        return ['DRE ANCASH','DRE CAJAMARCA','DRE LA LIBERTAD','DRE LAMBAYEQUE','DRE PIURA','DRE TUMBES']
    elif(macro=="sur"):
        return ['DRE AREQUIPA','DRE CUSCO','DRE MADRE DE DIOS','DRE MOQUEGUA','DRE PUNO','DRE TACNA']   
    elif(macro=="centro"):
        return ["DRE APURIMAC","DRE AYACUCHO","DRE HUANCAVELICA",'DRE HUANUCO','DRE JUNIN','DRE PASCO','DRE ICA']
    elif(macro=="oriente"):
        return ['DRE AMAZONAS','DRE LORETO','DRE SAN MARTIN','DRE UCAYALI']
'''

def f1_eval_metric(y_true, y_pred):

    eval_result = f1_score(y_true, y_pred.round())
    return ("f1", eval_result, True)

def precision_eval_metric(y_true, y_pred):

    eval_result = precision_score(y_true, y_pred.round())
    return ("precision", eval_result, True)      

def recall_eval_metric(y_true, y_pred):

    eval_result = recall_score(y_true, y_pred.round())
    return ("recall", eval_result, True)

def average_precision_eval_metric(y_true, y_pred):

    eval_result = average_precision_score(y_true, y_pred)
    return ("average_precision", eval_result, True)

def roc_auc_eval_metric(y_true, y_pred):

    eval_result = roc_auc_score(y_true, y_pred)
    return ("roc_auc", eval_result, True)

def get_fn_eval(score_rs):     
    if(score_rs=="f1"):
        fn_eval=f1_eval_metric
    elif(score_rs=="precision"):
        fn_eval=precision_eval_metric
    elif(score_rs=="recall"):
        fn_eval=recall_eval_metric
    elif(score_rs=="average_precision"):
        fn_eval=average_precision_eval_metric  
    elif(score_rs=="roc_auc"):
        fn_eval=roc_auc_eval_metric
    #else:
    #    fn_eval=custom_eval_metric
        
    return fn_eval


def get_hypers_dic(url,common_params):  
    hypers_dic = {}
    dir_list = os.listdir(url)    
    for file_name in dir_list:
        name = os.path.splitext(file_name)[0]    
        file_path  = url+file_name
        #print(file_path)
        with open(file_path) as json_file:
            data = json.load(json_file)    
            for key_mr , value_mr in data.items():
                for key_mr_model, value_mr_model in value_mr.items():
                    data[key_mr][key_mr_model] = {**common_params, **value_mr_model }
                    #data[key_mr][model_name] = {**common_params, **data[key_mr][model_name] }
           
            hypers_dic[name] = data  
            
    return hypers_dic


def get_hypers_gr_mr_dic(hyperparameters_dir,key,macro_region,model_name,params):
    if hyperparameters_dir is None:
        print("\nNo se especifico ruta para hyperparametros , se empleara valores por defecto\n")
        return params
    hypers_dic = get_hypers_dic(hyperparameters_dir, params)
    
    hypers_dic_gr = hypers_dic.get(key, None)
    if hypers_dic_gr is None:
        print("\nNo existe hyperparametros para {",key, "}, se empleara valores por defecto\n")
        return params
    else:
        hypers_dic_gr_mr = hypers_dic_gr.get(macro_region, None)
        if hypers_dic_gr_mr is None:
            print("\nNo existe hyperparametros para {",key,"-",macro_region, "}, se empleara valores por defecto\n")
            return params
        else:
            hypers_dic_gr_mr_model = hypers_dic_gr_mr.get(model_name, None)
            if hypers_dic_gr_mr_model is None:
                print("\nNo existe hyperparametros para {",key,"-",macro_region, "-",model_name,"}, se empleara valores por defecto\n")
                return params
            else:
                return hypers_dic_gr_mr_model
        
def save_hyper_draft(best_params_full,kpis_dict_full,hyper_draft_dir,key):
    save_json(best_params_full,hyper_draft_dir+key+".json") 
    save_json(kpis_dict_full,hyper_draft_dir+key+"_kpi.json") 
 

def save_json(dict_obj, url_file):
    if url_file is None:
        print("")
    else:
        # create json object from dictionary
        json_ = json.dumps(dict_obj, sort_keys=True, indent=4)
        # open file for writing, "w" 
        f = open(url_file,"w")
        # write json object to file
        f.write(json_)
        # close file
        f.close() 

def get_kfold():
    n_splits = 4
    kfold = StratifiedKFold(n_splits=n_splits, shuffle=True,random_state=2)
    return kfold

def save_model(model,dir_name):    
    if dir_name is None:
        print("")
    else:
        filename ='model.{}' 
        
        if len(dir_name.strip())==0 :
            full_dirname = filename
        else:
            if os.path.isdir(dir_name)==False:
                os.makedirs(dir_name)
            full_dirname = os.path.join(dir_name, filename)        
        
        if type(model)==lgb.basic.Booster:            
            model.save_model(full_dirname.format("booster"))            
        else:                  
            pickle.dump(model, open(full_dirname.format("sav"), 'wb'))   
    
def load_save_model(url_dir):
    filename = url_dir+'/model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model





def generate_summary_evaluation(X,y_prob_uno,y,dir_name,modalidad="EBR"):
    
    if dir_name is None:
        return 
    
    #y_prob_uno = predicted_probas[:,1]
    y_pred = np.round(y_prob_uno, 0)
    

    X_eval = X.copy()
    #X_eval['PREDICT_PROBA'] = estimator_random.predict_proba(X)[:,1]
    #X_eval['PREDICT'] = estimator_random.predict(X)
    
    X_eval['PREDICT_PROBA'] = y_prob_uno
    X_eval['PREDICT'] = list(y_pred)
    
    

    X_eval['REAL'] =  y

    criteria = [X_eval['PREDICT_PROBA'].between(0,0.1),
                X_eval['PREDICT_PROBA'].between(0.1, 0.2), 
                X_eval['PREDICT_PROBA'].between(0.2, 0.3),
                X_eval['PREDICT_PROBA'].between(0.3, 0.4),
                X_eval['PREDICT_PROBA'].between(0.4, 0.5),
                X_eval['PREDICT_PROBA'].between(0.5, 0.6),
                X_eval['PREDICT_PROBA'].between(0.6, 0.7),
                X_eval['PREDICT_PROBA'].between(0.7, 0.8),
                X_eval['PREDICT_PROBA'].between(0.8, 0.9),
                X_eval['PREDICT_PROBA'].between(0.9,0.95),
                X_eval['PREDICT_PROBA'].between(0.95, 1)
               ]

    values = ['0% - 10%', '10% - 20%', '20% - 30%','30% - 40%',
              '40% - 50%','50% - 60%','60% - 70%','70% - 80%','80% - 90%','90% - 95%','95% - 100%']

    values_index = [1, 2,3,4,5,6,7,8,9,10,11]
    
    ###################################################################
    
    criteria2 = [X_eval['PREDICT_PROBA'].between(0.0, 0.5),
                X_eval['PREDICT_PROBA'].between(0.5, 1),             
               ]

    values2 = ['0% - 50%', '50% - 100%']

    values_index2 = [1, 2]
    
    #####################################################
 
    X_eval['PREDICT_CATEGORY'] = np.select(criteria, values, 0)
    X_eval['PREDICT_CATEGORY_INDEX'] = np.select(criteria, values_index, 0)

    X_eval['PREDICT_CATEGORY2'] = np.select(criteria2, values2, 0)
    X_eval['PREDICT_CATEGORY_INDEX2'] = np.select(criteria2, values_index2, 0)

    X_eval['TOTAL'] = 1     

    
    X_eval['ACIERTO(VP)'] = np.where( (X_eval['REAL']==1) & (X_eval['PREDICT']==1), 1 ,0)
    X_eval['FP'] = np.where( (X_eval['REAL']==0) & (X_eval['PREDICT']==1), 1 ,0)    

    X_eval_gb = X_eval.groupby(['PREDICT_CATEGORY_INDEX','PREDICT_CATEGORY']).agg({'TOTAL':'count','REAL':'sum'}).reset_index()
    X_eval_gb.sort_values(by='PREDICT_CATEGORY_INDEX', ascending=False,inplace=True)
    X_eval_gb.rename(columns={'REAL': 'DESERTORES TEST','TOTAL': 'TOTAL TEST','PREDICT_CATEGORY':'RANGO'}, inplace=True)
    del X_eval_gb['PREDICT_CATEGORY_INDEX']
    X_eval_gb.reset_index(drop=True,inplace=True)

    X_eval_gb['TOTAL TEST %']=round(X_eval_gb['TOTAL TEST']/X_eval_gb['TOTAL TEST'].sum(),3)
    X_eval_gb['COBERTURA %']=round(X_eval_gb['DESERTORES TEST']/X_eval_gb['DESERTORES TEST'].sum(),3)


    X_eval_gb['PRECISION RANGO %']=round(X_eval_gb['DESERTORES TEST']/X_eval_gb['TOTAL TEST'],3)

    
    X_eval_gb['TOTAL TEST %'] = X_eval_gb['TOTAL TEST %']*100 
    X_eval_gb['PRECISION RANGO %'] = X_eval_gb['PRECISION RANGO %']*100 
    X_eval_gb['COBERTURA %'] = X_eval_gb['COBERTURA %']*100 
    
    #X_eval_gb.index.name = 'N'


    # Set colormap equal to seaborns light green color palette


    if dir_name is None:
        cm = sns.light_palette("red", as_cmap=True)
        return (X_eval_gb.style
                        .background_gradient(cmap=cm, subset=['PRECISION RANGO %'])
                        #.format({'TOTAL TEST %': "{:.1%}"})  
                        #.format({'PRECISION RANGO %': "{:.1%}"})
                        #.format({'COBERTURA %': "{:.1%}"})
                       )
    else:
        
        filename ='df_agg_t_{}.xlsx'
        if len(dir_name.strip())==0 :
            full_dirname = filename
        else:
            if os.path.isdir(dir_name)==False:
                os.makedirs(dir_name)
            full_dirname = os.path.join(dir_name, filename)  
        
        X_eval_gb.to_excel(full_dirname.format(modalidad), encoding="utf-8") 
        
        if(modalidad=="EBR"):
         #   X_eval_gb.to_excel(url_dir+"/df_agg_t.xlsx", encoding="utf-8")    
            get_min_prob_df(y_prob_uno,y,dir_name)
        #else:
        #    X_eval_gb.to_excel(url_dir+"/df_agg_t_{}.xlsx".format(modalidad), encoding="utf-8")  
            

           
def get_min_prob_df(y_prob_uno,y_test,dir_name):
    
    if dir_name is None:
        return

    #y_prob_uno = predicted_probas[:,1]
    y_pred = np.round(y_prob_uno, 0)

    df = pd.DataFrame()
    df['y_prob_uno']  = y_prob_uno
    df['y_pred']  = y_pred
    df['y_test']  = list(y_test)  
    df.sort_values(by=['y_prob_uno'],ascending=False,inplace=True)
    #print(df.head(20))
    total_deser = np.sum(y_test)  


    list_y_true = []
    list_y_pred = []
    list_precision = []
    prob_min = 0
    t_test_min = 0
    prec = 0 
    for index, row in df.iterrows(): 
        list_y_true.append(row['y_test'])
        list_y_pred.append(row['y_pred'])
        pr = precision_score(list_y_true, list_y_pred, average='binary')
        list_precision.append(pr)
        if(pr<1):
            break
        else:
            prob_min = row['y_prob_uno']
            t_test_min = len(list_y_true)
            prec = pr


    df_min = pd.DataFrame()
    df_min['PROB MIN']  = [prob_min]
    df_min['TOTAL DESERTORES TEST RANGO']  = [t_test_min]
    df_min['TOTAL DESERTORES TEST']  = [int(total_deser)]
    df_min['PRECISION RANGO %']  = [int(prec*100)]
    #return df_min
    
    filename ='df_agg_t_min.xlsx'
    if len(dir_name.strip())==0 :
        full_dirname = filename
    else:
        if os.path.isdir(dir_name)==False:
            os.makedirs(dir_name)
        full_dirname = os.path.join(dir_name, filename) 
    
    df_min.to_excel(full_dirname, encoding="utf-8")