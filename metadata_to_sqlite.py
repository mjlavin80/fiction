import pickle
import sqlite3
metadata = pickle.load( open( "pickled_data/metadata.p", "rb" ))
genres = pickle.load( open( "pickled_data/big_genres.p", "rb" ))
#docid	recordid	oclc	locnum	author	imprint	date	birthdate	firstpub	enumcron	subjects	title	nationality	gender	genretags

meta_tuples = []
for h,i in enumerate(metadata):
    try:
        year = int(i[8])
    except:
        year = 0
    genre = genres[h].decode('latin-1')
    doc_id = i[0].decode('latin-1')
    title = i[11].decode('latin-1')
    meta = (year, doc_id, title, genre)
    meta_tuples.append(meta)

conn = sqlite3.connect("all_measures_fiction.db")
c = conn.cursor()
drop = """DROP TABLE IF EXISTS metadata"""
c.execute(drop)
create = """CREATE TABLE IF NOT EXISTS metadata (id INTEGER PRIMARY KEY, pub_year INTEGER, doc_id TEXT, title TEXT, genre TEXT)"""
c.execute(create)

insert = """INSERT INTO metadata (id, pub_year, doc_id, title, genre ) VALUES (null, ?,?,?,?)"""

for s in meta_tuples:
    c.execute(insert, s)
    conn.commit()
