#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib import Constants
from nl_lib import Concepts
from nl_lib import TopicsModel

num_topics = 150

def createTopics(conceptFile):
    stopwords = list()
    stopwords.append("data")
    stopwords.append("applications")
    stopwords.append("systems")
    stopwords.append("s")
    stopwords.append("processes")
    stopwords.append("requirements")
    stopwords.append("xxx")
    stopwords.append("roadmap")
    
    logger.info("Load Concepts from " + conceptFile)
    concepts = Concepts.Concepts.loadConcepts(conceptFile)
    logger.info("Loaded Concepts")

    tm = TopicsModel.TopicsModel()

    logger.info("Load Documents from Concepts")
    documentsList, wordcount = tm.loadWords(concepts)

    logger.info("Read " + str(len(documentsList)) + " Documents, with " + str(wordcount) + " words.")

    logger.info("Compute Topics")
    topics = tm.computeTopics(documentsList, nt=num_topics)

    tm.logTopics(topics)

    logger.info("Saving Topics")
    topicsConcepts = tm.saveTopics(topics)

    logger.info("Complete createTopics")

if __name__ == "__main__":
    createTopics("chunks.p")



