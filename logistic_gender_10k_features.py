from random import shuffle
from application.selective_features import make_feature_list, dictionaries_of_features, make_genres_big_and_lavin
from application.pickles import pickledData
import pandas as pd
from scipy.stats.stats import spearmanr
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.metrics import recall_score

# all this has to do is split a list of ids into three groups
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def divide_by_three(list_of_ids):
    destinations = []
    while len(list_of_ids) > 2 or len(list_of_pairs) % 3 == 0:
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

def divide_list(mylist, number_of_splits):
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    l = (len(mylist) % number_of_splits)
    a = len(mylist) - l
    b = int(a/number_of_splits)
    newlists = list(chunks(mylist, b))
    newlists = [i for i in newlists if len(i) == b]
    return newlists

#this will be moved to application folder
def partition_test_train(genre, df, number_of_partitions):
    # supply a genre
    df_genre = df.loc[df['big_genres'] == genre]
    df_non_genre = df.loc[df['big_genres'] != genre ]
    df_non_genre = df_non_genre.loc[df_non_genre['big_genres'] != "multi" ]
    # create a dataset of random ids 50% in genre, 50% out of genre
    genre_ids = list(df_genre['ids'])
    # split into three separate sets of ids
    genre_split = divide_list(genre_ids, number_of_partitions)

    non_genre_ids = list(df_non_genre['ids'])
    #shuffle non_genre before splitting
    shuffle(non_genre_ids)
    non_genre_ids = non_genre_ids[0:len(genre_ids)]
    # split into three separate sets of ids
    non_genre_split = divide_list(non_genre_ids, number_of_partitions)

    rejoined = []
    #rejoin genre and nongenre

    for i, j in enumerate(non_genre_split):
        joined = j + genre_split[i]
        rejoined.append(joined)
    #sort by id and convert rejoined back to full df
    for r in rejoined:
        r.sort()
    rejoined_dfs = []
    for i in rejoined:
        new_df = df.loc[df['ids'].isin(i)]
        rejoined_dfs.append(new_df)
    return rejoined_dfs, rejoined

pData = pickledData()

# import feature dictionaries
feature_dicts_full = pData.feature_dicts

photo_terms = make_feature_list("lavin_lexicon/photo_terms.csv", "score", 8)

#perform feature selection on dictionaries of term frequencies, using top 100 photo_terms
feature_dicts = dictionaries_of_features(feature_dicts_full, photo_terms)

#define a dictionary with ids, genres, dates, authors, etc. Pass to each function
metadata = {"ids": pData._ids, "dates": pData.dates, "genres":pData.genres, "authors":pData.authors,
                "titles":pData.titles,"big_genres":pData.big_genres, "lavin_genres":pData.lavin_genres}

#convert all metadata to dataframe
data = [metadata[i] for i in metadata.keys()]
df = pd.DataFrame(data)
df = df.transpose()
df.index.name = 'position'
df.columns=metadata.keys()

df1 = pd.read_csv("female_gothic_data/male_list_all_retrieved_texts.csv")
df2 = pd.read_csv("female_gothic_data/female_list_all_retrieved_texts.csv")

#for each row, get underwood matches
df1_underwood = df1.loc[df1['underwood'] == 'x']
df2_underwood = df2.loc[df2['underwood'] == 'x']

#check if only riddell or gutenberg (if both, use riddell)
df1_riddell = df1.loc[df1['underwood'] != 'x']
df1_riddell = df1_riddell.loc[df1_riddell['riddell'] == 'x']

df2_riddell = df2.loc[df2['underwood'] != 'x']
df2_riddell = df2_riddell.loc[df2_riddell['riddell'] == 'x']

#add a column for the riddell id so there's no chance of overlap with other id sets
df1_riddell['rid'] = ["r_"+str(i) for i in list(df1_riddell['\ufeffid'])]
df2_riddell['rid'] = ["r_"+str(i) for i in list(df2_riddell['\ufeffid'])]

#check if matched in gutenberg only
df1_gutenberg = df1.loc[df1['underwood'] != 'x']
df1_gutenberg = df1_gutenberg.loc[df1_gutenberg['riddell'] != 'x']

df2_gutenberg = df2.loc[df2['underwood'] != 'x']
df2_gutenberg = df2_gutenberg.loc[df2_gutenberg['riddell'] != 'x']

#add a column for the gutenberg id so there's no chance of overlap with other id sets
df1_gutenberg['gid'] = ["g_"+str(i) for i in list(df1_gutenberg['\ufeffid'])]

df2_gutenberg['gid'] = ["g_"+str(i) for i in list(df2_gutenberg['\ufeffid'])]

#convert each df to a list of dicts in id order, join with existing lists
"""
_ids, dates, genres, authors, titles, big_genres, lavin_genres, processed_genres
"""
#big_genres value = important
#append columns to pData attributes
#append dictionaries to feature_dicts_full

def for_append_metadata(df, id_column, gender, metadata):
    _ids = list(df[id_column])
    dates = list(df["year"])
    genres = ["gothic" for i in _ids]
    authors = list(df["author"])
    titles = list(df["title"])
    big_genres = [gender + "_gothic" for i in _ids]
    lavin_genres = ["gothic" for i in _ids]
    columns = [titles, lavin_genres, big_genres, _ids, authors, genres, dates]
    df = pd.DataFrame(columns)
    df = df.transpose()
    df.columns=metadata.keys()
    df.index.name = 'position'

    return df

df_ = for_append_metadata(df1_riddell, 'rid', "male", metadata)
df = df.append(df_)
df_ = for_append_metadata(df1_gutenberg, 'gid', "male", metadata)
df = df.append(df_)
df_ = for_append_metadata(df1_underwood, '\ufeffid', "male", metadata)
df = df.append(df_)
df_ = for_append_metadata(df1_gutenberg, 'gid', "female", metadata)
df = df.append(df_)
df_ = for_append_metadata(df2_riddell, 'rid', "female", metadata)
df = df.append(df_)
df_ = for_append_metadata(df2_underwood, '\ufeffid', "female", metadata)
df = df.append(df_)

#cull repeats by removing all underwood gothic
df = df.loc[df["big_genres"] != "gothic"]

#cull feature_dicts_full of original underwood gothic
culled_dicts = []
df_originals = df.loc[df['big_genres'] != 'female_gothic']
df_originals = df_originals.loc[df_originals['big_genres'] != 'male_gothic']
df_culled = list(df_originals['ids'])
for h,i in enumerate(pData._ids):
    if i in df_culled:
        culled_dicts.append(feature_dicts_full[h])

for h,i in enumerate(df['ids']):
    try:
        if "g" in i:
            gid = i.replace("g_". "")
            #title match from csv
            #read txt file by id
            #remove gutenberg from and back matter
            #process text to dictionary
            #reduce to 10k by reading "lavin_lexicon/features_all.csv"

        if "r" in i:
            rid = i.replace("r_". "")
    except:
        pass


partitioned_dfs, partitioned_ids = partition_test_train("gothic", df, 2)

#convert lists of ids into dictionaries of features in order of ids
partitioned_dicts = []

#loop enumerate(pData._ids)
for id_list in partitioned_ids:
    processing_list =[]
    for index, _id in enumerate(pData._ids):
        if _id in id_list:
            processing_list.append(feature_dicts[index])
    partitioned_dicts.append(processing_list)

#generalize for gothic, scifi, and mystery (genre soup also?)
train_genres = list(partitioned_dfs[0]['big_genres'])
train_genres = ["gothic" if g == "gothic" else "not gothic" for g in train_genres]
target_genres = list(partitioned_dfs[1]['big_genres'])
target_genres = ["gothic" if g == "gothic" else "not gothic" for g in target_genres]

#use scikit learn Pipeline functionality to vectorize from dictionaries, run tfidf, and perform logistic regression
text_clf = Pipeline([('vect', DictVectorizer()), ('tfidf', TfidfTransformer()),('clf', LogisticRegression()),])
text_clf = text_clf.fit(partitioned_dicts[0], train_genres)
predicted = text_clf.predict(partitioned_dicts[1])
mean_accuracy = np.mean(predicted == target_genres)
proba = text_clf.predict_proba(partitioned_dicts[1])

plabel = "probability_" + str(text_clf.classes_[0])

result = partitioned_dfs[1]
p = [i[0] for i in proba]
correct = []
for y,z in enumerate(predicted):
    if z == target_genres[y]:
        correct.append(1)
    else:
        correct.append(0)
result["correct"] = correct
result["predicted"] = predicted
result[plabel] = p

t = [0 if s == "gothic" else 1 for s in target_genres]
pr = [0 if s == "gothic" else 1 for s in predicted]
pr_false = [1 if s == "gothic" else 0 for s in predicted]

#recall_score(t, pr)
result["target_binary"] = t
result["predicted_binary"] = pr
result["predicted_binary_false"] = pr_false

correct = []
for y,z in enumerate(predicted):
    if z == target_genres[y]:
        correct.append(1)
    else:
        correct.append(0)
result["correct"] = correct

result["predicted_binary_false"] = pr_false
result = result.sort_values(str(plabel), ascending="False")
#result.to_csv("lavin_results/photo_results_logistic_100.csv")

#split the df into a top half and bottom half
r_bottom, r_top = np.array_split(result, 2)



#bottom means predicted not gothic, calculate right and wrong
bottom_correct = r_bottom.loc[r_bottom['big_genres'] != 'gothic']
#print(bottom_correct)
print(len(bottom_correct.index))

bottom_incorrect = r_bottom.loc[r_bottom['big_genres'] == 'gothic']
print(len(bottom_incorrect.index))
#print(bottom_incorrect)

#top means predicted gothic, calculate right and wrong
top_correct = r_top.loc[r_top['big_genres'] == 'gothic']
print(len(top_correct.index))

top_incorrect = r_top.loc[r_top['big_genres'] != 'gothic']
print(len(top_incorrect.index))

#make a confusion matrix using matplotlib and save as png
