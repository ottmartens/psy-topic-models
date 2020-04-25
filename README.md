

# Psychology topic models

Requires: `docker`, `node`, `python`

### 1. Parsing, storing in db

_in pubmed-to-db:_
##### 1.1 Install dependencies: `npm install`
##### 1.2 Start database: `docker-compose up`
##### 1.2 Create database table structure: `node db-setup.js`
##### 1.2 Parse file: `node parse-from-xml.js <path-to-xml-file>`
_(xml-file refers to an export from pubmed)_

## 2. Preprocessing and model generation
_in topic-modelling:_
##### 2.1 Install modules `pip install nltk spacy gensim`
##### 2.2 Download nltk stopwords: `python download_stopwords.py`
##### 2.3 Download spacy en module: `python -m spacy download en`
##### 2.4 Preprocess the texts: `python preprocess.py`
##### 2.5 Transform corpus to dictionary and bag-of-words structure: `python -c "from transform_corpus import *; save_corpus_and_dictionary_to_file()"`
##### 2.6 Download Mallet, set `MALLET_PATH` environment variable
##### 2.7 Generate a topic model: `python generate_model.py <'gensim' | 'mallet'> ...topic_number_configurations`
##### 2.8 Calculate coherence scores: `python get_coherence.py ...model_names`
##### 2.8 Extract topics to a csv file: `python extract_topics.py <model-name> <number of topics>`
