import csv, pandas as pd
import pymysql
from application import db
from application.models import *

list_of_files = ["final/AllDetective2016-04-09.csv", "final/AllGothic2016-04-10.csv",
                 "final/AllSF2016-04-10.csv"]

f = pd.read_csv("meta/finalmeta.csv")
for key, value in f.iterrows():
    _id = value[0]
    genre_tags = value[14].split(" | ")
    #loop genre_tags
    for tag in genre_tags
        #insert into
        ins = Genres()
        ins.id = None
        ins.genre = tag

        try:
            _id = urllib.quote_plus(_id)
            work_id = db.session.query(Metadata).filter(Metadata.docid == _id).one().id
            #print(work_id)
            ins.work_id = work_id
            db.session.add(ins)
            db.session.commit()
        except:
            print("Skipped id %s, no match in DB" % _id)
