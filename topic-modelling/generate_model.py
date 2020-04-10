import os
import sys
import logging
from logging import log, INFO

import gensim

from utils import readCSV
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
        model_name = sys.argv[1]
    except:
        print(
            'Specify model name from the command line arguments (the same one from preprocessing')
        exit(1)

    if len(sys.argv) < 2:
        print("Specify topic counts to be ran as command line arguments")
        exit(1)
    
    topic_ns = list(map(int, sys.argv[1:]))
    log(INFO, "Generating model(s) with {} topics".format(topic_ns))

    source_file_path = 'models/{}_lemmatized.csv'.format(model_name)

    log(INFO, 'Parsing lemmatized texts from file {}'.format(source_file_path))
    ids, texts = readCSV(source_file_path)

    # Generate a dictionary of the corpus
    log(INFO, "Generating a dictionary")
    id2word = createDictionary(texts)

    # Create term document frequency corpus
    log(INFO, "Creating a term document frequency corpus")
    corpus = createCorpus(id2word, texts)

    for num_topics in topic_ns:

        # Generating a mallet lda model
        log(INFO, "Generating a mallet lda model")
        mallet_lda_model = gensim.models.wrappers.LdaMallet(
            mallet_path, corpus=corpus, num_topics=num_topics, id2word=id2word)

        model_path = 'models/{}_{}'.format(model_name, num_topics)

        mallet_lda_model.save(model_path)
        log(INFO, 'Saved model to file {}'.format(model_path))

        log(INFO, 'Generating a coherence model')
        coherence_model = gensim.models.CoherenceModel(
            model=mallet_lda_model, texts=texts, dictionary=id2word, coherence='c_v')

        coherence = coherence_model.get_coherence()
        log(INFO, 'Cohenrence of {} model: {}'.format(model_name, coherence))

    log(INFO, "Finished")

if __name__ == '__main__':
    main()
