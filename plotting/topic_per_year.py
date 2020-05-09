import sys
import csv
import matplotlib.pyplot as plt



def single(topic_no, label):

    topic, props = list(topic_per_years.items())[topic_no - 1]
    
    plt.figure(figsize=(3, 3))

    plt.title('topic {}\n\n{}'.format(topic, ',\n'.join(label.replace('_', ' ').split(','))))
    plt.grid(axis='y', linestyle='dotted')
    plt.plot(list(props.keys()), list(props.values()))
    plt.xticks([1, 11, 21, 31, 40])

    yticks = [0.005, 0.010]

    for num in [0.015, 0.020, 0.025]:
        if max(props.values()) > num:
            yticks.append(num)
    yticks.append(yticks[-1] + 0.005)

    plt.yticks(yticks)
    plt.ylim((0.005, yticks[-1]))
    plt.tight_layout(h_pad=1, w_pad=1, pad=1)
    plt.savefig("topic_{}.png".format(topic), dpi=300)


def three(topic_nums, labels):
    plt.figure(figsize=(8, 3))

    base_items = list(topic_per_years.items())
    items = [
        base_items[topic_nums[0] - 1],
        base_items[topic_nums[1] - 1],
        base_items[topic_nums[2] - 1]
    ]

    for index, (topic, props) in enumerate(items):
        
        plt.subplot( 1, 3, index + 1)

        plt.title('topic {}\n\n{}'.format(topic, ',\n'.join(labels[index].replace('_', ' ').split(','))))
        plt.grid(axis='y', linestyle='dotted')

        plt.plot(list(props.keys()), list(props.values()))

        plt.xticks([1, 11, 21, 31, 40])


        yticks = [0.005, 0.010]

        for num in [0.015, 0.020, 0.025]:
            if max(props.values()) > num:
                yticks.append(num)
        yticks.append(yticks[-1] + 0.005)

        plt.yticks(yticks)

        plt.ylim((0.005, yticks[-1]))

    plt.tight_layout(h_pad=1, w_pad=1, pad=1)
    plt.savefig("topics_per_years_{}.png".format(topic_nums), dpi=300)

def two(topic_nums, labels):
    plt.figure(figsize=(5.3, 3))

    base_items = list(topic_per_years.items())
    items = [
        base_items[topic_nums[0] - 1],
        base_items[topic_nums[1] - 1]
    ]

    for index, (topic, props) in enumerate(items):
        
        plt.subplot( 1, 2, index + 1)

        plt.title('topic {}\n\n{}'.format(topic, ',\n'.join(labels[index].replace('_', ' ').split(','))))
        plt.grid(axis='y', linestyle='dotted')

        plt.plot(list(props.keys()), list(props.values()))

        plt.xticks([1, 11, 21, 31, 40])


        yticks = [0.005, 0.010]

        for num in [0.015, 0.020, 0.025]:
            if max(props.values()) > num:
                yticks.append(num)
        yticks.append(yticks[-1] + 0.005)

        plt.yticks(yticks)

        plt.ylim((0.005, yticks[-1]))

    plt.tight_layout(h_pad=1, w_pad=1, pad=1)
    plt.savefig("topics_per_years_{}.png".format(topic_nums), dpi=300)


def five_rows():
    for i in range(20):
        start_topic = i * 5
        end_topic = start_topic + 5

        plt.figure(figsize=(3, 12))

        for index, (topic, props) in list(enumerate(list(topic_per_years.items())))[start_topic:end_topic]:
            

            plt.subplot(5, 1, index - start_topic + 1)

            plt.title('topic {}'.format(topic))
            plt.grid(axis='y', linestyle='dotted')

            plt.plot(list(props.keys()), list(props.values()))

            plt.xticks([1, 11, 21, 31, 40])


            yticks = [0.005, 0.010]

            for num in [0.015, 0.020, 0.025]:
                if max(props.values()) > num:
                    yticks.append(num)
            yticks.append(yticks[-1] + 0.005)

            plt.yticks(yticks)

            plt.ylim((0.005, yticks[-1]))

        plt.tight_layout(h_pad=1, w_pad=1, pad=1)
        plt.savefig("rows/topics_per_years_{}-{}.png".format(start_topic + 1, min(end_topic, 100)), dpi=300)



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


# try:
count = int(sys.argv[1])

if count == 1:
    topic_no = int(sys.argv[2])
    label = sys.argv[3]
    single(topic_no, label)
elif count == 2:
    topic_nums = list(map(int, sys.argv[2:4]))

    labels = sys.argv[4:6]
    
    two(topic_nums, labels)
elif count == 3:
    topic_nums = list(map(int, sys.argv[2:5]))

    labels = sys.argv[5:8]
    
    three(topic_nums, labels)

elif count == 5:
    five_rows()

# except Exception as e:
#     print('Specify count and topic numbers from command line', e)



