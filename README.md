# Petrarch Sentence Tester

## Install

### Clone

`git clone https://github.com/dgmurphy/petrarch_sentence_tester.git`

`cd petrarch_sentence_tester`

### Virtual Environment

Create a Python2 virtual environment:

```virtualenv -p /usr/bin/python2.7 venv```

Activate the virtual environment:

```source venv/bin/activate```

### Python Libs
```
pip install -r requirements.txt
```

### Core NLP
```
cd stanford_corenlp_pywrapper
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2014-06-16.zip
unzip stanford-corenlp-full-2014-06-16.zip
mv stanford-corenlp-full-2014-06-16 stanford-corenlp
cd stanford-corenlp
wget http://nlp.stanford.edu/software/stanford-srparser-2014-07-01-models.jar
```

## Usage

Edit file `input.txt` to add sentences. The sentence dates are used to resolve actor codes e.g. when the actor served a different role over time.

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

## Results

Output is in `results.txt`

Example:

```
SENTENCE PARSE RESULTS
2020-07-15 21:48:56.200741
# sentences: 4
Coding Mode:  Null Actors = TRUE

SENTENCE:
An armed group attacked the village of Macomia in northern Mozambique in the early morning hours of May 28, setting fire to homes, s
hops, schools, religious and government buildings, and forcing people to flee into the bush and neighboring villages, said the inter
national medical humanitarian organization Doctors Without Borders/Médecins Sans Frontières (MSF) on Friday.

sentence date: 2013 10 1

Events: 2

Source Actor, Target Actor, Verb Code, Verb Label
Event 1: *1*UAF	 *3*CVL	 015	said <ATTACKED>
Event 2: *1*UAF	 MEAREBHLH	 010	said

Actors for event 1
	Soure actor: armed group ... an <ARMED> <GROUP> => *1*UAF
	Target actor: village ... the ... village =>  *3*CVL
	Verb code:  015

Actors for event 2
	Soure actor: armed group ... an <ARMED> <GROUP> => *1*UAF
	Target actor: organization Doctors =>  MEAREBHLH
	Verb code:  010



SENTENCE:
Barack Obama met with Tony Blair.

sentence date: 2009 20 1

Events: 1

Source Actor, Target Actor, Verb Code, Verb Label
Event 1: USAGOV	 GBRELI	 040	met

Actors for event 1
	Soure actor: Barack Obama => USAGOV
	Target actor: Tony Blair =>  GBRELI
	Verb code:  040



SENTENCE:
Roger Waters argued with David Gilmore.

sentence date: 2009 10 1

Events: 1

Source Actor, Target Actor, Verb Code, Verb Label
Event 1: *1*	 *2*	 110	arged

Actors for event 1
	Soure actor: Roger Waters => *1*
	Target actor: David Gilmore =>  *2*
	Verb code:  110



SENTENCE:
This sentence will fail to generate events.
sentence date: 2009 10 1
# of events: 0
```
