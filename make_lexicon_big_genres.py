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
from scipy.stats.stats import spearmanr
import pickle
from application.pickles import pickledData

pData = pickledData()
_ids_dates_genres = pData._ids_dates_genres
_ids = pData._ids
dates = pData.dates
genres = pData.genres

def make_genres_big(piped_genres):
    big_genres = pd.read_csv("meta/datadictionary.csv")
    gen_dict = {}
    for i in big_genres.itertuples():
        gen_dict[i[1]] = i[2]
    gen_dict["chimyst"] = "crime"
    gen_dict["locghost"] = "gothic"
    gen_dict["lockandkey"] = "crime"
    big_genres = []

    for i in piped_genres:
        gen = i.split(" | ")
        g = []
        for z in gen:
            if z != "teamred" and z!= "teamblack" and z!= "stew" and z != "juvenile" and z != "drop" and "random" not in z:
                #look up and append big genre
                try:
                    g.append(gen_dict[z])
                except:
                    pass

        #merge duplicates
        g = list(set(g))
        #assign as multi if still mutiple genres
        if len(g) > 1:
            final_genre = "multi"
        #assign as non_genre if no genres left
        if len(g) == 0:
            final_genre = "non_genre"
        #keep biggenre if length of list is 1
        if len(g) == 1:
            final_genre = g[0]
        big_genres.append(final_genre)
    return big_genres

big_genres = make_genres_big(genres)

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
   p, c = spearmanr(column, big_genres)
   f_tuple = (p,c)
   p_tuples.append(f_tuple)

#print(len(term_list), len(p_tuples))
final_tuples = list(zip(term_list, [i[0] for i in p_tuples], [i[1] for i in p_tuples]))
#convert to pandas df
df = pd.DataFrame(final_tuples, columns=["term", "spearman", "p_value"])

#Save as csv in lavin_lexicon folder
df.to_csv("lavin_lexicon/features_correlation_with_genre.csv")
