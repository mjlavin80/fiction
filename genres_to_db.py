import csv, pandas as pd
import pymysql
from application import db
from application.models import *
import urllib

list_of_files = ["final/AllDetective2016-04-09.csv", "final/AllGothic2016-04-10.csv",
                 "final/AllSF2016-04-10.csv"]
genres = ["detective", "gothic", "scifi"]
for k, i in enumerate(list_of_files):
    f = pd.read_csv(i)
    for _id in list(f["volid"]):
        #insert into
        ins = Genres()
        ins.id = None
        ins.genre = genres[k]
        #convert u_id to work_id

        try:
            _id = urllib.quote_plus(_id)
            work_id = db.session.query(Metadata).filter(Metadata.docid == _id).one().id
            #print(work_id)
            ins.work_id = work_id
            db.session.add(ins)
            db.session.commit()
        except:
            print("Skipped id %s, no match in DB" % _id)
