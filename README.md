



## 1. Download corpus

## 2. Parse, store in db

### In pubmed-to-tb:
2.1 start database: `docker-comppose up`
2.2 create tables: `node db-setup.js`
2.2 parse file: `node index.js`

## 3. Preprocess, generate topic model

### In topic-modelling:
3.1 install modules `pip install nltk spacy gensim`
3.2 download nltk stopwords: `python download_stopwords.py`
3.3 download spacy en module: `python3 -m spacy download en`