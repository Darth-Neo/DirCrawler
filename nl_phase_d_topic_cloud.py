#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
import os
from nl_lib import Logger, Concepts, Constants, TopicCloud
logger = Logger.setupLogging(__name__)

def createTopicsCloud():
    logger.info("Starting Tag Cloud...")

    logger.info("Loading Topics from : " + Constants.topicsFile)
    topicsConcepts = Concepts.Concepts.loadConcepts(Constants.topicsFile)

    for topic in topicsConcepts.getConcepts().values():
        if topic.count == 0:
            del topicsConcepts.getConcepts()[topic.name]
    
    tc = TopicCloud.TopicCloud(topicsConcepts, os.getcwd() + os.sep)

    logger.info("Create Tag Cloud")

    tc.createCloudImage(size_x=1200, size_y=900, numWords=70)

    logger.info("Complete createTopicsCloud")


if __name__ == "__main__":
    createTopicsCloud()
