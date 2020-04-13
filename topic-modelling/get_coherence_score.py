import sys
import logging
from logging import log, INFO

import gensim

from utils import *
from preprocess_helpers import createDictionary

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=INFO)


def main():
    try:
        corpus_path = sys.argv[1]
        model_names = sys.argv[2:]
    except:
        print('specify corpus file and model name(s) from the command line')
        exit(1)
    
    corpus_path = 'models/{}'.format(corpus_path)

    log(INFO, 'Parsing texts from file')
    _, texts = readCSV(corpus_path)

    # Generate a dictionary of the corpus
    log(INFO, "Generating a dictionary")
    id2word = createDictionary(texts)

    coherences = []

    for model_name in model_names:

        log(INFO, "Loading model from models/{}".format(model_name))
        model_path = 'models/{}'.format(model_name)

        log(INFO, 'Loading topic model from file')
        model = gensim.utils.SaveLoad.load(model_path)

        log(INFO, 'Generating a cohenrence model')
        coherence_model = gensim.models.CoherenceModel(model, texts=texts)

        coherence = coherence_model.get_coherence()
        coherences.append(coherence)
    
    for model_name, coherence in list(zip(model_names, coherences)):
        log(INFO, "Coherence of {}: {}".format(model_name, coherence))
    
    writeCSV("coherences.csv", list(zip(model_names, coherences)))
    log(INFO, "Finished")


if __name__ == '__main__':
    main()
