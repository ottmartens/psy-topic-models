import csv
from datetime import datetime
import ast
from collections import defaultdict


def writeCSV(file_name, data):
    with open(file_name, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        file.close()


def readCSV(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        file.close()

        ids = [row[0] for row in rows]
        texts = [ast.literal_eval(row[1]) for row in rows]

        return ids, texts


def readMultiterms():

    with open('wordnet_multiword_terms.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

        multitermDict = defaultdict(list)

        for row in rows:
            term = row[0].lower()
            key = term[0]

            multitermDict[key].append(term)

        file.close()

    return multitermDict
