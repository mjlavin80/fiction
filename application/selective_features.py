

def dictionaries_of_features(list_of_dictionaries, feature_list):
    import pandas as pd
    """Loops through the list of dictionaries supplied, gathers counts for each term in the feature list,
    and returns a new list of smaller dictionaries. We then pass the reesults to sklearn CountVectorizer for zerofill
    and other model processing"""
    reduced_dictionaries = []
    for d in list_of_dictionaries:
        processing_dictionary = {}
        for feature in feature_list:
            # Here we just try to find the term in the source dictionary and skip if there's an exception,
            # which can only happen if the term is not in the source dictionary
            # This is more memory performant than an if-then approach
            try:
                processing_dictionary[feature] = d[feature]
            except:
                pass
        #finally we append the processing_dictionary to the new list of dicts, preserving their original order
        reduced_dictionaries.append(processing_dictionary)
    return reduced_dictionaries

def make_genres_big(piped_genres):
    import pandas as pd
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
