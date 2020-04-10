from nltk.corpus import wordnet as wn
import logging
from logging import log, INFO
from utils import *

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=INFO)

multiterms = []
log(INFO, "Generating a list of multiword terms from wordnet")

for synset in list(wn.all_synsets('n')):
    lemmas = synset.lemmas()
    for Lemma in lemmas:
        lemma = Lemma.name()
        if '_' in lemma and lemma not in multiterms:
            multiterms.append([lemma])

log(INFO, "Found {} multiterms".format(len(multiterms)))

filename = "wordnet_multiword_terms.csv"
log(INFO, "Writing to file {}".format(filename))
writeCSV(filename, multiterms)

log(INFO, "Finished")
