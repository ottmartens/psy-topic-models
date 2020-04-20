import csv
import logging
from logging import log, INFO

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=INFO)


log(INFO, "Parsing ids per year")
with open("ids_per_year.csv", "r") as file:
    ids_per_year = list(
        map(lambda row: (row[0], row[1:]), list(csv.reader(file))))
    file.close()

log(INFO, "Parsing document topic proportions")
with open("document_topic_props.csv", "r") as file:
    rows = list(csv.reader(file))
    document_topic_props = [list(map(float, row))
                            for row in rows]
    file.close()

log(INFO, "Parsing document ids")
with open("ids.csv", "r") as file:
    ids = list(map(int, list(csv.reader(file))[0]))
    file.close()

topic_props_per_year = {}

log(INFO, "Aggregating topic proportions for each year")
with open("result-files/topic_proportions_per_year.csv", "w") as file:

    writer = csv.writer(file)

    for (year, year_ids) in ids_per_year:

        topic_props_per_year[year] = dict()

        doc_count_in_year = len(year_ids)

        log(INFO, "Year {}".format(year))

        for i in range(1, 101):
            topic_props_per_year[year][i] = 0

        for doc_id in year_ids:
            doc_id = int(doc_id)

            index = ids.index(doc_id)

            doc_topic_props = document_topic_props[index]

            for index, topic_prop in enumerate(doc_topic_props):
                topic_nr = index + 1

                topic_props_per_year[year][topic_nr] += topic_prop

        for i in range(1, 101):
            topic_props_per_year[year][i] /= doc_count_in_year

        writer.writerow([year] + list(topic_props_per_year[year].values()))

    file.close()

log(INFO, "Finished")