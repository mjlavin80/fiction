import pandas as pd
from application import db
from application.models import *
import urllib

def genre_entry(docid, genre):
    #convert doc_id to id
    _id = urllib.quote_plus(docid)
    work_id = db.session.query(Metadata).filter(Metadata.docid == _id).one().id
    #creat Genres instance
    ins = Genres()
    ins.id = None
    ins.genre = genre
    ins.work_id = work_id
    try:
        db.session.add(ins)
        db.session.commit()
    except:
        pass

def genre_maker(row):
    if row[1] == "x":
        genre_entry(row[0],"lavin_ghost")
        #print("lavin_ghost")
    if row[2] == "x":
        genre_entry(row[0],"lavin_slasher")
        #print("lavin_slasher")
    if row[3] == "x":
        genre_entry(row[0],"lavin_magic")
        #print("lavin_magic")
    if row[4] =="x":
        genre_entry(row[0],"lavin_deranged")
        #print("lavin_deranged")

lavin_genres = pd.read_csv("lavin_meta/horror_subgenre_tracers.tsv", sep='\t')

columns = zip(list(lavin_genres["docid"]), list(lavin_genres["ghost-haunting"]), list(lavin_genres["killer-slasher-gore"]), \
 list(lavin_genres["demon-occult-witch-magic-psychic"]), list(lavin_genres["insanity-deranged"]))

for row in columns:
    genre_maker(row)
