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
from scipy.stats.stats import pearsonr
import pickle
from application.pickles import pickledData

pData = pickledData()
_ids_dates_genres = pData._ids_dates_genres
_ids = pData._ids
dates = pData.dates
genres = pData.genres

feature_dicts = pData.feature_dicts

#convert to tf-idf model
tfidf = TfidfTransformer()
vec = DictVectorizer()
vect = vec.fit_transform(feature_dicts)
adjusted = tfidf.fit_transform(vect)

term_indices = list(vec.vocabulary_.items())
#alphabetical order
term_indices.sort(key=operator.itemgetter(1))

term_list = [i[0] for i in term_indices]
data = adjusted.toarray()

p_tuples = []

for column in data.T:
   p, c = pearsonr(column, dates)
   f_tuple = (p,c)
   p_tuples.append(f_tuple)

print(len(term_list), len(p_tuples))
final_tuples = list(zip(term_list, [i[0] for i in p_tuples], [i[1] for i in p_tuples]))
#convert to pandas df
df = pd.DataFrame(final_tuples, columns=["term", "pearson", "p_value"])

#Save as csv in lavin_lexicon folder
df.to_csv("lavin_lexicon/features_correlation_with_pubdate.csv")
