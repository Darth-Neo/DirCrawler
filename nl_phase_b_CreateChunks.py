#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Natural Language Processing of PMO Information
#
import os

from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.Constants import *

import nltk
from nltk import tokenize, tag, chunk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

from pattern.vector import count, words, PORTER, LEMMA
from pattern.vector import Document, Model, TFIDF, HIERARCHICAL
from pattern.vector import Vector, distance, NB
from pattern.db import csv
from pattern.en import parse, Sentence, parsetree

logger = Logger.setupLogging(__name__)
      
def createChunks():
    conceptFile = 'documents.p'
    
    logger.info("Loading :" + conceptFile)
    concepts = Concepts.loadConcepts(conceptFile)

    stop = stopwords.words('english')

    stop.append("This")
    stop.append("The")
    stop.append(",")
    stop.append(".")
    stop.append("..")
    stop.append("...")
    stop.append(".")
    stop.append(";")
    stop.append("and")

    chunkConcepts = Concepts("Chunk", "Chunks")

    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    
    for document in concepts.getConcepts().values():
        logger.info("%s" % document.name)
        d = chunkConcepts.addConceptKeyType(document.name, "Document")
        
        for sentence in document.getConcepts().values():
            logger.debug("%s(%s)" % (sentence.name, sentence.typeName))
            cleanSentence = ' '.join([word for word in sentence.name.split() if word not in stop])

            listSentence = list()
            
            for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(cleanSentence)):
                logger.debug("Word: " + word + " POS: " + pos)

                if pos[:1] == "N":
                    lemmaWord = lemmatizer.lemmatize(word)
                    logger.debug("Word: " + word + " Lemma: " + lemmaWord)

                    synset = wn.synsets(word, pos='n')
                    logger.debug("synset : %s" %  synset)

                    if len(synset) != 0:
                        syn = synset[0]

                        root = syn.root_hypernyms()
                        logger.debug("root : %s" %  root)

                        hypernyms = syn.hypernyms()
                        logger.debug("hypernyms : %s" %  hypernyms)

                        if len(hypernyms) > 0:
                            hyponyms = syn.hypernyms()[0].hyponyms()
                            logger.debug("hyponyms : %s" %  hyponyms)
                        else:
                            hyponyms = None
                            
                        listSentence.append((word, lemmaWord, root, hypernyms, hyponyms))

            nounSentence = ""
            for word in listSentence:
                nounSentence += word[1] + " "
                
            if len(nounSentence) > 2:
                e = d.addConceptKeyType(nounSentence, "NounSentence")

                for word in listSentence:
                    f = e.addConceptKeyType(word[0], "Word")
                    f.addConceptKeyType(word[1], "Lemma")
                
            pt = parsetree(cleanSentence, relations=True, lemmata=True)

            for sentence in pt:
                logger.debug("relations: %s" % [x for x in sentence.relations])
                logger.debug("subject  : %s" % [x for x in sentence.subjects])
                logger.debug("verb     : %s" % [x for x in sentence.verbs])
                logger.debug("object   : %s" % [x for x in sentence.objects])
                
                if sentence.subjects is not None:
                    logger.debug("Sentence : %s" % sentence.chunks)
                    
                    for chunk in sentence.chunks:
                        logger.debug("Chunk  : %s" % chunk)
                    
                        relation = str(chunk.relation).encode("utf-8").strip()
                        role = str(chunk.role).encode("utf-8").strip()

                        logger.debug("Relation : %s" % relation)
                        logger.debug("Role     : %s" % role)

                        for subject in sentence.subjects:
                            logger.debug("Subject.realtion : %s " % subject.relation)
                            logger.debug("Subject : %s " % subject.string)
                            f = e.addConceptKeyType(subject.string, "SBJ")
                            
                            for verb in sentence.verbs:
                                if verb.relation == subject.relation:
                                    logger.debug("Verb.realtion : %s " % verb.relation)
                                    logger.debug("Verb   : %s " % verb.string)
                                    g = f.addConceptKeyType(verb.string, "VP")

                                for obj in sentence.objects:
                                    if obj.relation == verb.relation:
                                        logger.debug("Obj.realtion : %s " % obj.relation)
                                        logger.debug("Object : %s " % obj.string)
                                        g.addConceptKeyType(obj.string, "OBJ")
                    
    Concepts.saveConcepts(chunkConcepts, "chunks.p")

if __name__ == "__main__":
    createChunks()

            



