import gensim
from gensim.utils import simple_preprocess
import spacy
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
stop_words.extend(['man', 'use', 'one', 'two', 'year', 'also', 'set', 'like'])

en_model = spacy.load('en', disable=['ner', 'parser'])
en_model.add_pipe(en_model.create_pipe('sentencizer'))


def removeStopwords(texts):
    return [[word for word in simple_preprocess(abstract, deacc=True, min_len=3) if word not in stop_words] for abstract in texts]


def makeBigrams(texts, bigramPhraser):
    return [bigramPhraser[abstract] for abstract in texts]


def makeTrigrams(texts, bigramPhraser, trigramPhraser):
    return [trigramPhraser[bigramPhraser[abstract]] for abstract in texts]


def lemmatize(texts):
    return [[token.lemma_ for token in en_model(" ".join(abstract)) if token.tag_ != 'NNPS'] for abstract in texts]


def generatePhrasers(texts, min_count, threshold):
    bigram = gensim.models.Phrases(texts, min_count=5, threshold=50)
    trigram = gensim.models.Phrases(bigram[texts], threshold=50)

    bigramMod = gensim.models.phrases.Phraser(bigram)
    trigramMod = gensim.models.phrases.Phraser(trigram)

    return bigramMod, trigramMod


def createDictionary(texts):
    return gensim.corpora.Dictionary(texts)


def createCorpus(id2word, texts):
    return [id2word.doc2bow(text) for text in texts]
