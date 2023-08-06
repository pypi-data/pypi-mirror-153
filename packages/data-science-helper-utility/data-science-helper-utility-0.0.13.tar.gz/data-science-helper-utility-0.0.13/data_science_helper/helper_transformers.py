
import shap
import matplotlib.pylab as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder , LabelBinarizer
import seaborn as sns
import pandas as pd
import pyodbc
import numpy as np
import pyodbc
import missingno as msno
from nltk.corpus import stopwords
import nltk
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD

from data_science_helper import helper_dataframe as hd

import string
from nltk.stem.snowball import SnowballStemmer
import nltk 
from sklearn.metrics import silhouette_score
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import SpectralClustering
from scipy.stats import itemfreq
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
import lightgbm as lgb
import pandas as pd

from sklearn import preprocessing, decomposition, svm #, cross_validation


class ShapFeatureSelector( BaseEstimator, TransformerMixin ):
    #Class Constructor 
    def __init__( self,  objective="binary",min_shap=0,test_size=0.25,verbose=1,categorical_columns_name=[] ):
        #self._feature_names = feature_names 
        self._objective = objective
        self._min_shap = min_shap
        self._test_size=test_size
        self._model = None
        self._verbose = verbose
        self._categorical_columns_name = categorical_columns_name
    
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        
        print("inicio del proceso: feature_sel_shap con  min_shap:"+str(self._min_shap))
        train_cols = X.columns.tolist()

#         _cols = X.columns
#         _num_cols = X._get_numeric_data().columns
#         _categorical_columns_name = list(set(_cols) - set(_num_cols))
        
#         le = preprocessing.LabelEncoder()
#         for c in _categorical_columns_name:
#             col_type = X[c].dtype
#             if col_type == 'object' or col_type.name == 'category':
#                 #print("column : "+str(c))
#                 X[c] = le.fit_transform(X[c])
#                 #X[c] = X[c].astype('category') 
        
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self._test_size, stratify=y, random_state=1)

        
        train_data = lgb.Dataset(X_train, label=y_train.astype(int), feature_name=train_cols)
        test_data = lgb.Dataset(X_test, label=y_test.astype(int), feature_name=train_cols, reference=train_data)
        
        # LGB parameters:
        params = {
                'metric': 'binary_error',
                'learning_rate': 0.01,
                'boosting': 'gbdt', 
                'objective': self._objective,
                'num_leaves': 2000,
                'min_data_in_leaf': 200,
                'max_bin': 200,
                'max_depth': -1,
                'seed': 2018,
                'nthread': 10,
                "lambda_l1": 0.1,            
                }
        
        self._model = lgb.train(params, train_data, 
                    categorical_feature=self._categorical_columns_name,
                    num_boost_round=1000, 
                    valid_sets=(test_data,), 
                    valid_names=('valid',), 
                    verbose_eval=False, 
                    early_stopping_rounds=20)
        
        return self 
    
    #Method that describes what we need this transformer to do
    def transform( self, X, y = None ):
        
        if(self._model is not None):
            explainer = shap.TreeExplainer(self._model)
            shap_values = explainer.shap_values(X)

            if(self._objective=="multiclass"):
                shap_sum = np.abs(shap_values).mean(axis=0).mean(axis=0)
            else:  
                shap_sum = np.abs(shap_values).mean(axis=0).mean(axis=0)

            #print("shap_sum...done")
            importance_df = pd.DataFrame([X.columns.tolist(), shap_sum.tolist()]).T
            importance_df.columns = ['column_name', 'shap_importance']
            importance_df = importance_df.sort_values('shap_importance', ascending=False)

            importance_df['percentage'] = (importance_df['shap_importance']/importance_df['shap_importance'].sum())*100
            importance_df.reset_index(inplace=True,drop=True)
            if(self._verbose==1):
                print(importance_df)
            
            
            zero_features = importance_df[importance_df['shap_importance']<=self._min_shap].column_name.values
            return X.drop(columns = zero_features)     
        else:
            print("No se ha ejecutado el metodo FIT")
            
    def importances_df(self):
        return self._importance_df


class CorrTransformer( BaseEstimator, TransformerMixin ):
    #Class Constructor 
    def __init__( self, umbral  = 0.95 ):
        self.to_drop  = []
        self.umbral = umbral
    
    #Return self nothing else to do here    
    def fit( self, X, y = None ):   
        
        c_c = hd.get_cat_columns(X)
        
        # Create correlation matrix
        corr_matrix = X.drop(c_c,axis=1).corr().abs()
        # Select upper triangle of correlation matrix
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
        # Find index of feature columns with correlation greater than 0.95
        to_drop = [column for column in upper.columns if any(upper[column] > self.umbral)]
        self.to_drop = to_drop
        return self 
    
    #Method that describes what we need this transformer to do
    def transform( self, X, y = None ):
        
        new_df = X.drop(self.to_drop,axis=1,inplace=False)  
        return new_df
        
     
       
    
class CatTransformer( BaseEstimator, TransformerMixin ):
    #Class Constructor 
    def __init__( self, pp  = "le" , console= False ):
        
        #columns_cat
        self.cat_encoders  = []
        self.encoded_df = []
        self.pp = pp
        self.console = console
    
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        
        self.catcolumns = hd.get_cat_columns(X)

        for name in self.catcolumns:
            if(self.pp=="le"):
                le = LabelEncoder()  
            elif(self.pp=="lb"):
                le = LabelBinarizer()  
            else:
                msg = "Error: pp INVALIDO"
                raise Exception(msg)
                break;
            if self.console==True:
                print("NEW Binarios {}".format(name))
            if X[name].isna().any():
                msg = "ERROR: La columna "+name+" tiene valores MISSING, corregir eso para continuar"
                raise Exception(msg)
                #print("ERROR: La columna ",name," tiene valores MISSING, corregir eso para continuar")
                break
            le.fit(X[name])
            self.cat_encoders.append((name, le))
        return self 
    
    #Method that describes what we need this transformer to do
    def transform( self, X, y = None ):
        
        #print(self.cat_encoders)
        for name, encs in self.cat_encoders :
            df_c = encs.transform(X[name])
            
            prefix = str(name) + "_"

            if(self.pp=="le"):
                self.encoded_df.append(pd.DataFrame(df_c,columns=[name],index=X.index))
            elif(self.pp=="lb"):
                #self.encoded_df.append(pd.DataFrame(df_c,columns=encs.classes_,index=X.index).add_prefix(str(prefix).upper()))
                if(df_c.shape[1]==1):                    
                    if (len(encs.classes_)==2):  
                        classe_1 = encs.classes_[1]+"_pos_"+encs.classes_[0]+"_neg"
                        self.encoded_df.append(pd.DataFrame(df_c,columns=[classe_1],index=X.index).add_prefix(str(prefix).upper()))
                    else:
                        self.encoded_df.append(pd.DataFrame(df_c,columns=[name],index=X.index))                    
                else:                
                    self.encoded_df.append(pd.DataFrame(df_c,columns=encs.classes_,index=X.index).add_prefix(str(prefix).upper()))          
            
            else:
                print("Error: pp INVALIDO")
                break;            
            
        encoded_df_c = pd.concat(self.encoded_df, axis = 1, ignore_index  = False)   
        #print(list(encoded_df_c.columns))
        #print(self.encoded_df.columns)
       
        self.df_num = X.drop(self.catcolumns, axis = 1) 
        #print(self.df_num.shape)
        #print(list(self.df_num.columns))
        new_df = pd.concat([self.df_num, encoded_df_c], axis = 1, ignore_index = False)
        
        #para que las columnas categoricas codificadas con numeros no se confundan con valores numericos, le asignamos tipo category
        if(self.pp=="le"):
            for c in self.catcolumns:
                new_df[c] = new_df[c].astype('category') 
        
        #print(new_df.shape)
        #print(list(y.columns))
        return new_df
        
     
        
        
        
class FeatureSelector( BaseEstimator, TransformerMixin ):
    #Class Constructor 
    def __init__( self, feature_names ):
        self._feature_names = feature_names 
    
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self 
    
    #Method that describes what we need this transformer to do
    def transform( self, X, y = None ):
        return X[ self._feature_names ] 