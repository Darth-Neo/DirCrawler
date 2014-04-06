#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
import os
from nl_lib.Constants import *
from nl_lib import Logger
from nl_lib.Concepts import Concepts

import nltk
from nltk import tokenize, tag, chunk
from nltk.corpus import webtext
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer, WordNetLemmatizer

logger = Logger.setupLogging(__name__)
   
if __name__ == "__main__":
    conceptFile = "documents.p"

    stop = stopwords.words('english')
    stop.append("This")
    stop.append("The")
    stop.append(",")
    stop.append(".")
    stop.append("..")
    stop.append("...")
    stop.append(".")
    stop.append(";")
    stop.append("/")
    stop.append(")")
    stop.append("(")
    stop.append("must")
    stop.append("system")

    lemmatizer = WordNetLemmatizer()

    stopset = set(stop)
    filter_stops = lambda w: len(w) < 3 or w in stopset

    conceptNGram = Concepts("n-gram", "NGRAM")

    logger.info("Loading :" + os.getcwd() + os.sep + conceptFile)
    concepts = Concepts.loadConcepts(conceptFile)

    words = list()

    for document in concepts.getConcepts().values():
        logger.debug(document.name)
        for concept in document.getConcepts().values():
           logger.debug(concept.name)

           for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(concept.name)):
                logger.debug("Word: " + word + " POS: " + pos)
                lemmaWord = lemmatizer.lemmatize(word.lower())
                logger.debug("Word: " + word + " Lemma: " + lemmaWord)
                words.append(lemmaWord)

    bcf = BigramCollocationFinder.from_words(words)
    tcf = TrigramCollocationFinder.from_words(words)

    bcf.apply_word_filter(filter_stops)
    tcf.apply_word_filter(filter_stops)
    tcf.apply_freq_filter(3)

    listBCF = bcf.nbest(BigramAssocMeasures.likelihood_ratio, 100)

    for bigram in listBCF:
        concept = ' '.join([bg for bg in bigram])
        e = conceptNGram.addConceptKeyType(concept, "BiGram")
        logger.info("Bigram  : %s" % concept)
        for x in concept.split():
            e.addConceptKeyType(x, "BWord")

    listTCF = tcf.nbest(TrigramAssocMeasures.likelihood_ratio, 100)

    for trigram in listTCF:
        concept = ' '.join([bg for bg in trigram])
        e = conceptNGram.addConceptKeyType(concept, "TriGram")
        for x in concept.split():
            e.addConceptKeyType(x, "TWord")
        logger.info("Trigram : %s" % concept)

    conceptScore = Concepts("NGram_Score", "Score")

    bcfscored = bcf.score_ngrams(BigramAssocMeasures.likelihood_ratio)
    lt = sorted(bcfscored, key=lambda c: c[1], reverse=True)
    for score in lt:
        name = ' '.join([w for w in score[0]])
        count = float(score[1])
        e = conceptScore.addConceptKeyType(name, "BiGram")
        for x in score[0]:
            e.addConceptKeyType(x, "BWord")
        e.count = count
        logger.info("bcfscored: %s=%s" % (name, count))

    tcfscored = tcf.score_ngrams(TrigramAssocMeasures.likelihood_ratio)
    lt = sorted(tcfscored, key=lambda c: c[1], reverse=True)
    for score in lt:
        name = ' '.join([w for w in score[0]])
        count = float(score[1])
        e = conceptScore.addConceptKeyType(name, "TriGram")
        for x in score[0]:
            e.addConceptKeyType(x, "TWord")
        e.count = count
        logger.info("tcfscored: %s = %s" % (name, count))

    Concepts.saveConcepts(conceptScore, "ngramscore.p")
    Concepts.saveConcepts(conceptNGram, "ngrams.p")
