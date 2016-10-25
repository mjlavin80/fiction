import operator
from application import db
from application.models import *
import pymysql
from collections import Counter
from config import USER, PWD
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
import pickle
import urllib

try:
    _ids = pickle.load( open( "pickled_data/ids.p", "rb" ) )
except:
    # get ids, store order here
    _ids  = [i.id for i in db.session.query(Metadata).all()]
    pickle.dump( _ids, open( "pickled_data/ids.p", "wb" ) )

try:
    _ids = pickle.load( open( "pickled_data/ids_dates_genres.p", "rb" ) )
except:
    # get ids, store order here
    _ids_dates_genres  = [i.id, i.firstpub, urllib.unquote_plus(i.genres) for i in db.session.query(Metadata).all()]
    pickle.dump( _ids, open( "pickled_data/ids_dates_genres.p", "wb" ) )

#load feature dict from pickle
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


#convert to tf-idf model
tfidf = TfidfTransformer()
vec = DictVectorizer()
vect = vec.fit_transform(feature_dicts)
adjusted = tfidf.fit_transform(vect)

term_indices = list(vec.vocabulary_.items())
term_indices.sort(key=operator.itemgetter(1))
term_list = [i[0] for i in term_indices]

#get all dates


#get all tfidf scores for word in same order as dates list

#p, c = pearsonr(term_freqs,dates)
#append to final_tuples


#convert to pandas df
#df = pd.DataFrame(final_tuples, columns=["term", "docs", "pearson", "confidence"])

#Save as csv in lavin_lexicon folder
#df.to_csv("lavin_lexicon/features_correlated_with_pubdate.csv")
