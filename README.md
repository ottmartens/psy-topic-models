

# Psychology topic models

Requires: `docker`, `node`, `python`

### 2. Parsing, storing in db

_in pubmed-to-db:_
##### 2.1 Install dependencies: `npm install`
##### 2.2 Start database: `docker-comppose up`
##### 2.2 Create database table structure: `node db-setup.js`
##### 2.2 Parse file: `node parse-from-xml.js <path-to-xml-file>`
_(xml-file refers to an export from the pubmed database)_

## 3. Preprocess, generate topic model

_in topic-modelling:_
##### 3.1 Install modules `pip install nltk spacy gensim`
##### 3.2 Download nltk stopwords: `python download_stopwords.py`
##### 3.3 Download spacy en module: `python -m spacy download en`
##### 3.4 Preprocess the texts: `python preprocess.py <model-name>`
##### 3.5 Generate a topic model: `python generate_model.py <mode-name>`
##### 3.6 Extract topics to a csv file: `python extract_topics.py <model-name>`
