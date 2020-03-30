import os
import sys
import logging
from logging import log, INFO

import gensim

from utils import readCSV


def main():

    try:
        mallet_path = os.environ['MALLET_PATH']
    except:
        print('MALLET_PATH environment variable not found')
        exit(1)

    try:
        source_file = sys.argv[1]
        model_name = sys.argv[2]
    except:
        print(
            'specify lemmatized source file and model name from the command line arguments')
        exit(1)

    log(INFO, 'Parsing lemmatized texts from file {}'.format(source_file))
    ids, texts = readCSV(source_file)

    # Generate a dictionary of the corpus
    log(INFO, "Generating a dictionary")
    id2word = createDictionary(texts)

    # Create term document frequency corpus
    log(INFO, "Creating a term document frequency corpus")
    corpus = createCorpus(id2word, texts)

    # Generating a mallet lda model
    log(INFO, "Generating a mallet lda model")
    mallet_lda_model = gensim.models.wrappers.LdaMallet(
        mallet_path, corpus=corpus, num_topics=25, id2word=id2word)

    model_path = 'models/{}'.format(model_name)

    mallet_lda_model.save(model_path)
    log(INFO, 'Saved model to file {}'.format(model_path))

    log(INFO, 'Generating a coherence model')
    coherence_model = gensim.models.CoherenceModel(
        model, corpus=corpus, dictionary=id2word)

    coherence = coherence_model.get_coherence()
    log(INFO, 'Cohenrence of {} model: {}'.format(model_name, coherence))


if __name__ == '__main__':
    main()
