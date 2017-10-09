import csv
import pickle

#parse "Etymologies.txt"
dictcom_dict = {}

with open ("Etymologies.txt", "r") as myfile:
    #insert statement
    for line in csv.reader(myfile, dialect="excel-tab"):
        dictcom_dict[line[0]] = line[1]
        #k = ("term", "year")

pickle.dump(dictcom_dict, open( "pickled_data/dictcom_dict.p", "wb" ))
