import csv
import matplotlib.pyplot as plt


with open('topic_proportions_per_year.csv', 'r') as file:
    rows = list(csv.reader(file))

topic_per_years = {}

for i in range(1, 101):
    topic_per_years[i] = {}


for row in rows[:-1]:
    year = row[0]

    topic_props = enumerate(list(map(float, row[1:])), 1)

    for topic_id, topic_prop in topic_props:

        topic_per_years[topic_id][year] = topic_prop


for i in range(5):
    start_topic = i * 15
    end_topc = start_topic + 15

    plt.figure(figsize=(10,12))

    for index, (topic, props) in list(enumerate(list(topic_per_years.items())))[start_topic:end_topc]:

        plt.subplot(5, 3, index - start_topic + 1)

        plt.title('topic {}'.format(topic))
        plt.grid(axis='y', linestyle='dotted')

        plt.bar(list(props.keys()), list(props.values()))

        plt.xticks([1, 11, 21, 31, 40])
        plt.yticks([0.005, 0.01])

        plt.ylim(ymin=0.005)

    plt.tight_layout(h_pad=1, w_pad=1, pad=2)
    plt.show()
            # plt.savefig("topics_per_years_{}-{}.png".format(topic - 20, topic), dpi=300)
