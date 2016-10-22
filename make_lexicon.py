from application import db
from application.models import *
import pymysql
from collections import Counter
from config import USER, PWD
import pandas as pd
#Make empty dictionary
terms = {}
#Loop ids from metadata
_ids = [i.id for i in db.session.query(Metadata).all()]

conn = pymysql.connect(host='localhost', port=3306, user=USER, passwd=PWD, db='horror')

cur = conn.cursor()

for _id in _ids:
    print(_id)
    query = "".join(["SELECT type FROM counts WHERE work_id=", str(_id), " AND type REGEXP '^[A-Za-z]+$';"])
    #loop terms matching certain criteria (regex query)
    a = cur.execute(query)
    for row in cur:
        #Try to add to count in dictionary
        try:
            current = terms[row[0]]
            terms[row[0]] = current+1
        except:
            #Except add term to dictionary with count of one
            terms[row[0]] = 1

#At end of loop, order by count, stop at 10k
term_pairs = Counter(terms).most_common(10000)

#convert to pandas df (terms and counts)
df = pd.DataFrame(term_pairs, columns=["term", "docs"])

#Save as csv in lavin_lexicon folder
df.to_csv("lavin_lexicon/features_all.csv")

cur.close()
conn.close()
