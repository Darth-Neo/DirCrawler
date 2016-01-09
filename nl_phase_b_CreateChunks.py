#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Natural Language Processing of PMO Information
#
import os

from nl_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts
from nl_lib.Constants import *

import nltk
from nltk import tokenize, tag, chunk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from itertools import islice
from pattern.vector import count, words, PORTER, LEMMA
from pattern.vector import Document, Model, TFIDF, HIERARCHICAL
from pattern.vector import Vector, distance, NB
from pattern.db import csv
from pattern.en import parse, Sentence, parsetree


class Chunks(object):
    
    conceptFile = u'documents.p'
    chunkFile = u'chunks.p'
    concepts = None
    chunkConcepts = None
    
    def __init__(self, concepts=None):
        if concepts is None:
            logger.info(u"Loading : %s" % self.conceptFile)
            self.concepts = Concepts.loadConcepts(self.conceptFile)
        else:
            logger.info(u"Using   : %s" % concepts.name)
            self.concepts = concepts

        self.chunkConcepts = Concepts(u"Chunk", u"Chunks")

    def getChunkConcepts(self):
        return self.chunkConcepts
      
    def createChunks(self):  
        stop = stopwords.words(u'english')
        stop.append(u"This")
        stop.append(u"The")
        stop.append(u",")
        stop.append(u".")
        stop.append(u"..")
        stop.append(u"...")
        stop.append(u".")
        stop.append(u";")
        stop.append(u"and")

        stemmer = PorterStemmer()
        lemmatizer = WordNetLemmatizer()
        tokenizer = RegexpTokenizer(u"[\w]+")
        
        for document in self.concepts.getConcepts().values():
            logger.debug(u"%s" % document.name)
            d = self.chunkConcepts.addConceptKeyType(document.name, u"Document")
            
            for sentence in document.getConcepts().values():
                logger.debug(u"%s(%s)" % (sentence.name, sentence.typeName))
                cleanSentence = ' '.join([word for word in sentence.name.split() if word not in stop])

                listSentence = list()

                for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(cleanSentence)):                
                    logger.debug(u"Word: " + word + u" POS: " + pos)

                    if pos[:1] == u"N":
                    # if True:
                        lemmaWord = lemmatizer.lemmatize(word)
                        logger.debug(u"Word: " + word + u" Lemma: " + lemmaWord)

                        morphWord = wn.morphy(word, wn.NOUN)
                        if morphWord is not None:
                            logger.debug(u"Word: " + word + u" Morph: " + morphWord)

                        synset = wn.synsets(word, pos=u'n')
                        logger.debug(u"synset : %s" %  synset)

                        if len(synset) != 0:
                            syn = synset[0]

                            root = syn.root_hypernyms()
                            logger.debug(u"root : %s" % root)

                            mh = syn.member_holonyms()
                            logger.debug(u"member_holonyms : %s" % mh)

                            hypernyms = syn.hypernyms()
                            logger.debug(u"hypernyms : %s" % hypernyms)

                            if len(hypernyms) > 0:
                                hyponyms = syn.hypernyms()[0].hyponyms()
                                logger.debug(u"hyponyms : %s" % hyponyms)
                            else:
                                hyponyms = None
                                
                            listSentence.append((word, lemmaWord, pos, root, hypernyms, hyponyms))

                nounSentence = u""
                for word in listSentence:
                    nounSentence += word[1] + u" "
                    
                if len(nounSentence) > 2:
                    e = d.addConceptKeyType(nounSentence, u"NounSentence")

                    for word in listSentence:
                        f = e.addConceptKeyType(word[0], word[2])
                        f.addConceptKeyType(word[1], u"Lemma")
                
                logger.debug(u"%s = %s" % (cleanSentence, type(cleanSentence)))
                cleanSentence = cleanSentence.encode(u"utf-8", errors=u"ignore")
                cleanSentence = cleanSentence.decode(u"ascii", errors=u"ignore")

                pt = parsetree(cleanSentence, relations=True, lemmata=True)

                for sentence in pt:
                    logger.debug(u"relations: %s" % [x for x in sentence.relations])
                    logger.debug(u"subject  : %s" % [x for x in sentence.subjects])
                    logger.debug(u"verb     : %s" % [x for x in sentence.verbs])
                    logger.debug(u"object   : %s" % [x for x in sentence.objects])
                    
                    if sentence.subjects is not None:
                        logger.debug(u"Sentence : %s" % sentence.chunks)
                        
                        for chunk in sentence.chunks:
                            logger.debug(u"Chunk  : %s" % chunk)
                        
                            relation = unicode(chunk.relation).strip()  #.encode("ascii", errors="ignore").strip()
                            role = unicode(chunk.role).strip()  # .encode("ascii", errors="ignore").strip()

                            logger.debug(u"Relation : %s" % relation)
                            logger.debug(u"Role     : %s" % role)

                            for subject in sentence.subjects:
                                logger.debug(u"Subject.realtion : %s " % subject.relation)
                                logger.debug(u"Subject : %s " % subject.string)
                                f = e.addConceptKeyType(subject.string, u"SBJ")
                                
                                for verb in sentence.verbs:
                                    if verb.relation == subject.relation:
                                        logger.debug(u"Verb.realtion : %s " % verb.relation)
                                        logger.debug(u"Verb   : %s " % verb.string)
                                        g = f.addConceptKeyType(verb.string, u"VP")

                                        for obj in sentence.objects:
                                            if obj.relation == verb.relation:
                                                logger.debug(u"Obj.realtion : %s " % obj.relation)
                                                logger.debug(u"Object : %s " % obj.string)
                                                g.addConceptKeyType(obj.string, u"OBJ")
                            
        Concepts.saveConcepts(self.chunkConcepts, self.chunkFile)

if __name__ == u"__main__":

    os.chdir(u"test")

    chunks = Chunks()
    
    chunks.createChunks()

            



