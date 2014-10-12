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
    #conceptTopic = "Topic"
    #topic = "SBJ"

    #conceptFile = "archi.p"
    #topic="name"

    #conceptFile = "chunks.p"
    #topic = "Lemma"
    #topic = "SBJ"
    #topic = "OBJ"
    #topic = "VP"
    #topic = "NN"
    #topic = "NNP"

    #conceptFile = "ngrams.p"

    conceptFile = "ngramsubject.p"
    topic = "NGRAM"


    #topic = "TriGram"

    dir = "/Users/morrj140/Development/GitRepository/DirCrawler/CodeGen/EAI Models_20140310_170012"
    #dir = os.getcwd()

    #filePath = dir + os.sep + conceptFile
    filePath = dir + conceptFile

    conceptFile = "ngramsubject.p"
    topic = "NGRAM"

    logger.info("Loading Topics from : " + conceptFile)

    concepts = Concepts.loadConcepts(conceptFile)

    createTopicsCloud(concepts, topic)
