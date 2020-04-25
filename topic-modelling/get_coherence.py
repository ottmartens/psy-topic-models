import sys
import logging
from logging import log, INFO
import gensim

from utils import *

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=INFO)

def main():
    try:
        model_names = sys.argv[1:]
    except:
        print('specify model name(s) from the command line')
        exit(1)

    log(INFO, 'Parsing texts from file')
    _, texts = readCSV('lemmatized.csv')

    log(INFO, 'Parsing dictionary from file')
    id2word = gensim.utils.SaveLoad.load('dictionary')

    coherences = []

    for model_name in model_names:

        log(INFO, "Loading model {} from file".format(model_name))
        model_path = 'models/{}'.format(model_name)
        model = gensim.utils.SaveLoad.load(model_path)

        coherence = get_coherence(model, texts, id2word)
        coherences.append(coherence)

    for model_name, coherence in list(zip(model_names, coherences)):
        log(INFO, "Coherence of {}: {}".format(model_name, coherence))

    writeCSV("coherences.csv", list(zip(model_names, coherences)))

    log(INFO, "Finished")


def get_coherence(model, texts, dictionary):
    log(INFO, 'Generating a coherence model')
    coherence_model = gensim.models.CoherenceModel(
        model=model, texts=texts, dictionary=dictionary, coherence='c_v')

    return coherence_model.get_coherence()



if __name__ == '__main__':
    main()
