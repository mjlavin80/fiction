from nltk import corpus
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
import pickle

stops = corpus.stopwords.words('english')
# load features
feature_df = pd.read_csv("lavin_lexicon/features_all.csv")
features_all = [i for i in list(feature_df["term"]) if i not in stops]
features = features_all[:9000]

from application import db
from application.models import *
import pymysql
from collections import Counter
from config import USER, PWD
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user=USER, passwd=PWD, db='horror')
cur = conn.cursor()

try:
    _ids = pickle.load( open( "pickled_data/ids.p", "rb" ) )
except:
    # get ids, store order here
    _ids  = [i.id for i in db.session.query(Metadata).all()]
    pickle.dump( _ids, open( "pickled_data/ids.p", "wb" ) )

try:
    feature_dicts = pickle.load( open( "pickled_data/feature_dicts.p", "rb" ) )
    print("Loaded pickle data successfully.")

except:
    print("Did not find feature data in pickle form. Creating pickle for future use.")
    feature_dicts = []

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

    print("Finished making dictionaries")
    pickle.dump( feature_dicts, open( "pickled_data/feature_dicts.p", "wb" ) )
    cur.close()
    conn.close()

# create vectors using N top features not in stops
tfidf = TfidfTransformer()
vec = DictVectorizer()
vect = vec.fit_transform(feature_dicts)
adjusted = tfidf.fit_transform(vect)
data = adjusted.toarray()

# the following bandwidth can be automatically detected using
#bandwidth = estimate_bandwidth(data, quantile=0.2, n_samples=900)
bandwidth = .800652837213
#print(bandwidth)

#ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms = MeanShift(bandwidth=bandwidth, bin_seeding=False)
ms.fit(data)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

#print(labels)
print("number of estimated clusters : %d" % n_clusters_)

#join with genres and years
genres =[]
years = []

for _id in _ids:
    #get genres and years
    year = db.session.query(Metadata).filter(Metadata.id==_id).one().firstpub
    genre_rows  = [i.genre for i in db.session.query(Genres).filter(Genres.work_id==_id).all()]
    #mush genres to string
    g = " | ".join(genre_rows)
    #append
    genres.append(g)
    years.append(year)
#Store results for graphing
#At end of loop, order by count, stop at 10k
groupings = zip(_ids, labels, genres, years)

#convert to pandas df (terms and counts)
df = pd.DataFrame(groupings, columns=["docid", "group_label", "genres", "year"])

#Save as csv in lavin_lexicon folder
#df.to_csv("lavin_results/meanshift_all_bin_w_seeding.csv")
df.to_csv("lavin_results/meanshift_all_no_seeding.csv")
