def divide_by_three(list_of_pairs):
    for_features = {}
    test = {}
    train = {}
    destinations = [for_features, test, train]
    while len(list_of_pairs) > 2 or len(list_of_pairs) % 3 == 0:
        #grab a random id from big_genre and remove
        for m, l in enumerate(destinations):

            candidates = list(list_of_pairs.keys())
            shuffle(candidates)
            key = candidates[0]
            #print(key)
            candidate = list_of_pairs[key]
            #remove from dictionary
            del list_of_pairs[key]
            #make sure the author is not in the dict
            if candidate not in l:
                l[key] = candidate

            else:
                next_one = destinations[m+1]
                #next list same id if author in dict
                if candidate not in next_one:
                    next_one[key] = candidate
                else:
                    next_one = destinations[m+2]
                    if candidate not in next_one:
                        next_one[key] = candidate
    destinations_trimmed =[]
    for i,j in enumerate(destinations):
        aTuple = list(j.items())
        shuffle(aTuple)
        destinations_trimmed.append(dict(aTuple[:83]))
    return destinations_trimmed

from random import shuffle
from application.selective_features import dictionaries_of_features, make_genres_big
from application.pickles import pickledData
import pandas as pd
from scipy.stats.stats import spearmanr
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import DictVectorizer


pData = pickledData()

# define as a function, supply a big_genre
def partition_features_test_train(big_genre, pData):
    # Local variables. All are ordered by mysql _id field, which is also the original order of finalmeta.csv
    _ids = pData._ids
    dates = pData.dates
    genres = pData.genres
    #needs conversion
    big_genres = make_genres_big(genres)
    authors = pData.authors
    feature_dicts = pData.feature_dicts

    # get all ids for big_genre
    big_genre_ids_and_author = {}
    other_ids_and_author = {}
    for i, j in enumerate(big_genres):
         #print(i, _ids[i], j)
         if j == big_genre:
             big_genre_ids_and_author[_ids[i]] = authors[i]
         else:
             other_ids_and_author[_ids[i]] = authors[i]

    # shuffle big_genre_tuples and "deal out" randomly like deck of cards into three, starting with author repeats
    in_genre = divide_by_three(big_genre_ids_and_author)
    # do same for other_ids
    non_genre = divide_by_three(other_ids_and_author)
    combined_partitions_ids = []
    combined_partitions_binary_genres = []
    for f,g in enumerate(in_genre):
        combined = list(g.keys())+list(non_genre[f].keys())
        shuffle(combined)
        genre_processor = []
        for i in combined:
            if i in list(g.keys()):
                genre_processor.append(1)
            else:
                genre_processor.append(1)
        combined_partitions_binary_genres.append(genre_processor)
        combined_partitions_ids.append(combined)
    return combined_partitions_ids, combined_partitions_binary_genres

combined_partitions_ids, combined_partitions_binary_genres = partition_features_test_train("crime", pData)

#convert lists of ids into dictionaries of features in order of ids

print(pData.feature_dicts[983])
print(max(combined_partitions_ids[0]))
print(max(combined_partitions_ids[1]))
print(max(combined_partitions_ids[2]))



feature_select_dicts = [pData.feature_dicts[d-1] for d in combined_partitions_ids[0]]
test_dicts = pData.feature_dicts = [pData.feature_dicts[d-1] for d in combined_partitions_ids[1]]
train_dicts = pData.feature_dicts = [pData.feature_dicts[d-1] for d in combined_partitions_ids[2]]

binary_genres = combined_partitions_binary_genres[0]
## Begin function block

#convert to tf-idf model
tfidf = TfidfTransformer()
vec = DictVectorizer()
vect = vec.fit_transform(feature_select_dicts)
adjusted = tfidf.fit_transform(vect)

term_indices = list(vec.vocabulary_.items())
#alphabetical order
term_indices.sort(key=operator.itemgetter(1))

term_list = [i[0] for i in term_indices]
data = adjusted.toarray()

p_tuples = []

for column in data.T:
   p, c = spearmanr(column, binary_genres)
   f_tuple = (p,c)
   p_tuples.append(f_tuple)

# zip back together with term_list
#print(len(term_list), len(p_tuples))
final_tuples = list(zip(term_list, [i[0] for i in p_tuples], [i[1] for i in p_tuples]))

print(final_tuples)
## end function block
##
##

# build feature list using sorted p_tuples
selected_feature_list = []

# process test and train dicts to include only chosen features
# result = dictionaries_of_features(feature_dicts, genre_features)

text_clf = Pipeline([('vect', DictVectorizer()), ('tfidf', TfidfTransformer()),('clf', LogisticRegression()),])
