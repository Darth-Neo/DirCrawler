#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
import os

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

import logging
logger.setLevel(logging.INFO)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

import nltk
from nltk import tokenize, tag, chunk
from nltk.corpus import webtext
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer, WordNetLemmatizer

class Collocations(object):
    concepts         = None
    
    conceptsNGram        = None
    conceptNGramScore    = None
    conceptsNGramSubject = None

    conceptFile      = u"documents.p"

    ngramFile        = u"ngrams.p"
    ngramScoreFile   = u"ngramscore.p"
    ngramSubjectFile = u"ngramsubject.p"
    
    def __init__(self, conceptFile=None):
        if conceptFile == None:
            conceptFile      = u"documents.p"

        logger.info(u"Load Concepts from %s " % (conceptFile))
        self.concepts = Concepts.loadConcepts(conceptFile)
        logger.info(u"Loaded Concepts")

        self.conceptsNGram = Concepts(u"n-gram", u"NGRAM")
        self.conceptsNGramScore = Concepts(u"NGram_Score", u"Score")
        self.conceptsNGramSubject = Concepts(u"Subject", u"Subjects")

    def getCollocationConcepts(self):
        return self.conceptsNGram, self.conceptsNGramScore, self.conceptsNGramSubject
        
    def find_collocations(self):
        lemmatizer = WordNetLemmatizer()

        stopset = set(stop)
        filter_stops = lambda w: len(w) < 3 or w in stopset

        words = list()

        dictWords = dict()

        for document in self.concepts.getConcepts().values():
            logger.debug(document.name)
            for concept in document.getConcepts().values():
               logger.debug(concept.name)

               for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(concept.name)):
                    logger.debug(u"Word: " + word + u" POS: " + pos)
                    lemmaWord = lemmatizer.lemmatize(word.lower())
                    logger.debug(u"Word: " + word + u" Lemma: " + lemmaWord)
                    words.append(lemmaWord)

                    if pos[0] == u"N":
                        dictWords[lemmaWord] = word


        for x in dictWords.keys():
            logger.info(u"noun : %s" % x)

        bcf = BigramCollocationFinder.from_words(words)
        tcf = TrigramCollocationFinder.from_words(words)

        bcf.apply_word_filter(filter_stops)
        tcf.apply_word_filter(filter_stops)
        tcf.apply_freq_filter(3)

        listBCF = bcf.nbest(BigramAssocMeasures.likelihood_ratio, 100)

        for bigram in listBCF:
            concept = u' '.join([bg for bg in bigram])
            e = self.conceptsNGram.addConceptKeyType(concept, u"BiGram")
            logger.info(u"Bigram  : %s" % concept)
            for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(concept)):
                e.addConceptKeyType(word, pos)

        listTCF = tcf.nbest(TrigramAssocMeasures.likelihood_ratio, 100)

        for trigram in listTCF:
            concept = u' '.join([bg for bg in trigram])
            e = self.conceptsNGram.addConceptKeyType(concept, u"TriGram")
            logger.info(u"Trigram : %s" % concept)
            for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(concept)):
                e.addConceptKeyType(word, pos)
            
        bcfscored = bcf.score_ngrams(BigramAssocMeasures.likelihood_ratio)
        lt = sorted(bcfscored, key=lambda c: c[1], reverse=True)
        for score in lt:
            name = ' '.join([w for w in score[0]])
            count = float(score[1])
            e = self.conceptsNGramScore.addConceptKeyType(name, u"BiGram")
            for x in score[0]:
                e.addConceptKeyType(x, u"BWord")
            e.count = count
            logger.debug(u"bcfscored: %s=%s" % (name, count))

        tcfscored = tcf.score_ngrams(TrigramAssocMeasures.likelihood_ratio)
        lt = sorted(tcfscored, key=lambda c: c[1], reverse=True)
        for score in lt:
            name = ' '.join([w for w in score[0]])
            count = float(score[1])
            e = self.conceptsNGramScore.addConceptKeyType(name, u"TriGram")
            for x in score[0]:
                e.addConceptKeyType(x, u"TWord")
            e.count = count
            logger.debug(u"tcfscored: %s = %s" % (name, count))

        Concepts.saveConcepts(self.conceptsNGramScore, self.ngramScoreFile)
        Concepts.saveConcepts(self.conceptsNGram, self.ngramFile)

        for concept in self.conceptsNGram.getConcepts().values():
            for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(concept.name)):
                if pos[0] == u"N":
                    e = self.conceptsNGramSubject.addConceptKeyType(word, pos)
                    e.addConceptKeyType(concept.name, u"NGRAM")

        Concepts.saveConcepts(self.conceptsNGramSubject, self.ngramSubjectFile)

if __name__ == u"__main__":
    os.chdir(u"." + os.sep + u"t34_20151004_151638")
    
    # fc = Collocations("documents.p")
    fc = Collocations(u"chunks.p")
    fc.find_collocations()
