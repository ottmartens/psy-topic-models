import gensim
import logging
from logging import log, INFO

from parse_corpus import read_corpus_from_file

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=INFO)

model = gensim.utils.SaveLoad.load('models/model_100')

corpus = read_corpus_from_file()

model = model[corpus]


with open("document_topic_props.csv", "w") as file:
    writer = csv.writer(file)

    for i, doc in enumerate(model):
        
        if i % 10000 == 0:
            log(INFO, "Processed {} documents".format(i))

        writer.writerow([topic_prop for (topic_no, topic_prop) in doc])
        
    file.close()
    
log(INFO, "Finished")

