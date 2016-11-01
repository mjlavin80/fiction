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

def save_labels(sklearn_instance, filename, _ids, genres, years):
    labels = sklearn_instance.labels_
    #At end of loop, order by count, stop at 10k
    groupings = zip(_ids, labels, genres, years)
    #convert to pandas df (terms and counts)
    df = pd.DataFrame(groupings, columns=["docid", "group_label", "genres", "year"])
    #Save as csv in lavin_results folder
    df.to_csv("lavin_results/" + filename)

stops = corpus.stopwords.words('english')
# load features
feature_df = pd.read_csv("lavin_lexicon/features_all.csv")
features_all = [i for i in list(feature_df["term"]) if i not in stops]
features = features_all[:9000]

conn = pymysql.connect(host='localhost', port=3306, user=USER, passwd=PWD, db='horror')
cur = conn.cursor()

from application.pickles import pickledData

pData = pickledData()
_ids_dates_genres = pData._ids_dates_genres
_ids = pData._ids
dates = pData.dates
genres = pData.genres
feature_dicts = pData.feature_dicts

# create vectors using N top features not in stops
tfidf = TfidfTransformer()
vec = DictVectorizer()
vect = vec.fit_transform(feature_dicts)
adjusted = tfidf.fit_transform(vect)
data = adjusted.toarray()

bandwidth= .89
ms = MeanShift(bandwidth=bandwidth, bin_seeding=False)
ms.fit(data)
save_labels(ms, "meanshift_all_no_bin_seeding.csv", _ids, genres, years)

bandwidth2 = estimate_bandwidth(data, quantile=0.2, n_samples=400)
ms2 = MeanShift(bandwidth=bandwidth2, bin_seeding=True)
ms2.fit(data)
save_labels(ms2, "meanshift_all_w_bin_seeding.csv", _ids, genres, years)


# affinity all
af = AffinityPropagation().fit(data)
save_labels(af, "affinity_all.csv", _ids, genres, years)

# mini batch k-means all
mbkm = MiniBatchKMeans().fit(data)
save_labels(mbkm, "mini_batch_km_all.csv", _ids, genres, years)

# hierarchical all
wc = AgglomerativeClustering(linkage="ward", n_clusters=10).fit(data)
save_labels(wc, "ward_hierarchical_all.csv", _ids, genres, years)

wc2 = AgglomerativeClustering(linkage="average", n_clusters=10).fit(data)
save_labels(wc2, "avg_hierarchical_all.csv", _ids, genres, years)

wc3 = AgglomerativeClustering(linkage="complete", n_clusters=10).fit(data)
save_labels(wc3, "complete_hierarchical_all.csv", _ids, genres, years)

#get ids of horror using biggenre table
sg = ["locghost", "lochorror", "pbgothic", "stangothic", "chihorror"]
horror_ids = [int(h_object.work_id) for h_object in db.session.query(Genres).filter(or_(Genres.genre == sg[0], Genres.genre == sg[1], Genres.genre == sg[2], Genres.genre == sg[3], Genres.genre == sg[4] )).all()]
horror_ids = sorted(set(horror_ids))

horror_genres = []
horror_years = []

#define feature_dicts_horror, a list of dictionaries
feature_dicts_horror = []
for position, feature_dict in enumerate(feature_dicts):
    if position+1 in horror_ids:
        feature_dicts_horror.append(feature_dict)
        horror_genres.append(genres[position])
        horror_years.append(years[position])

tfidf_horror = TfidfTransformer()
vec_horror = DictVectorizer()
#horror_vect
horror_vect = vec_horror.fit_transform(feature_dicts_horror)
#horror_adjusted
horror_adjusted = tfidf.fit_transform(horror_vect)
#horror_data
horror_data = horror_adjusted.toarray()

# meanshift on just horror
# the following bandwidth can be automatically detected using
horror_bandwidth = estimate_bandwidth(horror_data, quantile=0.2, n_samples=150)
ms = MeanShift(bandwidth=horror_bandwidth, bin_seeding=False)
ms.fit(horror_data)
save_labels(ms, "meanshift_horror_no_seeding.csv", horror_ids, horror_genres, horror_years)

# affinity just horror
af = AffinityPropagation().fit(horror_data)
save_labels(af, "affinity_horror.csv", horror_ids, horror_genres, horror_years)

# mini batch k-means horror
mbkm = MiniBatchKMeans().fit(horror_data)
save_labels(mbkm, "mini_batch_km_horror.csv", horror_ids, horror_genres, horror_years)

# hierarchical horror
wc = AgglomerativeClustering(linkage="ward", n_clusters=5).fit(horror_data)
save_labels(wc, "ward_hierarchical_horror.csv", horror_ids, horror_genres, horror_years)

wc2 = AgglomerativeClustering(linkage="average", n_clusters=5).fit(horror_data)
save_labels(wc2, "avg_hierarchical_horror.csv", horror_ids, horror_genres, horror_years)

wc3 = AgglomerativeClustering(linkage="complete", n_clusters=5).fit(horror_data)
save_labels(wc3, "complete_hierarchical_horror.csv", horror_ids, horror_genres, horror_years)
