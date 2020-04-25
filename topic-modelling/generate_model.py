import os
import sys
import logging
from logging import log, INFO

import gensim

from utils import readCSV
from transform_corpus import read_corpus_from_file
from preprocess_helpers import createCorpus, createDictionary

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=INFO)


def main():

    try:
        mallet_path = os.environ['MALLET_PATH']
    except:
        print('MALLET_PATH environment variable not found')
        exit(1)

    try:
        model_type = sys.argv[1]

        if model_type not in ['gensim', 'mallet']:
            raise Exception
    except:
        print(
            'Specify model type as the first argument as either gensim or mallet')
        exit(1)

    if len(sys.argv) < 2:
        print("Specify topic counts to be ran as command line arguments")
        exit(1)

    topic_ns = list(map(int, sys.argv[2:]))
    log(INFO, "Generating model(s) with {} topics".format(", ".join(topic_ns)))

    log(INFO, "Parsing dictionary from file")
    id2word = gensim.utils.SaveLoad.load('dictionary')

    log(INFO, "Parsing corpus from file")
    corpus = read_corpus_from_file()

    for num_topics in topic_ns:

        model_name = '{}_{}'.format(model_type, num_topics)

        if model_type == 'gensim':

            log(INFO, "Generating a gensim lda model")
            model = gensim.models.ldamulticore(
                corpus, num_topics=num_topics, id2word=id2word
            )

            log(INFO, "Perplexity of {} estimated of a fraction of the corpus: {}".format(
                model_name, model.log_perplexity(corpus[::100])))

        else:

            log(INFO, "Generating a mallet lda model")
            model = gensim.models.wrappers.LdaMallet(
                mallet_path, corpus=corpus, num_topics=num_topics, id2word=id2word)

        model_path = 'models/{}'.format(model_name)

        model.save(model_path)
        log(INFO, 'Saved model to file {}'.format(model_path))

    log(INFO, "Finished")


if __name__ == '__main__':
    main()
