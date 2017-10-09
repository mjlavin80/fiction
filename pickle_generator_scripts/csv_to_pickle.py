import pickle
import csv

dict_of_10k = {}
with open ("lexicon/new10k.csv", "r") as myfile:
    for m_line in csv.reader(myfile):
        if m_line[0] != "word":
            dict_of_10k[m_line[0]] = m_line[1]

full_feature_dicts = []
feature_dicts = []

#initial list of excluded_ids
excluded_ids = ["dul1.ark+=13960=t6446jc6s", "sanskritdevasmita", "arabicthreesharpers", "uc1.$b522186", \
"pushkinqueenofspades", "chekhovsafetymatch", "nnc1.0113307762", "mdp.39015005108595", "meyrinkmanonthebottle"]

docids = []
with open ("meta/finalmeta.csv", "r") as myfile:
    for m_line in csv.reader(myfile):
        if m_line[0] != "docid":
            if m_line[0] not in excluded_ids:
                docids.append(m_line[0])


for _id in docids:
    try:
        full_fdict = {}
        fdict = {}
        with open("newdata/%s.fic.tsv" % str(_id)) as f:
            s = f.read()
            s = s.replace("\n\"\t", "\n\\\"\t")
            row = s.split("\n")
            cells = [tuple(i.split("\t")) for i in row]
            for y in cells:
                try:
                    full_fdict[y[0]] = int(y[1])
                except:
                    pass
                #check for top 10k terms
                try:
                    test = dict_of_10k[y[0]]
                    fdict[y[0]] = int(y[1])
                except:
                    pass
        full_feature_dicts.append(full_fdict)
        feature_dicts.append(fdict)
    except:
        print(_id)
        excluded_ids.append(_id)

pickle.dump(feature_dicts, open( "pickled_data/feature_dicts_10k.p", "wb" ))
pickle.dump(full_feature_dicts, open( "pickled_data/full_feature_dicts.p", "wb" ))
pickle.dump(excluded_ids, open( "pickled_data/excluded_ids.p", "wb" ))
