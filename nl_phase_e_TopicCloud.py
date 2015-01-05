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

def createTopicsCloud(concepts, topic, numWords=50, scale=1.0):
    logger.info("Starting Tag Cloud...")

    tc = TopicCloud(concepts, os.getcwd() + os.sep)

    logger.info("Create Tag Cloud")

    # Note: the first parameter must match for a topic cloud image to be created!
    tc.createCloudImage(topic, size_x=1200, size_y=900, numWords=numWords, scale=scale)

    logger.info("Complete createTopicsCloud")


if __name__ == "__main__":

    #conceptFile = "TopicChunks.p"
    #topic = "Chunk"

    #conceptFile = "topicsDict.p"
    #topic="Topic"

    #conceptFile = "archi.p"
    #topic="name"

    conceptFile = "ngramsubject.p"
    topic="NGRAM"

    #conceptFile = "req.p"
    #topic = "Word"

    #conceptFile = "chunks.p"
    #topic = "Lemma"
    #topic = "SBJ"
    #topic = "OBJ"
    #topic = "VP"
    #topic = "NN"
    #topic = "NNP"

    #conceptFile = "ngrams.p"
    #topic = "NGRAM"

    directory = "/Users/morrj140/Development/GitRepository/DirCrawler/DVC_20150201_102155"
    #dir = os.getcwd()

    os.chdir(directory)

    c = Concepts("GraphConcepts", "GRAPH")

    filePath = directory + os.sep + conceptFile
    logger.info("Loading Topics from : " + filePath)

    concepts = Concepts.loadConcepts(filePath)

    createTopicsCloud(concepts, topic)
