#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.TopicsModel import TopicsModel

num_topics = 150

def createTopics(conceptFile):
    stopwords = list()
    stopwords.append("data")
    stopwords.append("applications")
    stopwords.append("systems")
    stopwords.append("system")
    stopwords.append("s")
    stopwords.append("processes")
    stopwords.append("requirements")
    stopwords.append("xxx")
    stopwords.append("roadmap")
    
    logger.info("Load Concepts from " + conceptFile)
    conceptChunks = Concepts.loadConcepts(conceptFile)
    logger.info("Loaded Concepts")

    tm = TopicsModel()

    logger.info("Load Documents from Concepts")
    documentsList, wordcount = tm.loadWords(conceptChunks)

    logger.info("Read " + str(len(documentsList)) + " Documents, with " + str(wordcount) + " words.")

    num_topics = int(wordcount * 0.10)
    
    logger.info("Compute Topics")
    topics = tm.computeTopics(documentsList, nt=num_topics)

    tm.logTopics(topics)

    logger.info("Saving Topics")
    topicsConcepts = tm.saveTopics(topics)

    logger.info("Complete createTopics")

    topicChunksConcepts = Concepts("TopicChunks", "TC")

    for topic in topicsConcepts.getConcepts().values():
        logger.info("topic : %s", topic.name)
        tcc = topicChunksConcepts.addConceptKeyType(topic.name, "TopicWord")
        for document in conceptChunks.getConcepts().values():
            logger.debug("document : %s", document.name)
            for chunk in document.getConcepts().values():
                logger.debug("chunk : %s", chunk.name)
                if chunk.name.find(topic.name, 0, len(chunk.name)) > 0:
                    logger.info("Topic: %s \t Chunk : %s", topic.name, chunk.name)
                    tcc.addConceptKeyType(chunk.name, "CHUNK")

    Concepts.saveConcepts(topicChunksConcepts, "TopicChunks.p")

if __name__ == "__main__":
    createTopics("chunks.p")



