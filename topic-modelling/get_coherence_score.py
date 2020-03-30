import sys
import logging
from logging import log, INFO

import gensim

from utils import readCSV

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=INFO)


def main():
    try:
        model_name = sys.argv[1]
    except:
        print('specify name of the model from the command line')
        exit(1)

    model_path = 'models/{}'.format(model_name)
    corpus_path = 'models/{}_lemmatized.csv'.format(model_name)

    log(INFO, 'Parsing texts from file')
    _, texts = readCSV(corpus_path)

    log(INFO, 'Loading topic model from file')
    model = gensim.utils.SaveLoad.load(model_path)

    log(INFO, 'Generating a cohenrence model')
    coherence_model = gensim.models.CoherenceModel(model, texts=texts)

    coherence = coherence_model.get_coherence()

    print('Coherence of {} : {}'.format(model_name, coherence))


if __name__ == '__main__':
    main()
