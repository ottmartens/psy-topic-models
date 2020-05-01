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


def save_corpus_ordered_by_year():

    log(INFO, "Parsing texts")
    ids, texts = readCSV("lemmatized.csv")

    with open('ids_per_year.csv', 'r') as file:
        ids_per_year = list(csv.reader(file))
        file.close()

    texts_odered_by_year = []
    corpus_year_intervals = []

    log(INFO, "Sorting and filtering texts per year")
    for row in ids_per_year:
        year = row[0]
        ids = row[1:]

        corpus_year_intervals.append(len(ids))

        for id in ids:
            index = ids.index(id)
            texts_odered_by_year.append(texts[index])
    
    log(INFO, "Creating dictionary")
    dicrionary_ordered_by_year = createDictionary(texts_odered_by_year)

    log(INFO, "Saving dictionary")
    dicrionary_ordered_by_year.save("dictionary_ordered_by_year")

    corpus_odered_by_year = createCorpus(dicrionary_ordered_by_year, texts_odered_by_year)

    log(INFO, "Writing ordered coprus to file, total length: {}".format(
        len(corpus_odered_by_year)))

    with open('corpus_ordered_by_year.csv', 'w') as file:
        writer = csv.writer(file)

        for row in corpus_odered_by_year:
            writer.writerow(itertools.chain(*row))

        file.close()

    log(INFO, "Writing corpus year intervals to file")

    with open('corpus_year_intervals.csv', 'w') as file:
        writer = csv.writer(file)

        writer.writerow(corpus_year_intervals)
        file.close()

    log(INFO, "Finished")

def read_corpus_ordered_by_year():
    with open('corpus_ordered_by_year.csv', 'r') as file:
        rows = list(csv.reader(file))

        file.close()

    result = []

    log(INFO, "Converting corpus to tuple structure")

    for row in rows:
        result.append(
            list(zip(
                list(map(int, row[::2])),
                list(map(int, row[1::2]))
            ))
        )

    log(INFO, "Ordered coprus parsed")

    return result