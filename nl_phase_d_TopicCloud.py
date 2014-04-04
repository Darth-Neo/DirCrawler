#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
import os
from nl_lib import Logger
from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.TopicCloud import TopicCloud

logger = Logger.setupLogging(__name__)

def createTopicsCloud():
    logger.info("Starting Tag Cloud...")

    conceptFile = "Chunks.p"
    
    logger.info("Loading Topics from : " + conceptFile)
    concepts = Concepts.loadConcepts(conceptFile)

    concepts.logConcepts()

    #for topic in concepts.getConcepts().values():
    #    if topic.count == 0:
    #        del concepts.getConcepts()[topic.name]
    
    tc = TopicCloud(concepts, os.getcwd() + os.sep)

    logger.info("Create Tag Cloud")

    tc.createCloudImage(size_x=1200, size_y=900, numWords=10)

    logger.info("Complete createTopicsCloud")


if __name__ == "__main__":
    createTopicsCloud()
