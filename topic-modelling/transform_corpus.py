from logging import log, INFO
import logging
import csv
from utils import *
from preprocess_helpers import createCorpus, createDictionary
import itertools


logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=INFO)


def save_corpus_and_dictionary_to_file():
    log(INFO, "Parsing texts")

    ids, texts = readCSV("lemmatized.csv")

    log(INFO, "Creating dictionary")

    id2word = createDictionary(texts)

    log(INFO, "Saving dictionary to a file")

    id2word.save("dictionary")

    log(INFO, "Creating corpus")

    corpus = createCorpus(id2word, texts)

    with open('flat_corpus.csv', 'w') as file:

        log(INFO, "Writing to file")

        writer = csv.writer(file)

        for corpus_row in corpus:

            writer.writerow(itertools.chain(*corpus_row))

        log(INFO, "Finished")


def read_corpus_from_file():

    with open('flat_corpus.csv', 'r') as file:
        rows = list(csv.reader(file))

        result = []

        log(INFO, "Converting corpus to tuple structure")

        for row in rows:
            result.append(
                list(zip(
                    list(map(int, row[::2])),
                    list(map(int, row[1::2]))
                ))
            )

        file.close()

        log(INFO, "Coprus parsed")

    return result
