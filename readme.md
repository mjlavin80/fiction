lavin edits (in progress)
======
- added structure for flask-sqlalchemy ORM, including application/models.py
- added and am periodically updating requirements.txt for python dependencies
- added db ingestion scripts to transfer metadata, counts, and genres to a mysql database as quickly as possible

# To replicate ingestion:
1. Set up an empty mysql target database (utf8) and a usr will priveleges
2. In root folder of local version of this repo, make a file called config.py (see sample_config.py for what needs to be in it)
3. Assuming you have python and pip all set up, run "pip install -r requirements.txt" (works best inside a virtualenv)
4. Run "db_create.py"
5. Run "underwood_metadata.py"
6. Run "underwood_counts.py"
7. Run "genres_to_db.py"

# To use scripts in lavin_tests directory

At a project's root level, you would typically run a file like this:

`python some_script.py`

Scripts in the lavin_scripts folder, however, depend upon packages in sibling folders, e.g. application.models. As a result, to run these scripts, you should remain in . directory and execute script without the .py extension so they are interpreted as packages. Here is an example of the command line text used to run lavin_tests/test_feat_list.py:

`python -m lavin_scripts.test_feat_list`

This method will keep the application context visible and keep the relative paths to .csv files intact at the same time. I'm working on a cleaner way to tuck scripts away in sibling folders, but so far I haven't found one that does both of these things, partly because importing from inside sibling folders is not an encourage Python approach. 

- added a folder for "additional_texts" and a script to read that folder and add text to the database (will eventually add texts)
- to add texts of your own, place txt files in the "additional_texts" folder and run "other_txt_to_db.py"

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
