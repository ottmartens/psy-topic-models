from gensim.utils import SaveLoad
from gensim.models.wrappers import DtmModel
from transform_corpus import read_corpus_ordered_by_year
import csv
import os
import sys

import logging
from logging import log, INFO
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=INFO)


try:
    dtm_binary_path = os.environ['DTM_BINARY_PATH']
except:
    print("Please specify path to dtm binary in DTM_BINARY_PATH env variable")
    exit(1)

try:
    num_topics = int(sys.argv[1])
except:
    print("Specify number of topics from command line")
    exit(1)

log(INFO, "Parsing corpus year intervals")

with open('corpus_year_intervals.csv', 'r') as file:
    rows = list(csv.reader(file))
    intervals = list(map(int, rows[0]))
    file.close()

log(INFO, "Parsing ordered corpus from file")
ordered_corpus = read_corpus_ordered_by_year()

log(INFO, "Reading dictionary from file")
dictionary = SaveLoad.load('dictionary_ordered_by_year')

log(INFO, "Generating a dynamic topic model with {} topics".format(num_topics))
model = DtmModel(dtm_binary_path, corpus=ordered_corpus,
                 time_slices=intervals, id2word=dictionary, num_topics=num_topics)

model_path = 'models/dtm_{}'.format(num_topics)
log(INFO, "Saving model to {}".format(model_path))
model.save(model_path)

log(INFO, "Finished")
