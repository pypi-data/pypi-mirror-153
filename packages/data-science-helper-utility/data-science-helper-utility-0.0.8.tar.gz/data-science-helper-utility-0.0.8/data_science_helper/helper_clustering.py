import matplotlib.pylab as plt
import matplotlib.cm as cm

from sklearn import preprocessing
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


import string
from nltk.stem.snowball import SnowballStemmer
import nltk 
from sklearn.metrics import silhouette_score,silhouette_samples
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import SpectralClustering
from scipy.stats import itemfreq
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd



class ClusterTransform( BaseEstimator, TransformerMixin ):
    #Class Constructor                                                               
    def __init__( self,  cluster_model='KMeans',embedded="TSNE",progreso_score=False,perplexity=40,
                 n_clusters=20,verbose=1,start=1 ,limit=50,step=5,label_group=None,color_map=None ):
        
        #self._feature_names = feature_names 
        self._progreso_score = progreso_score
        self._n_clusters = n_clusters
 
        self._model = None
        self._verbose = verbose
        self._start = start
        self._limit = limit
        self._step = step
        self._perplexity = perplexity
        self._cluster_model = cluster_model
        self._embedded = embedded
        
        self._label_group = label_group
        self._color_map = color_map
    
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
                     

        
        return self 
    
    #Method that describes what we need this transformer to do
    def transform( self, X, y = None ):
        
        print("inicio del proceso: cluster_summary ")     
        
        labels = cluster_summary(X,embedded = self._embedded,
                                      perplexity = self._perplexity,
                                      cluster_model = self._cluster_model,                                      
                                      progreso_score = self._progreso_score,
                                      n_clusters = self._n_clusters,
                                      start=self._start ,limit=self._limit,step=self._step,
                                      label_group = self._label_group,
                                      color_map = self._color_map,
                                )
        
        return labels

            
    def importances_df(self):
        return self._importance_df




def cluster_summary(df=None, embedded='TSNE',perplexity=40,cluster_model='KMeans',n_clusters=30
                 ,progreso_score=False,start=1 ,limit=50,step=5,embedded_in_cluster=True,plot=True,
                    return_silhouette_score=False,label_group=None,color_map=None):
    
        random_state=42
        df_text = df.copy()

        X = df_text.copy()
        
        data_vector = X.values

        if(embedded=='TSNE'):
            X_embedded = TSNE(n_components=2, perplexity=perplexity, verbose=0).fit_transform(data_vector)             
            #try data_vector or X_reduced
            #verbose->2 para mostrar log
        else:
            pca = PCA(n_components=2, random_state=random_state)
            X_embedded = pca.fit_transform(data_vector)
            
        if embedded_in_cluster:
            data_vector = X_embedded

        print(cluster_model)
        if(cluster_model=='KMeans'):        
            clustering_model = KMeans(n_clusters=n_clusters, max_iter=200, n_init=100,random_state=42)
            labels = clustering_model.fit_predict(data_vector)
            
        elif(cluster_model=='DBSCAN'):             
            clustering_model = DBSCAN().fit(data_vector)
            labels = clustering_model.labels_
        elif(cluster_model=='SpectralClustering'): 
            clustering_model=SpectralClustering(n_clusters= n_clusters, affinity='nearest_neighbors')
            labels = clustering_model.fit_predict(data_vector)
        
        if label_group==None:
            labels_names = ["Class_" + str(x) for x in labels]
        else:
            labels_names = list(map(label_group.get, labels))
        
        if plot:
            colors = plot_cluster(X=X_embedded,range_n_clusters=[n_clusters],
                                  clusterer=clustering_model,cluster_labels=labels,color_map=color_map)
            fig = plt.figure(figsize=(8, 5))
            
            if color_map==None:
                colors = colors.tolist()
            print("-----------------")
            #print(len(labels))
            #print(len(colors)) 
            print("-----------------")
            
            #print(labels)
            #print(colors.head())
            DATA = {'label': labels_names,
                    'color': colors
                   }
            df_l = pd.DataFrame(DATA, columns = ['label','color'])
            df_l['total'] = 1
            if color_map==None:
                df_l['color'] = [tuple(x) for x in df_l.color.values]
          
            df_tem_g = df_l.groupby(['label','color']).sum().reset_index().sort_values(by=['total'], ascending=True)
            df_tem_g['perc']= df_tem_g['total']/df_tem_g['total'].sum()                      
            
            fig = plt.figure(figsize=(7, 5))
            
            x = df_tem_g.label.tolist()
            y = df_tem_g.total.tolist()         
            colors_g = df_tem_g.color.tolist()
            print(colors_g)
            plt.barh(x, y,color=colors_g)

            plt.xlabel("Total", fontsize="x-large")
            plt.ylabel("Grupos", fontsize="x-large")

            for index, value in enumerate(y):
                plt.text(value, index, "  "+str(value)+" ", fontsize=15)
            
            #plt.hist(labels, bins=n_clusters)
            plt.show() 
            
            fig = plt.figure(figsize=(8, 6))
            fig1, ax1 = plt.subplots()
            fig1 = plt.figure(figsize=(8, 6))
            wedges, texts, autotexts =  ax1.pie(df_tem_g['perc'].tolist(),labels=x, autopct='%1.1f%%',
                    shadow=True, startangle=90,colors=colors_g,textprops=dict(color="w"))
            plt.setp(autotexts, size=12, weight="bold")
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            plt.show()

            
        
            print("Frecuencia : ")
            print("*********************************************************************************")
            cluster , frecuency = np.unique(labels, return_counts=True)
            cls_fre = zip(cluster,frecuency)
            for i in cls_fre:    
                print("[",i[0],"-",i[1],"]", end = ", ") 
            
        #return df_l

        if(progreso_score):
            #buscando numero de cluster ideal
            X_=data_vector
            scores = []
            scores_silueta = []           
            for k in range (start, limit,step):
                if(cluster_model=='KMeans'): 
                    kmeans = KMeans(n_clusters= k, max_iter=200, n_init=100).fit(X_)
                    score = kmeans.score(X_)
                    scores.append((k,score))
                    ssc= silhouette_score(X_, labels=kmeans.predict(X_))
                    scores_silueta.append((k,ssc)) 
                if(cluster_model=='SpectralClustering'): 
                    labels_=SpectralClustering(n_clusters= k, affinity='nearest_neighbors').fit_predict(data_vector)
                    ssc= silhouette_score(X_, labels=labels_)
                    scores_silueta.append((k,ssc))
                
            scores = np.array(scores)
            scores_silueta = np.array(scores_silueta)

            fig = plt.figure(figsize=(18, 5))
            ax1 = fig.add_subplot(121)
            plt.title('Progreso de scores_silueta')
            plt.plot(scores_silueta[:,0], scores_silueta[:,1],  marker='o')
            
            if(cluster_model=='KMeans'):
                ax2 = fig.add_subplot(122)
                plt.title('Elbow Curve')
                plt.plot(scores[:,0], scores[:,1],  marker='o') 

            plt.show()           

        ssc= silhouette_score(data_vector, labels=labels)    
        print("silhouette_score : "+str(ssc))
            
        if return_silhouette_score:
            return ssc
        else:       
            return labels_names

    

    
    
    
def plot_cluster(X=None,range_n_clusters=[],clusterer=None,cluster_labels=[],color_map=None):
    colors = []
    for n_clusters in range_n_clusters:
        # Create a subplot with 1 row and 2 columns
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.set_size_inches(18, 7)

        # The 1st subplot is the silhouette plot
        # The silhouette coefficient can range from -1, 1 but in this example all
        # lie within [-0.1, 1]
        ax1.set_xlim([-0.1, 1])
        # The (n_clusters+1)*10 is for inserting blank space between silhouette
        # plots of individual clusters, to demarcate them clearly.
        ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

        # Initialize the clusterer with n_clusters value and a random generator
        # seed of 10 for reproducibility.
        ###clusterer = KMeans(n_clusters=n_clusters, random_state=10)
        ###cluster_labels = clusterer.fit_predict(X)

        # The silhouette_score gives the average value for all the samples.
        # This gives a perspective into the density and separation of the formed
        # clusters
        silhouette_avg = silhouette_score(X, cluster_labels)
        print("For n_clusters =", n_clusters,
              "The average silhouette_score is :", silhouette_avg)

        # Compute the silhouette scores for each sample
        sample_silhouette_values = silhouette_samples(X, cluster_labels)

        y_lower = 10
        for i in range(n_clusters):
            # Aggregate the silhouette scores for samples belonging to
            # cluster i, and sort them
            ith_cluster_silhouette_values = \
                sample_silhouette_values[cluster_labels == i]

            ith_cluster_silhouette_values.sort()

            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i
            
            if color_map == None:
                color = cm.nipy_spectral(float(i) / n_clusters)
            else:
                color = color_map[i]
                
            ax1.fill_betweenx(np.arange(y_lower, y_upper),
                              0, ith_cluster_silhouette_values,
                              facecolor=color, edgecolor=color, alpha=0.7)

            # Label the silhouette plots with their cluster numbers at the middle
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            # Compute the new y_lower for next plot
            y_lower = y_upper + 10  # 10 for the 0 samples

        ax1.set_title("The silhouette plot for the various clusters.")
        ax1.set_xlabel("The silhouette coefficient values")
        ax1.set_ylabel("Cluster label")

        # The vertical line for average silhouette score of all the values
        ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

        ax1.set_yticks([])  # Clear the yaxis labels / ticks
        ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

        if color_map == None:
            # 2nd Plot showing the actual clusters formed
            colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
        else:
            colors = list(map(color_map.get, cluster_labels))
        
        ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
                    c=colors, edgecolor='k')

        # Labeling the clusters
        centers = clusterer.cluster_centers_
        #print(centers)
        # Draw white circles at cluster centers
        ax2.scatter(centers[:, 0], centers[:, 1], marker='o', c="white", alpha=1, s=200, edgecolor='k')

        for i, c in enumerate(centers):
            ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
                        s=50, edgecolor='k')

        ax2.set_title("The visualization of the clustered data.")
        ax2.set_xlabel("Feature space for the 1st feature")
        ax2.set_ylabel("Feature space for the 2nd feature")

        plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
                      "with n_clusters = %d" % n_clusters),
                     fontsize=14, fontweight='bold')

    plt.show()
    return colors