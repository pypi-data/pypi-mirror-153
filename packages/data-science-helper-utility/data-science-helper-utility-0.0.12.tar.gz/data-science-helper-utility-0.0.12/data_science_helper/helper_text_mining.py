import matplotlib.pylab as plt

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
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
#from googletrans import Translator
import string
from nltk.stem.snowball import SnowballStemmer
import nltk 
from sklearn.metrics import silhouette_score
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import SpectralClustering
from scipy.stats import itemfreq

import pandas as pd

random_state = 0 
trans_table = {ord(c): None for c in string.punctuation + string.digits}  
stemmer=SnowballStemmer("spanish", ignore_stopwords=True)

_stopwords_news = [] 
spanish_stopwords = stopwords.words("spanish")+ _stopwords_news



sinonimos_nan = ['', 'aab', 'amenz', 'aplic', 'c', 'conoc', 'contempl', 'd',
                   'detect', 'empres crecimient present debil', 'encontr',
                   'encontr debil present propuest', 'encuentr', 'feb', 'fen',
                   'garantiz', 'identif', 'identific', 'minim', 'moment',
                   'moment ningun', 'muestr', 'n', 'nb', 'nigun', 'ningun',
                   'ningun principal comercializ tel ciudadclient nuev todavi gener debil',
                   'observ', 'observ ningun', 'observ unidad', 'oficin registr', 'ok',
                   'percib', 'present debil', 'present debil aparent', 'registr',
                   'ubic', 'v', 'visualiz', 'x']



def cluster_foda(df=None,columns=[],freq_word=True,word_cloud=True,
                 embedded='TSNE',perplexity=40,cluster_model='KMeans',n_clusters=30
                 ,progreso_score=False,min_df=0.1,max_df=0.6):
    
    for column in columns:
                
        
        df_text = df.copy()
        
        clean_column = "clean_"+column
        df_text[column].replace(np.nan, value ='ninguna',inplace=True) 
        df_text[clean_column] = tokenize_column(df_text, column)
        df_text[clean_column].replace(to_replace =sinonimos_nan, value =np.nan,inplace=True) 
        
        df_text_temp = df_text.copy()        
        print("inicial: "+ str(df_text_temp.shape))   
        
        #df_text_temp[clean_column] = tokenize_column(df_text_temp, column)        
        #removiendo nulos
        
        df_text_temp.dropna(subset=[clean_column],inplace=True)          
        df_text_temp.reset_index(drop=True,inplace=True)
        print("removiendo nulos: "+ str(df_text_temp.shape))
        
        #removiendo duplicados
        df_text_temp.drop_duplicates(subset=[clean_column], keep='first', inplace=True)
        df_text_temp.reset_index(drop=True,inplace=True)
        print("removiendo duplicados: "+ str(df_text_temp.shape))
        
        X = df_text_temp[clean_column].copy()

        # for idx, item in enumerate(X):
        #     X[idx] = X[idx].splitlines()
        #     X[idx] = list(filter(None, X[idx]))

        # total = []
        # for i in X:
        #     total += i

        total = X    

        vectorizer = TfidfVectorizer(tokenizer=tokenize, analyzer="word",stop_words=spanish_stopwords,max_df=max_df, 
                                     min_df=min_df)#fit_transform(total)#todense()
        #vectorizer = CountVectorizer(tokenizer=tokenize,stop_words=spanish_stopwords)

        tdm = vectorizer.fit_transform(total)
        tfidf_vector = tdm.todense()
        freqs = {word: tdm.getcol(idx).sum() for word, idx in vectorizer.vocabulary_.items()}
        results = pd.DataFrame(tdm.toarray(), columns=vectorizer.get_feature_names())
        print ("Dimentions of tfidf_vector: ", tfidf_vector.shape)
        if(freq_word):
            for i in sorted (vectorizer.vocabulary_.items()) :  
                print(i, end = " ") 

        if(word_cloud):
            w = WordCloud(width=1600, height=800, max_font_size=200).fit_words(freqs)
            plt.figure(figsize=(18,18))
            plt.imshow(w)
            plt.axis("off")
            plt.show()    

        if(embedded=='TSNE'):
            X_embedded = TSNE(n_components=2, perplexity=perplexity, verbose=0).fit_transform(tfidf_vector) 
            #try tfidf_vector or X_reduced
            #verbose->2 para mostrar log
        else:
            pca = PCA(n_components=2, random_state=random_state)
            X_embedded = pca.fit_transform(tfidf_vector)

        print(cluster_model)
        if(cluster_model=='KMeans'):        
            clustering_model = KMeans(n_clusters=n_clusters, max_iter=200, n_init=100)
            labels = clustering_model.fit_predict(tfidf_vector)
        elif(cluster_model=='DBSCAN'):             
            clustering_model = DBSCAN().fit(tfidf_vector)
            labels = clustering_model.labels_
        elif(cluster_model=='SpectralClustering'): 
            labels=SpectralClustering(n_clusters= n_clusters, affinity='nearest_neighbors').fit_predict(tfidf_vector)
            
        fig = plt.figure(figsize=(8, 5))
        plt.hist(labels, bins=n_clusters)
        plt.show() 
        
        print("Frecuencia : ")
        print("*********************************************************************************")
        cluster , frecuency = np.unique(labels, return_counts=True)
        cls_fre = zip(cluster,frecuency)
        for i in cls_fre:    
            print("[",i[0],"-",i[1],"]", end = ", ") 

        if(progreso_score):
            #buscando numero de cluster ideal
            X_=tfidf_vector
            scores = []
            scores_silueta = []
            for k in range (2, 150,10):
                if(cluster_model=='KMeans'): 
                    kmeans = KMeans(n_clusters= k, max_iter=200, n_init=100).fit(X_)
                    score = kmeans.score(X_)
                    scores.append((k,score))
                    ssc= silhouette_score(X_, labels=kmeans.predict(X_))
                    scores_silueta.append((k,ssc)) 
                if(cluster_model=='SpectralClustering'): 
                    labels_=SpectralClustering(n_clusters= k, affinity='nearest_neighbors').fit_predict(tfidf_vector)
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

      
        fig = plt.figure(figsize=(10, 10))
        #ax = Axes3D(fig)
        ax = plt.axes(frameon=False)
        plt.setp(ax, xticks=(), yticks=())
        plt.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=0.9,
                        wspace=0.0, hspace=0.0)
        plt.scatter(X_embedded[:, 0], X_embedded[:, 1],
                c=labels, marker="x",cmap = 'tab20')
        cbar = plt.colorbar()
        cbar.set_label('Color Intensity')
        
        print("")
        print("Top terms per cluster:")        
        print("*********************************************************************************")
        order_centroids = clustering_model.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()
        for i in range(n_clusters):
            print("Cluster %d:" % i, end='')
            for ind in order_centroids[i, :10]:
                print(' %s' % terms[ind], end='')
                print()
        
        
        #ssc= silhouette_score(tfidf_vector, labels=clustering_model.predict(tfidf_vector))
        ssc= silhouette_score(tfidf_vector, labels=labels)
        
        cluster_column = 'cluster_'+column
        df_text_temp[cluster_column]=labels
        
        #df_text = pd.merge(df_text,df_text_temp[[clean_column,cluster_column,'MES','ID_CLIENTE']], 
        #left_on=['MES','ID_CLIENTE'],right_on=['MES','ID_CLIENTE'],how='left')
        df_text = pd.merge(df_text,df_text_temp[[clean_column,cluster_column]], left_on=[clean_column],right_on=[clean_column],how='left')

        
        print("silhouette_score : "+str(ssc))
        return df_text
    
def tokenize(text):
        # my text was unicode so I had to use the unicode-specific translate function. If your documents are strings, 
        #you will need to use a different `translate` function here. `Translated` here just does search-replace. 
        #See the trans_table: any matching character in the set is replaced with `None`
        tokens = [word for word in nltk.word_tokenize(text.translate(trans_table)) if len(word) > 1] #if len(word) > 1 
        #because I only want to retain words that are at least two characters before stemming, 
        #although I can't think of any such words that are not also stopwords
        stems = [stemmer.stem(item) for item in tokens]
        return stems
    
    
    
def tokenize_column(df, column_name):    
    return (df[column_name]
            .apply(lambda row: nltk.word_tokenize(row))
            .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))
            .apply(lambda tokens_list: list(map(lambda token: token.lower(), tokens_list)))
            .apply(lambda word_list: list(filter(lambda word: word not in spanish_stopwords, word_list)))
            .apply(lambda tokens_list_stem: list(map(lambda token: stemmer.stem(token), tokens_list_stem)))
            .apply(lambda tokens_valid_list_stem: ' '.join(tokens_valid_list_stem)))



def total_words(df, column_name):
    return (df
        .dropna() # eliminamos los NaN en caso que aún los haya
        .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1) # tokenizamos nuestra columna
        .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens))) # del todas las palabras que no sean alfanuméricas
        .apply(lambda tokens_list: list(map(lambda token: token.lower(), tokens_list))) # conv tk a L_c to comp. correct. con sw
        .apply(lambda word_list: list(filter(lambda word: word not in spanish_stopwords, word_list))) # del palabras dentro de s_w
        .apply(lambda valid_word_list: len(valid_word_list)) # obtenemos cuántas palabras son
    )


def total_caracteres(df, column_name):
    return (df
        .dropna() # eliminamos los NaN en caso que aún los haya
        .apply(lambda row: row[column_name].lower()) # convertir tokens a lower_case para compararlas correctamente con stopwords
        
    )