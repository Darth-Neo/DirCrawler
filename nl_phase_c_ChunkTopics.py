#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.TopicsModel import TopicsModel

def createChunkTopics(conceptFile):
    
    logger.info("Load Concepts from " + conceptFile)
    conceptChunks = Concepts.loadConcepts(conceptFile)
    logger.info("Loaded Concepts")

    tm = TopicsModel()

    logger.info("Load Documents from Concepts")
                                
    documentsList, wordcount = tm.loadConceptsWords(conceptChunks)

    logger.info("Read " + str(len(documentsList)) + " Documents, with " + str(wordcount) + " words.")

    num_topics = int(wordcount * 0.10)
    #num_topics = 100
    
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
            for sentence in document.getConcepts().values():
                logger.debug("sentence : %s", sentence.name)
                if sentence.name.find(topic.name, 0, len(sentence.name)) > 0:
                    logger.info("Topic: %s \t Sentence : %s", topic.name, sentence.name)
                    tcc.addConcept(sentence)

    Concepts.saveConcepts(topicChunksConcepts, "TopicChunks.p")

if __name__ == "__main__":
    createChunkTopics("chunks.p")



