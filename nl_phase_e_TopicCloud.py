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

def createTopicsCloud(concepts, topic, numWords=30, scale=1.5):
    logger.info("Starting Tag Cloud...")

    tc = TopicCloud(concepts, os.getcwd() + os.sep)

    logger.info("Create Tag Cloud")

    # Note: the first parameter must match for a topic cloud image to be created!
    tc.createCloudImage(topic, size_x=1200, size_y=900, numWords=numWords, scale=scale)

    logger.info("Complete createTopicsCloud")


if __name__ == "__main__":
    #conceptFile = "TopicChunks.p"
    #conceptFile = "topicsDict.p"
    #conceptTopic = "Topic"
    # topic = "SBJ"

    conceptFile = "ngramsubject.p"
    topic = "NGRAM"

    logger.info("Loading Topics from : " + conceptFile)

    concepts = Concepts.loadConcepts(conceptFile)

    createTopicsCloud(concepts, topic)
