import gensim
from gensim.utils import simple_preprocess
import spacy
from nltk.corpus import stopwords
import logging
from logging import log, INFO

from utils import *

stop_words = stopwords.words('english')
en_model = spacy.load('en', disable=['parser', 'textcat'])


def removeStopwords(texts):
    return [[word for word in simple_preprocess(abstract, deacc=True, min_len=3) if word not in stop_words] for abstract in texts]


def makeNGrgrams(texts, bigramPhraser, trigramPhraser):
    return [trigramPhraser[bigramPhraser[abstract]] for abstract in texts]


def applyWordnetMultiterms(texts, multitermDict):
    result = []

    for text in texts:
        resultText = []
        for index, word in enumerate(text):
            if index == 0:
                resultText.append(word)
            else:
                lastword = resultText[-1]
                multiterm = "{}_{}".format(lastword, word)
                key = multiterm[0]

                if multitermDict.get(key) != None and multiterm in multitermDict.get(key):
                    resultText[-1] = multiterm
                else:
                    resultText.append(word)

        result.append(resultText)

    count = 0
    for text, newText in list(zip(texts, result)):
        count += abs(len(text) - len(newText))

    log(INFO, "Found total of {} multiterms with wordnet samples".format(count))

    return result


def lemmatize(texts, allowed_token_tags=['NNP', 'NNS' 'NN']):

    result = []
    for abstract in texts:
        doc = en_model(" ".join(abstract))

        lemmas = [
            token.lemma_ for token in doc if token.tag_ in allowed_token_tags]

        result.append(lemmas)

    return result


def generatePhrasers(texts, min_count, threshold):
    bigram = gensim.models.Phrases(texts, min_count=5, threshold=treshold)
    trigram = gensim.models.Phrases(bigram[texts], threshold=threshold)

    bigramPhraser = gensim.models.phrases.Phraser(bigram)
    trigramPhraser = gensim.models.phrases.Phraser(trigram)

    return bigramPhraser, trigramPhraser


def createDictionary(texts):
    return gensim.corpora.Dictionary(texts)


def createCorpus(id2word, texts):
    return [id2word.doc2bow(text) for text in texts]
