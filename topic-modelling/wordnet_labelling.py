import sys
import gensim
from nltk.corpus import wordnet as wn

from utils import *

# Hypernyms that by empirical investigation occur too often and provide no insight in terms of labelling


def get_absolute_depth(synset):
    return min([len(path) for path in synset.hypernym_paths()])


def get_stop_hypernyms():
    stop_words = ["physical_entity", "entity"]

    stop_hypernyms = []

    for word in stop_words:
        stop_hypernyms += wn.synsets(word, pos='n')

    return stop_hypernyms


def triplets(synsets):
    common_hypernyms = set()

    for first_synset in synsets[0]:
        for second_word in synsets[1:]:
            for second_synset in second_word:
                for third_word in synsets[1:]:
                    for third_synset in third_word:

                        if second_word != third_word:

                            two_word_hypernyms = first_synset.lowest_common_hypernyms(
                                second_synset)

                            for hypernym in two_word_hypernyms:
                                three_word_hypernyms = hypernym.lowest_common_hypernyms(
                                    third_synset)

                                common_hypernyms.update(three_word_hypernyms)

    common_hypernyms = list(
        filter(lambda word: word not in stop_hypernyms, common_hypernyms))

    return find_lowest_hypernym(common_hypernyms)


def all_combinations_higher_than_threshold(synsets, threshold, probs):

    synsets = list(map(lambda entry: entry[0],
                       filter(lambda entry: entry[1] > threshold,
                              zip(synsets, probs))))

    common_hypernyms = set()

    for first_word in synsets:
        for first_synset in first_word:
            for second_word in synsets:
                for second_synset in second_word:
                    if second_word != first_word:
                        hypernyms = first_synset.lowest_common_hypernyms(
                            second_synset)

                        common_hypernyms.update(hypernyms)

    common_hypernyms = list(
        filter(lambda word: word not in stop_hypernyms, common_hypernyms))

    return find_lowest_hypernym(common_hypernyms)


def top_word_plus_highest_match(synsets):

    common_hypernyms = set()

    for first_synset in synsets[0]:
        for second_word in synsets[1:]:
            for second_synset in second_word:
                hypernyms = first_synset.lowest_common_hypernyms(second_synset)

                common_hypernyms.update(hypernyms)

    common_hypernyms = list(
        filter(lambda word: word not in stop_hypernyms, common_hypernyms))

    return find_lowest_hypernym(common_hypernyms)


def find_lowest_hypernym(hypernyms):

    lowest = None
    min_distance = 0

    for hypernym in hypernyms:
        distance_from_root = get_absolute_depth(hypernym)

        if distance_from_root > min_distance:
            lowest = hypernym
            min_distance = distance_from_root

    return lowest


model_name = sys.argv[1]

model = gensim.utils.SaveLoad.load("models/{}".format(model_name))

topics = model.show_topics(formatted=False, num_topics=100)

stop_hypernyms = get_stop_hypernyms()


print("\n{:<5} {:<26} {:<5} {:<26} {:<5} {:<26} {:<5} {:<26}\n".format(
    "Topic", "Top word + highest", "depth", "Combinations > thresh", "depth", "triplets", "depth", "Picked result"))


result = []

for topic in topics:

    topic_nr = topic[0] + 1

    topic_words = list(map(lambda entry: entry[0], topic[1]))

    topic_word_probs = list(map(lambda entry: entry[1], topic[1]))

    topic_word_synsets = list(
        map(lambda word: wn.synsets(word, pos='n'), topic_words))

    label_1 = top_word_plus_highest_match(topic_word_synsets)
    if label_1 is None:
        string_1 = ""
        depth_1 = "-"
    else:
        string_1 = label_1.lemma_names()[0]
        depth_1 = get_absolute_depth(label_1)

    label_2 = all_combinations_higher_than_threshold(
        topic_word_synsets, 0.03, topic_word_probs)
    if label_2 is None:
        string_2 = ""
        depth_2 = "-"
    else:
        string_2 = label_2.lemma_names()[0]
        depth_2 = get_absolute_depth(label_2)

    label_3 = triplets(topic_word_synsets)
    if label_3 is None:
        string_3 = ""
        depth_3 = "-"
    else:
        string_3 = label_3.lemma_names()[0]
        depth_3 = get_absolute_depth(label_3)
    
    
    if label_1 is None:
        picked = string_2
    elif label_2 is None:
        picked = string_1


    # Pick label from model 2 if specificity is significantly higher
    elif (depth_2 - depth_1) > 2:
        picked = string_2

    # Default to the first model
    else:
        picked = string_1


    print("{:<5} {:<26} {:<5} {:<26} {:<5} {:<26} {:<5} {:<26}".format(
        topic_nr, string_1, depth_1, string_2, depth_2, string_3, depth_3, picked))
    
    result.append([topic_nr, string_1, string_2, string_3, picked])

    


with open('result-files/wordnet_labels.csv', 'w') as file:
    writer = csv.writer(file)

    writer.writerow(["topic_no", "first_plus_highest", "above_3%", "triplets", "picked"])

    writer.writerows(result)

    file.close()