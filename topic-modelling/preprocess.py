import sys
import logging
from logging import log, INFO

from fetch_data import getAbstracts
from preprocess import *
from utils import writeCSV

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=INFO)

try:
    model_name = sys.argv[1]
    data_count = sys.argv[2]
except:
    print('Specify model name (and data count) from the command line')

# Query abstracts from db
log(INFO, 'Querying {} abstracts'.format(data_count))
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
lemmatizedTexts = lemmatize(texts)


# Write preprocessed texts to a file
file_path = 'models/{}_lemmatized.csv'.format(model_name)
log(INFO, "Writing lemmatized abstracts to file {}".format(file_path))

writeCSV(file_name, list(zip(ids, lemmatizedTexts)))

log(INFO, "Finished")
