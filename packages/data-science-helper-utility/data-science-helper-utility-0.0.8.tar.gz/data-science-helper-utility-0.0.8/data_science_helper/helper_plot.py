# -*- coding: utf-8 -*-
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sklearn
from sklearn.model_selection import learning_curve
from sklearn.metrics import roc_curve, roc_auc_score
import shap
import os
import scikitplot as skplt
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import confusion_matrix, roc_auc_score, classification_report,average_precision_score , f1_score
   
def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=-1, train_sizes=np.linspace(.1, 1.0, 7), score="",url_dir=""):
    """Generate a simple plot of the test and training learning curve"""
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score : "+score)
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes, scoring = score)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    if not url_dir:
        plt.show()
    else:
        plt.savefig(url_dir+'learning_curve.png', bbox_inches='tight')
        plt.close()
        
        
def plot_confusion_matrix(cm, class_labels,url_dir=""):
    """Pretty prints a confusion matrix as a figure

    Args:
        cm:  A confusion matrix for example
        [[245, 5 ], 
         [ 34, 245]]
         
        class_labels: The list of class labels to be plotted on x-y axis

    Rerturns:
        Just plots the confusion matrix.
    """
    
    df_cm = pd.DataFrame(cm, index = [i for i in class_labels],
                  columns = [i for i in class_labels])
    sns.set(font_scale=1)
    sns.heatmap(df_cm, annot=True, fmt='g', cmap='Blues')
    plt.xlabel("Predicted label")
    plt.ylabel("Real label")
    #plt.show()
    if not url_dir:
        plt.show()
    else:
        plt.savefig(url_dir+'confusion_matrix.png', bbox_inches='tight')
        plt.close()
        

def print_kpis_rendimiento_modelo(y_test,predicted_probas,dir_name,print_consola):   
    
    y_prob_uno = predicted_probas[:,1]
    y_pred = np.round(y_prob_uno, 0)
    
    #y_pred = np.round(y_prob_uno, 0) se estaba repitiendo
    precision, recall, f1, support = precision_recall_fscore_support(y_test, y_pred,average="binary",pos_label=1)
    average_precision = average_precision_score(y_test, y_pred,pos_label=1)
    roc_auc = roc_auc_score(y_test, y_prob_uno) 
    
    if (print_consola):
        
        print(classification_report(y_test, y_pred))
        print("average_precision", average_precision)
        print(" -------  roc_auc_score -----------")
        
        
        skplt.metrics.plot_roc(y_test, predicted_probas)    
        if dir_name is None:
            plt.show()
        else:        
            filename ='roc_curve.png'
            if len(dir_name.strip())==0 :
                full_dirname = filename
            else:
                if os.path.isdir(dir_name)==False:
                    os.makedirs(dir_name)
                full_dirname = os.path.join(dir_name, filename)         
                    
            plt.savefig(full_dirname, bbox_inches='tight')
            plt.close()
    
    return precision, recall, f1 , average_precision , roc_auc



def print_shap_plot(model,X_test,dir_name):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    #shap.summary_plot(shap_values, X_test)    
    #print(shap_values[0].shape)
    if dir_name is None:
        #shap_values[1] hace referencia a los valores shap de la class 1
        shap.summary_plot(shap_values[1], X_test)
    else:
        filename ='importancia_variables.png'
        if len(dir_name.strip())==0 :
            full_dirname = filename
        else:
            if os.path.isdir(dir_name)==False:
                os.makedirs(dir_name)
            full_dirname = os.path.join(dir_name, filename)       
                      
        
        fig = shap.summary_plot(shap_values[1], X_test,show=False )
        plt.savefig(full_dirname, bbox_inches='tight')
        plt.close(fig)      
         


def get_auc(y, y_pred_probabilities, class_labels, column =1, plot = True):
    fpr, tpr, _ = roc_curve(y == column, y_pred_probabilities[:,column])
    roc_auc = roc_auc_score(y_true=y, y_score=y_pred_probabilities[:,1])
    print ("AUC: ", roc_auc)
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()
        