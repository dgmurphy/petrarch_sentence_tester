# Petrarch Sentence Tester

## Install

### Python Libs
```
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
pip install -r requirements.txt
```

### Core NLP
```
cd stanford_corenlp_pywrapper
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2014-06-16.zip
unzip stanford-corenlp-full-2014-06-16.zip
mv stanford-corenlp-full-2014-06-16 standforstanford-corenlp
cd stanford-corenlp
wget http://nlp.stanford.edu/software/stanford-srparser-2014-07-01-models.jar
```

## Usage

Run in 'standard' mode to produce events:

`python test_parse.py s`

OR

Run in 'null actors' mode to see events and the actor labels.

`python test_parse.py n`

Note that this mode will produce events that would not have
been created in standard mode because standard mode will
not produce an event unless two actors can be coded.


Use null actors mode to see the labels needed to add the actors
to the dictionary.  Use the CAMEO code book and/or similar actors
that are already in the dictionary to determine what
the new actor codes should be.


