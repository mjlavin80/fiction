import sys, os
sys.path.insert(0, os.path.abspath('..'))

#get feature dicts from .p file
from application.pickles import pickledData

pData = pickledData()
_ids_dates_genres = pData._ids_dates_genres
_ids = pData._ids
dates = pData.dates
genres = pData.genres
feature_dicts = pData.feature_dicts

from application.selective_features import make_feature_list, dictionaries_without_features, dictionaries_of_features

top_genre_terms = make_feature_list("../lavin_lexicon/features_correlation_with_genre_all.csv", "spearman", 500)
#print(top_genre_terms)
top_year_terms = make_feature_list("../lavin_lexicon/features_correlation_with_pubdate_all.csv", "pearson", 5500)
#print(top_year_terms)

#run dictionaries of features
new_feature_dicts = dictionaries_of_features(feature_dicts, top_genre_terms)
print("Done making feature list")

#run dictionaries without features
revised_feature_dicts = dictionaries_without_features(new_feature_dicts, top_year_terms)

from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd


# create vectors using N top features not in stops
tfidf = TfidfTransformer()
vec = DictVectorizer()
vect = vec.fit_transform(new_feature_dicts)
adjusted = tfidf.fit_transform(vect)
data = adjusted.toarray()
print(len(data[0]))
