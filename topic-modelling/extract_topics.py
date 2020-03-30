import gensim
import csv
import sys

model_name = sys.argv[1]

mallet_lda_model = gensim.models.utils.SaveLoad.load('models/{}'.format(model_name))

topics = mallet_lda_model.show_topics(formatted=False, num_topics=25)

topic_file_path = 'models/{}_topics.csv'.format(model_name)

with open(topic_file_path, 'w') as file:
    writer = csv.writer(file)

    header = []
    for i in range(25):
        header.extend((i+1, 'prob'))

    writer.writerow(header)

    for i in range(10):
        row = []
        for topic in topics:
            word = topic[1][i][0]
            prob = topic[1][i][1]
            row.extend((word, round(prob, 4)))
        writer.writerow(row)

print('Wrote topics to result file {}'.format(topic_file_path))

