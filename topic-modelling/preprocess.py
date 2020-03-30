import sys
import logging
from logging import log, INFO

from fetch_data import getAbstracts
from preprocess_helpers import *
from utils import writeCSV, readCSV

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=INFO)

try:
    model_name = sys.argv[1]
except:
    print('Specify model name from the command line')
    exit(1)

# Query abstracts from db
log(INFO, 'Querying abstracts')
texts, ids = getAbstracts()
log(INFO, "Found {} abstracts".format(len(texts)))


# Remove stopwords
log(INFO, 'Removing stopwords')
texts = removeStopwords(texts)


# Generate phrasers for bigrams an trigrams
log(INFO, 'Generating phrasers')
bigramPhraser, trigramPhraser = generatePhrasers(
    texts, min_count=5, threshold=100)

# Generate bigrams and trigrams
log(INFO, "Generating bigrams")
bigrams = makeBigrams(texts, bigramPhraser)

log(INFO, 'Generating trigrams')
trigrams = makeTrigrams(texts, bigramPhraser, trigramPhraser)

# Lemmatize the texts
log(INFO, "Lemmatizing")
texts = lemmatize(trigrams)

# Write preprocessed texts to a file
file_path = 'models/{}_lemmatized.csv'.format(model_name)
log(INFO, "Writing lemmatized abstracts to file {}".format(file_path))

writeCSV(file_path, list(zip(ids, texts)))

log(INFO, "Finished")
