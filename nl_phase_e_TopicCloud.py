#!/usr/bin/python
#
# Natural Language Processing of Information
#
import os
from nl_lib import Logger
from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.TopicCloud import TopicCloud

logger = Logger.setupLogging(__name__)

def createTopicsCloud(concepts, topic, numWords=50, scale=1.0):
    logger.info("Starting Tag Cloud...")

    tc = TopicCloud(concepts, os.getcwd() + os.sep)

    logger.info("Create Tag Cloud")

    # Note: the first parameter must match for a topic cloud image to be created!
    tc.createCloudImage(topic, size_x=1200, size_y=900, numWords=numWords, scale=scale)

    logger.info("Complete createTopicsCloud")


if __name__ == "__main__":
    #conceptFile = "TopicChunks.p"
    conceptFile = "topicsDict.p"
    topic = "Topic"

    #conceptFile = "archi.p"
    #topic="name"

    #conceptFile = "ngramsubject.p"
    #topic = "NGRAM"

    #conceptFile = "chunks.p"
    #topic = "Lemma"
    #topic = "SBJ"
    #topic = "OBJ"
    #topic = "VP"
    #topic = "NN"
    #topic = "NNP"

    #conceptFile = "ngrams.p"
    #topic = "NGRAM"

    #conceptFile = "ngramsubject.p"
    #topic = "TriGram"

    dir = "/Users/morrj140/Development/GitRepository/DirCrawler/TravelBox Overview_20142810_115621"
    #dir = os.getcwd()

    #filePath = dir + os.sep + conceptFile
    filePath = dir + os.sep + conceptFile

    logger.info("Loading Topics from : " + filePath)

    concepts = Concepts.loadConcepts(filePath)

    newConcepts = Concepts(concepts.name, concepts.typeName)
    for c in concepts.getConcepts().values():
        name = c.name.strip("\"")
        typeName = c.typeName
        nc = newConcepts.addConceptKeyType(name, typeName)
        nc.count = c.count
        logger.info("name : %s" % name)

    createTopicsCloud(newConcepts, topic)
