#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Natural Language Processing of PMO Information
#
import os

from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.Constants import *

from pattern.vector import count, words, PORTER, LEMMA
from pattern.vector import Document, Model, TFIDF, HIERARCHICAL
from pattern.vector import Vector, distance, NB
from pattern.db import csv
from pattern.en import parse, Sentence, parsetree

logger = Logger.setupLogging(__name__)

def printChunks(chunks):
    for chunk in chunks:
            print("Chunk %s: .%s." % (chunk.type, chunk)) 
            wordChunk = chunk.string

            for word in chunk.words:
                print("word: .%s." % (word)) 
                synsetsWordNet(word)

def printSentence(sentence):
    print("sentence.string .%s." % sentence.string)             # Tokenized string, without tags.
    print("sentence.words .%s." % sentence.words)               # List of Word objects.
    print("sentence.lemmata .%s." % sentence.lemmata)           # List of word lemmata.
    print("sentence.chunks .%s." % sentence.chunks)             # List of Chunk objects.
    print("sentence.subjects .%s." % sentence.subjects)         # List of NP-SBJ chunks.
    print("sentence.objects .%s." % sentence.objects)           # List of NP-OBJ chunks.
    print("sentence.verbs .%s." % sentence.verbs)               # List of VP chunks.
    print("sentence.relations .%s." % sentence.relations)       # {'SBJ': {1: Chunk('the cat/NP-SBJ-1')},
                                                                #  'VP': {1: Chunk('sat/VP-1')},
                                                                #  'OBJ': {}} 
def synsetsWordNet(word):
    s = wordnet.synsets(word)[0]

    logger.info("\tDefinition: %s" % s.gloss)
    logger.info("\t Synonyms : %s" % s.synonyms)
    logger.info("\t Hypernyms: %s" % s.hypernyms())
    logger.info("\t Hyponyms : %s" % s.hyponyms())
    logger.info("\t Holonyms : %s" % s.holonyms())
    logger.info("\t Meronyms : %s" % s.meronyms())

def printExamples():
    s =  "The shuttle Discovery, already delayed three times by technical problems and bad weather, was grounded again Friday, this "
    s += "time by a potentially dangerous gaseous hydrogen leak in a vent line attached to the ship's external tank. The Discovery "
    s += "was initially scheduled to make its 39th and final flight last Monday, bearing fresh supplies and an intelligent robot for "
    s += "the International Space Station. But complications delayed the flight from Monday to Friday,  when the hydrogen leak led NASA "
    s += "to conclude that the shuttle would not be ready to launch before its flight window closed this Monday."
    print("Stemming")
    print("PORTER ", count(words(s), stemmer=PORTER))
    #print("LEMMA  ", count(words(s), stemmer=LEMMA))
    print
    print("Keywords")
    d = Document(s, threshold=1)
    for x in d.keywords(top=10):
        print("%2.4f = %s" % (x[0], x[1]))
    print
    print("Sentence")
    sent = Sentence(parse(s))
    for chunk in sent.chunks:
        print("%s.%s.%s." % (chunk.head, chunk.string, chunk.type))

def printVectorModel():
    print("Vector Distance")
    v1 = Vector({"curiosity": 1, "kill": 1, "cat": 1})
    v2 = Vector({"curiosity": 1, "explore": 1, "mars": 1})
    print(1 - distance(v1, v2))
    print
    print ("Vector Example")
    d1 = Document('A tiger is a big yellow cat with stripes.', type='tiger')
    d2 = Document('A lion is a big yellow cat with manes.', type='lion',)
    d3 = Document('An elephant is a big grey animal with a slurf.', type='elephant')
    print d1.vector, d2.vector, d3.vector
    print
    print("Similarity")
    m = Model(documents=[d1, d2, d3], weight=TFIDF)
    print m.similarity(d1, d2) # tiger vs. lion
    print m.similarity(d1, d3) # tiger vs. elephant
    print
    print ("Model Example")
    d1 = Document('The cat purrs.', name='cat1')
    d2 = Document('Curiosity killed the cat.', name='cat2')
    d3 = Document('The dog wags his tail.', name='dog1')
    d4 = Document('The dog is happy.', name='dog2')
    
    m = Model([d1, d2, d3, d4])
    m.reduce(2)
    
    for d in m.documents:
        print
        print d.name
        for concept, w1 in m.lsa.vectors[d.id].items():
            for feature, w2 in m.lsa.concepts[concept].items():
                if w1 != 0 and w2 != 0:
                    print("%s = %2.3f" % (feature, w1 * w2))

    print
    print ("Cluster Example")
    d1 = Document('Cats are independent pets.', name='cat')
    d2 = Document('Dogs are trustworthy pets.', name='dog')
    d3 = Document('Boxes are made of cardboard.', name='box')
    
    m = Model((d1, d2, d3))
    print m.cluster(method=HIERARCHICAL, k=2)


def trainClassifier():
   
    nb = NB()
    for review, rating in csv('reviews.csv'):
        v = Document(review, type=int(rating), stopwords=True)
        nb.train(v)
    
    print nb.classes
    print nb.classify(Document('A good movie!'))

    data = csv('reviews.csv')
    data = [(review, int(rating)) for review, rating in data]
    data = [Document(review, type=rating, stopwords=True) for review, rating in data]
    
    nb = NB(train=data[:500])
    
    accuracy, precision, recall, f1 = nb.test(data[500:])
    print accuracy

def getChunkWords(chunk, role, ID):
    if chunk.relation == ID and chunk.role == role:
        print("Chunk[%s] : .%s.%s.%s" % (chunk.type , [w.string for w in chunk.words], chunk.relation, chunk.role))

def printList(pl, n = 0, pt=None):
    if pt == None:
        pt = ""
        
    n += 1
    if isinstance(pl, list):
        for l in pl:
            pt += printList(l) + " "
    else:
        spaces = " " * n
        pti = pl[0]
        return pl[0]

    return pt
        
if __name__ == "__main__":

    #printExamples()

    conceptFile = 'chunks.p'
    
    logger.info("Loading :" + conceptFile)
    concepts = Concepts.loadConcepts(conceptFile)

    stop.append("This")
    stop.append("The")

    chunkConcepts = Concepts("NVPChunk", "NVPChunks")

    for document in concepts.getConcepts().values():
        d = chunkConcepts.addConceptKeyType(document.name, "Document") 
        for x in document.getConcepts().values():
            #print("x:%s(%s)" % (x.name, x.typeName))

            cleanSentence = ' '.join([word for word in x.name.split() if word not in stop])
      
            pt = parsetree(cleanSentence, relations=True, lemmata=True)

            #print("s: .%s." % pt)

            for sentence in pt:
                #print("sentence: .%s.\n.%s.\nlen=%d" % (sentence, sentence.subjects, len(sentence.subjects)))
                #printSentence(sentence)

                #print ("relations: %s" % [x for x in sentence.relations])
                #print ("subject  : %s" % [x for x in sentence.subjects])
                #print ("verb     : %s" % [x for x in sentence.verbs])
                #print ("object   : %s" % [x for x in sentence.objects])
                
                #print("%s.%s(%s)" % (subject, verb, predicate))

                if sentence.subjects is not None and sentence.verbs is not None:
                    dictChunks = dict()
                    #print ("Sentence : %s" % sentence.chunks)
                    for chunk in sentence.chunks:
                        print("Chunk %s: .%s." % (chunk.type, chunk)) 
                        for word in chunk.words:
                            print("word: .%s." % (word)) 

    #Concepts.saveConcepts(chunkConcepts, "NVPChunks.p")



            



