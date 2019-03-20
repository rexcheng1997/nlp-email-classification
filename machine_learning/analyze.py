'''
    Taking a pandas DataFrame and analyze the data through machine learning.
'''

__author__ = "rexcheng"

import numpy
from .draw import *
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.cluster import KMeans

def analyze(df):
    stopWords = ENGLISH_STOP_WORDS.union(["ees", "com", "et", "hou", "ect", "-e-"])
    vect = TfidfVectorizer(analyzer='word', stop_words=stopWords, max_df=0.9, min_df=2)
    X = vect.fit_transform(df.words)
    features = vect.get_feature_names()
    print(top_feats_in_msg(X, features, 1, 10))
    print(top_mean_feats(X, features, None, 0.1, 10))
    clf = KMeans(n_clusters=3, max_iter=100, init="k-means++", n_init=1)
    labels = clf.fit_predict(X)
    plot_tfidf(top_feats_per_cluster(X, labels, features, 0.1, 25))
