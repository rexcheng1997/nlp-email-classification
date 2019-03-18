'''
    Functions that help draw the results.
'''

import pandas, numpy
import matplotlib.pyplot as plot

def top_tfidf_feats(row, features, topN=20):
    topIDs = numpy.argsort(row)[::-1][:topN]
    topFeats = [(features[i], row[i]) for i in topIDs]
    df = pandas.DataFrame(topFeats, columns=["features", "score"])
    return df

def top_feats_in_msg(X, features, rowID, topN=25):
    row = numpy.squeeze(X[rowID].toarray())
    return top_tfidf_feats(row, features, topN)

def top_mean_feats(X, features, groupIDs=None, minTfidf=0.1, topN=25):
    if groupIDs:
        D = X[groupIDs].toarray()
    else:
        D = X.toarray()

    D[D < minTfidf] = 0
    tfidfMeans = numpy.mean(D, axis=0)
    return top_tfidf_feats(tfidfMeans, features, topN)

def top_feats_per_cluster(X, y, features, minTfidf=0.1, topN=25):
    dfs = []
    labels = numpy.unique(y)
    for label in labels:
        ids = numpy.where(y==label)
        featsDf = top_mean_feats(X, features, ids, minTfidf=minTfidf, topN=topN)
        featsDf.label = label
        dfs.append(featsDf)
    return dfs

def plot_tfidf(dfs):
    fig = plot.figure(figsize=(12, 9), facecolor='w')
    x = numpy.arange(len(dfs[0]))
    for i, df in enumerate(dfs):
        ax = fig.add_subplot(1, len(dfs), i + 1)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_frame_on(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.set_xlabel("Tf-Idf Score", labelpad=16, fontsize=14)
        ax.set_title("Cluster = " + str(df.label), fontsize=16)
        ax.ticklabel_format(axis='x', style="sci", scilimits=(-2,2))
        ax.barh(x, df.score, align="center", color="#7530FF")
        ax.set_yticks(x)
        ax.set_ylim([-1, x[-1]+1])
        yticks = ax.set_yticklabels(df.features)
        plot.subplots_adjust(bottom=0.09, right=0.97, left=0.15, top=0.95, wspace=0.52)
    plot.show()
