
from nltk import corpus
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd

stops = corpus.stopwords.words('english') 
# load features
feature_df = pd.read_csv("lavin_lexicon/features_all.csv")
features_all = [i for i in list(feature_df["term"]) if i not in stops]
features = features_all[:500]

from application import db
from application.models import *
import pymysql
from collections import Counter
from config import USER, PWD
import pymysql

# loop ids, store order here
_ids  = [i.id for i in db.session.query(Metadata).all()]

feature_dicts = []

conn = pymysql.connect(host='localhost', port=3306, user=USER, passwd=PWD, db='horror')
cur = conn.cursor()

for _id in _ids:
    feature_dict = {}
    # get types and counts
    query = "".join(["SELECT type, type_count FROM counts WHERE work_id=", str(_id), " AND type REGEXP '^[A-Za-z]+$';"])
    #loop terms matching certain criteria (regex query)
    a = cur.execute(query)
    for row in cur:
        #add to dict if ok to use
        if row[0] in features:
            feature_dict[row[0]] = row[1]
    feature_dicts.append(feature_dict)
        
# create vectors using N top features not in stops
tfidf = TfidfTransformer()
vec = DictVectorizer()
vect = vec.fit_transform(feature_dicts)
adjusted = tfidf.fit_transform(vect)
data = adjusted.toarray()

# the following bandwidth can be automatically detected using
bandwidth = estimate_bandwidth(data, quantile=0.2, n_samples=200)

ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(data)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

print(labels)
print("number of estimated clusters : %d" % n_clusters_)

cur.close()
conn.close()
#Store results for graphing

