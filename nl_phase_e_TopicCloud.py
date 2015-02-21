#!/usr/bin/python
#
# Natural Language Processing of Information
#
import os
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

import logging
logger.setLevel(logging.INFO)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.TopicCloud import TopicCloud

def createTopicsCloud(concepts, topic, conceptFile, numWords=150, scale=1.75):
    logger.info("Starting Tag Cloud...")

    tc = TopicCloud(concepts, conceptFile=conceptFile+".png")

    logger.info("Create Tag Cloud")

    # Note: the first parameter must match for a topic cloud image to be created!
    tc.createCloudImage(topic, size_x=1200, size_y=900, numWords=numWords, scale=scale)

    logger.info("Complete createTopicsCloud")


if __name__ == "__main__":

    if False:
        conceptFile = "TopicChunks.p"
        topic = "Chunk"

    elif False:
        conceptFile = "topicsDict.p"
        topic="Topic"

    elif False:
        conceptFile = "archi.p"
        topic="name"

    elif True:
        conceptFile = "ngramsubject.p"
        topic="NGRAM"

    elif False:
        conceptFile = "req.p"
        topic = "Word"

    elif False:
        conceptFile = "chunks.p"
        topic = "Lemma"
        topic = "SBJ"
        topic = "OBJ"
        topic = "VP"
        topic = "NN"
        topic = "NNP"

    elif False:
        conceptFile = "ngrams.p"
        topic = "NGRAM"

    #directory = "./crawl_20151002_123832" #os.getcwd()
    #os.chdir(directory)
    #filePath = directory + os.sep + conceptFile

    c = Concepts("GraphConcepts", "GRAPH")

    logger.info("Loading Topics from : " + conceptFile)

    concepts = Concepts.loadConcepts(conceptFile)

    createTopicsCloud(concepts, topic, conceptFile[:-2], numWords=30, scale=0.2)
