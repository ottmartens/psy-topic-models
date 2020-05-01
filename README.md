

# Psychology topic models

Requires: `docker`, `node`, `python`

## 1. Parsing, storing in db
_in pubmed-to-db:_
##### 1.1 Install dependencies: `npm install`
##### 1.2 Start database: `docker-compose up`
##### 1.2 Create database table structure: `node db-setup.js`
##### 1.2 Parse file: `node parse-from-xml.js <path-to-xml-file>`
_(xml-file refers to an export from pubmed)_

## 2. Preprocessing
_in topic-modelling:_
##### 2.1 Install modules `pip install nltk spacy gensim`
##### 2.2 Download nltk stopwords: `python download_stopwords.py`
##### 2.3 Download spacy en module: `python -m spacy download en`
##### 2.4 Preprocess the texts: `python preprocess.py`
##### 2.5 Transform corpus to dictionary and bag-of-words structure: `python -c "from transform_corpus import *; save_corpus_and_dictionary_to_file()"`

## 3. LDA
_in topic-modelling:_
##### 3.1 Download Mallet, set `MALLET_PATH` environment variable
##### 3.2 Generate a topic model: `python generate_model.py <'gensim' | 'mallet'> ...topic_number_configurations`
##### 3.3 Calculate coherence scores: `python get_coherence.py ...model_names`
##### 3.4 Extract topics to a csv file: `python extract_topics.py <model-name> <number of topics>`

## 4. Dynamic topic model
_in topic-modelling:_
##### 4.1 Order corpus per year "from transform_corpus import *; save_corpus_ordered_by_year()"
##### 4.2 Dowload precompiled dtm binary from https://github.com/magsilva/dtm/tree/master/bin
##### 4.3 Set DTM_BINARY_PATH to downloaded binary
##### 4.3 Make sure you have gsl/libgs library installed
##### 4.4 Generate the model `python dynamic_topic_model.py <num_topics>`