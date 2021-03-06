import sys
import logging
from logging import log, INFO

from fetch_data import getAbstracts
from preprocess_helpers import *
from utils import writeCSV, readCSV

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=INFO)

# Query abstracts from db
log(INFO, 'Querying abstracts')
texts, ids = getAbstracts()
log(INFO, "Found {} abstracts".format(len(texts)))

# Tokenize, remove stopwords
log(INFO, 'Tokenizing and removing stopwords')
texts = removeStopwords(texts)

# Generate phrasers for multiwords
log(INFO, 'Generating phrasers')
bigramPhraser, trigramPhraser = generatePhrasers(
    texts, min_count=5, threshold=50)

# Generate multiword n-grams
log(INFO, "Generating multiword n-grams")
texts = makeNGrgrams(texts, bigramPhraser, trigramPhraser)

# Parse all multiword terms from wordnet
log(INFO, "Parsing wordnet multiterms into dictionary")
wordnetMultitermDict = readMultiterms()

# Match multiword terms from wordnet
log(INFO, "Matching wordnet multiterms")
texts = applyWordnetMultiterms(texts, wordnetMultitermDict)

# Lemmatize the texts and filter for allowed token tags
log(INFO, "Lemmatizing")
texts = lemmatize(texts, allowed_token_tags=['NNP', 'NNS', 'NN'])

# Write preprocessed texts to a file
file_path = 'models/lemmatized.csv'.format(model_name)

log(INFO, "Writing lemmatized abstracts to file {}".format(file_path))
writeCSV(file_path, list(zip(ids, texts)))

log(INFO, "Finished")
