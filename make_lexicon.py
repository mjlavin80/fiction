from application import db
from application.models import *
import pymysql
from config import USER, PWD

#Make empty dictionary
terms = {}
#Loop ids from metadata
_ids = [i.id for i in db.session.query(Metadata).all()]

conn = pymysql.connect(host='localhost', port=3306, user=USER, passwd=PWD, db='horror')

cur = conn.cursor()

for _id in _ids[:5]:
    print(_id)
    query = "".join(["SELECT type FROM counts WHERE work_id=", str(_id), " AND type REGEXP '^[A-Za-z]+$';"])
    #loop terms matching certain criteria (regex query)
    a = cur.execute(query)
    for row in cur:
        print(row[0])
cur.close()
conn.close()
    #Try to add to count in dictionary
    #Except add term to dictionary with count of one
    #At end of loop, convert to pandas df (terms and counts)
    #Order by count
    #Stop at 10k
    #Save as csv in lavin_lexicon folder
