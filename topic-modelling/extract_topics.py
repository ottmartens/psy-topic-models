import gensim
import csv
import sys


try:
    model_name = sys.argv[1]
    num_topics = int(sys.argv[2])
except:
    print('Specify model name and number of topics as arguments')
    exit(1)

mallet_lda_model = gensim.models.utils.SaveLoad.load(
    'models/{}'.format(model_name))

topics = mallet_lda_model.show_topics(formatted=False, num_topics=num_topics)

topic_file_path = 'result-files/{}_topics.csv'.format(model_name)

with open(topic_file_path, 'w') as file:
    writer = csv.writer(file)

    for topic in topics:

        writer.writerow([])
        writer.writerow([topic[0] + 1])

        for i in range(10):

            word = topic[1][i][0]
            prob = topic[1][i][1]

            writer.writerow((word, round(prob * 100, 4)))

    file.close()

print('Wrote topics to result file {}'.format(topic_file_path))
