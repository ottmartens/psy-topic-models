import csv
from datetime import datetime
import ast


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
