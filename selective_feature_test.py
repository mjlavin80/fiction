from application.selective_features import dictionaries_of_features
from application.pickles import pickledData

pData = pickledData()
_ids_dates_genres = pData._ids_dates_genres
_ids = pData._ids
dates = pData.dates
genres = pData.genres
feature_dicts = pData.feature_dicts

#test with one word
result = dictionaries_of_features(feature_dicts, ["could",])
print(result)
#it works!
