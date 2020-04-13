import csv


def readCSV(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        file.close()
        return rows
