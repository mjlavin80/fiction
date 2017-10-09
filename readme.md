# Notes

- Numerous ids don't have corresponding data folders in newdata because they were purged (as children's lit?) at some point
- As a result, the length of finalmeta.csv and feature_dicts.p will only line up if you purge those ids, as csv_meta_to_pickle.py does

# Protocol to add files
  - metadata should be loaded from a master csv, "lavin_meta/lavin_meta.csv"
  - metadata format mimics finalmeta
  - id in lavin_meta should match filename.txt in lavin_additional_texts
  - genre is snhorror to denote mentioned in Lovecraft's *Supernatural Horror in Literature*  
  - duplicates marked in readme.md (see below)
  - need to do something other than lovecraft_horror in one big text file
    - make other combinations of stories by date?

# Best Order of pickle scripts

#### Run from root directory as ...

python pickle_generator_scripts/csv_to_pickle.py
python pickle_generator_scripts/csv_meta_to_pickle.py
python pickle_generator_scripts/lavin_to_pickle.py
python -m pickle_generator_scripts.big_genres_to_pickle
python pickle_generator_scripts/dictom_to_p.py
python pickle_generator_scripts/oed_to_p.py

# Run dictionary-based Tests
run_all_ratios.py

# Files missing or removed from original Underwood repo
- hvd.hwpn81
- dul1.ark+=13960=t95723c7j
- uc2.ark+=13960=t43r0q389
- njp.32101068784931
- mdp.39015031447595
- uc1.$b813837
- njp.32101068784923
- njp.32101065766410
- uc2.ark+=13960=t1qf8mn3h
- uc1.$b813839
- inu.30000042750632
- nyp.33433082344916
- nc01.ark+=13960=t2d80cp48
- nyp.33433082529995
- nyp.33433082332051
- nyp.33433082305636
- nyp.33433082332077
- nyp.33433082305644
- nyp.33433082344874
- nyp.33433082530050
- nyp.33433082305628
- nyp.33433082332069

# SQL queries to save results to csv

#### From all_measures_fiction.db ...
SELECT doc_id, oed_ratio_no_set, oed_ratio_set FROM  results WHERE is_resample=0;
SELECT doc_id, gl_ratio_no_set, gl_ratio_set FROM  results WHERE is_resample=0;
SELECT doc_id, walker_ratio_no_set, walker_ratio_set FROM  results WHERE is_resample=0;

#### From regression_scores.db ...
SELECT doc_id, AVG(predicted) as average_predicted, actual, AVG(margin) as average_margin FROM results GROUP BY  doc_id ORDER BY average_margin;

<em>Hereafter is Ted Underwood's readme.md from his original repo for the article ["The Life Cycles of Genres" in _Cultural Analytics._](http://culturalanalytics.org/2016/05/the-life-cycles-of-genres/)</em>
<hr/>

fiction
=======

Code and data supporting the article ["The Life Cycles of Genres" in _Cultural Analytics._](http://culturalanalytics.org/2016/05/the-life-cycles-of-genres/)

[![DOI](https://zenodo.org/badge/19804/tedunderwood/fiction.svg)](https://zenodo.org/badge/latestdoi/19804/tedunderwood/fiction)

The data model here assumes that genre designations are situated and perspectival. An observer in a particular place and time groups a particular set of works and calls them 'crime fiction.' We don't necessarily know that anyone else will agree; a different observer could group different works as 'detective fiction,' which might or not be the same thing. Nothing prevents some of these works from also being 'science fiction.' For that matter, some works can belong to no genre at all.

In short, every work can carry any number of genre tags, from zero upward. The compatibility of different definitions becomes an empirical question. Do different observers actually agree? Can a model trained on one observer's claims about detective fiction also predict the boundaries of 'crime fiction', as defined by someone else?

We use predictive modeling to test these questions. If you want to replicate the results here you'll need Python 3 and a copy of this repository. Running code/replicate.py will give you a range of modeling options keyed to particular sections of the article. The script will draw on metadata in meta/finalmeta.csv, wordcount files in the newdata directory, and the provided lexicon. Note that the selection of volumes in the negative contrast set can be stochastic, if more are available than needed to match the positive volumes. (For that matter, the positive set can at times be a random subset too.) So please don't expect replication to exactly match every figure down to the decimal point.

Because many of the books here are under copyright or otherwise encumbered with intellectual property agreements, I have to share wordcounts rather than original texts. If you want to consult texts in HathiTrust before 1922, it's usually possible to find them by pasting the Hathi volume id into a link of this form:

[http://babel.hathitrust.org/cgi/pt?id=uiuo.ark:/13960/t7wm20x0v](http://babel.hathitrust.org/cgi/pt?id=uiuo.ark:/13960/t7wm20x0v)

final
----
This is the folder where you will find lists of predictive features for various genres modeled in the article, along with probabilities assigned to particular volumes.

meta
----
Metadata for the project.

Right now the most complete set of metadata is in finalmeta.csv.

newdata
----
The data used in the model: tables of word counts for each volume, as separate files. No, there is no olddata.

code
----
Code for the modeling process. The key modules for modeling are logisticpredict, metafilter, modelingprocess, and metautils. replicate.py is a script that allows readers to reproduce the particular settings I used for tests in the article.

plot
----
(Mostly R) scripts for plotting in the sense of "dataviz." Has nothing to do with fictional plots.

lexicon
-------
The set of features that was used to produce the article; the top 10,000 words by document frequency in the whole corpus.
