from nltk import corpus
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth, AffinityPropagation, MiniBatchKMeans, AgglomerativeClustering
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
import pickle
from application import db
from application.models import *
import pymysql
from collections import Counter
from config import USER, PWD
from sqlalchemy import or_

from application.output import save_labels
from application.pickles import pickledData

pData = pickledData()

feature_dicts = pData.feature_dicts

#define a dictionary with ids, genres, dates, authors, etc. Pass to each function
metadata = {"ids": pData._ids, "dates": pData.dates, "genres":pData.genres, "authors":pData.authors,
                "titles":pData.titles,"big_genres":pData.big_genres, "lavin_genres":pData.lavin_genres}
#convert all metadata to dataframe
data = [metadata[i] for i in metadata.keys()]
df = pd.DataFrame(data)
df = df.transpose()
df.index.name = 'position'
df.columns=metadata.keys()

#select by genre, loop position to define feature_dicts_horror
df_horror = df.loc[df['big_genres'] == "gothic"]
horror_indices = list(df_horror.index)
horror_feature_dicts = []
for position in horror_indices:
    horror_feature_dicts.append(feature_dicts[position])

from application.selective_features import make_feature_list, dictionaries_of_features

top_genre_terms = make_feature_list("lavin_lexicon/features_correlation_with_genre_all.csv", "spearman", 100)
new_feature_dicts = dictionaries_of_features(feature_dicts, top_genre_terms)
print("Done making feature list")

# create vectors using N top features not in stops
tfidf = TfidfTransformer()
vec = DictVectorizer()
vect = vec.fit_transform(new_feature_dicts)
adjusted = tfidf.fit_transform(vect)
data = adjusted.toarray()

bandwidth= estimate_bandwidth(data, quantile=0.2, n_samples=400)
ms = MeanShift(bandwidth=bandwidth, bin_seeding=False)
ms.fit(data)
save_labels(ms, "meanshift_all_no_bin_seeding_genre_features_100.csv", df)

bandwidth2 = estimate_bandwidth(data, quantile=0.2, n_samples=400)
ms2 = MeanShift(bandwidth=bandwidth2, bin_seeding=True)
ms2.fit(data)
save_labels(ms2, "meanshift_all_w_bin_seeding_genre_features_100.csv", df)

# affinity all
af = AffinityPropagation().fit(data)
save_labels(af, "affinity_all_genre_features_100.csv", df)

# mini batch k-means all
mbkm = MiniBatchKMeans().fit(data)
save_labels(mbkm, "mini_batch_km_all_genre_features_100.csv", df)

# hierarchical all
wc = AgglomerativeClustering(linkage="ward", n_clusters=10).fit(data)
save_labels(wc, "ward_hierarchical_all_genre_features_100.csv", df)

wc2 = AgglomerativeClustering(linkage="average", n_clusters=10).fit(data)
save_labels(wc2, "avg_hierarchical_all_genre_features_100.csv", df)

wc3 = AgglomerativeClustering(linkage="complete", n_clusters=10).fit(data)
save_labels(wc3, "complete_hierarchical_all_genre_features_100.csv", df)


new_feature_dicts_horror = dictionaries_of_features(horror_feature_dicts, top_genre_terms)

tfidf_horror = TfidfTransformer()
vec_horror = DictVectorizer()
#horror_vect
horror_vect = vec_horror.fit_transform(new_feature_dicts_horror)
#horror_adjusted
horror_adjusted = tfidf_horror.fit_transform(horror_vect)
#horror_data
horror_data = horror_adjusted.toarray()

# meanshift on just horror
# the following bandwidth can be automatically detected using
horror_bandwidth = estimate_bandwidth(horror_data, quantile=0.2, n_samples=150)
ms = MeanShift(bandwidth=horror_bandwidth, bin_seeding=False)
ms.fit(horror_data)
save_labels(ms, "meanshift_horror_no_seeding_genre_features_100.csv", df_horror)

# affinity just horror
af = AffinityPropagation().fit(horror_data)
save_labels(af, "affinity_horror_genre_features_100.csv", df_horror)

# mini batch k-means horror
mbkm = MiniBatchKMeans().fit(horror_data)
save_labels(mbkm, "mini_batch_km_horror_genre_features_100.csv", df_horror)

# hierarchical horror
wc = AgglomerativeClustering(linkage="ward", n_clusters=5).fit(horror_data)
save_labels(wc, "ward_hierarchical_horror_genre_features_100.csv", df_horror)

wc2 = AgglomerativeClustering(linkage="average", n_clusters=5).fit(horror_data)
save_labels(wc2, "avg_hierarchical_horror_genre_features_100.csv", df_horror)

wc3 = AgglomerativeClustering(linkage="complete", n_clusters=5).fit(horror_data)
save_labels(wc3, "complete_hierarchical_horror_genre_features_100.csv", df_horror)
