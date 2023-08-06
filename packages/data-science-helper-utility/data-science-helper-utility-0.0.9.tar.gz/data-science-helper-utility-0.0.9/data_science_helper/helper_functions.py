import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sklearn
from matplotlib import colors
from sklearn import datasets
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os



# Codifica todas las variables categoricas o de tipo object con LabelEncoder
def encoder_cat(X=None,columns_cat=[]):    
    le = LabelEncoder()
    for c in columns_cat:
        col_type = X[c].dtype
        if col_type == 'object' or col_type.name == 'category':
            #print("column : "+str(c))
            X[c] = le.fit_transform(X[c])
      



def pivot_columns(df_prod_bco_pivot):
    cls_fre = zip(df_prod_bco_pivot.columns.get_level_values(0),df_prod_bco_pivot.columns.get_level_values(1))
    simple_columns = []
    for i in cls_fre: 
        simple_columns.append(str(i[0])+"_"+str(i[1]))

    df_prod_bco_pivot.columns = simple_columns
    df_prod_bco_pivot.reset_index(inplace=True)
    #return simple_columns




def clean_df(df, columns):
    for column in columns:
        df[column] = df[column].astype('str')
        df[column] = df[column].str.strip()
        df[column] = df[column].str.upper()
        

def plot_boundaries_iris_dataset(model, iris):
    plt.figure(figsize=(14, 8))
    for pairidx, pair in enumerate([[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]):
        
        
        # Parameters
        n_classes = 3
        plot_colors = "rgb"
        cmap = colors.ListedColormap(['mistyrose', 'honeydew', 'lavender'])
        plot_step = 0.02

        # We only take the two corresponding features
        X = iris.data[:, pair]
        y = iris.target

        # Train
        clf = sklearn.base.clone(model)
        clf.fit(X, y)

        
        # Plot the decision boundary
        plt.subplot(2, 3, pairidx + 1)

        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step),
                             np.arange(y_min, y_max, plot_step))

        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        cs = plt.contourf(xx, yy, Z, cmap= cmap)

        plt.xlabel(iris.feature_names[pair[0]])
        plt.ylabel(iris.feature_names[pair[1]])
        plt.axis("tight")

        # Plot the training points
        for i, color in zip(range(n_classes), plot_colors):
            idx = np.where(y == i)
            plt.scatter(X[idx, 0], X[idx, 1], c=color, label=iris.target_names[i],
                        cmap=plt.cm.Paired, s=5, alpha = 0.8)

        plt.axis("tight")

    plt.suptitle("Decision surface using paired features")
    plt.legend()
    plt.show()

    
    

    
    


import random
def plot_digits_sample(images, target, labels = None):
    # The data that we are interested in is made of 8x8 images of digits, let's
    # have a look at the first images, stored in the `images` attribute of the
    # dataset.  If we were working from image files, we could load them using
    # matplotlib.pyplot.imread.  Note that each image must have the same size. For these
    # images, we know which digit they represent: it is given in the 'target' of
    # the dataset.
    

    fig, axes = plt.subplots(5, 5, figsize=(5, 5),
                             subplot_kw={'xticks':[], 'yticks':[]},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))

    for i, ax in enumerate(axes.flat):
        im = random.randint(0, len(images)-1)
        ax.imshow(images[im].reshape([8,8]), cmap=plt.cm.gray_r, interpolation='nearest')
        ax.text(0.05, 0.05, str(target[im]),
                transform=ax.transAxes, color='green')

    plt.show()
    

