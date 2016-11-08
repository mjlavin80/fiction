import nltk
import pymysql
from config import MYDB, PWD
from application import db
from application.models import *
from collections import Counter
import glob

text = glob.glob('additional_texts/*.txt')

for filename in text:
    #open and read()
    with open(filename) as f:
        md_text = f.read()
    #tokenize, lowercase, remove newlines and tabs, strip punctuation and numbers
    #convert newlines and tabs to spaces
    md_text = md_text.replace('\n', ' ').replace('\t', ' ')
    #remove no-alpha characters, convert all to lowercase
    md_no_punct = ''.join(char.lower() if char.isalpha() else ' ' for char in md_text )
    #tokenize and drop empty list items
    md_tokens = [i for i in md_no_punct.split(' ') if i != '']
    #convert to counter
    md_counts = Counter(md_tokens).items()
    #insert to db
    ins = Metadata()
    ins.id = None
    #add title
    #print(filename)
    t = filename.replace("additional_texts/", "").replace(".txt", "")
    ins.title = t
    #add dates separately?
    db.session.add(ins)
    db.session.commit()
    #retrieve data you just added to get id

    _id = db.session.query(Metadata).filter(Metadata.title==t).one()

    #add to counts_id
    for pair in md_counts:
        row = Counts()
        row.counts_id = None
        row.work_id = _id.id
        row.type = pair[0]
        row.type_count = pair[1]
        db.session.add(row)
        db.session.commit()
