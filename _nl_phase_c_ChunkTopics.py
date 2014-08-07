#!/usr/bin/python
#
# Natural Language Processing of Information
#
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.TopicsModel import TopicsModel

class ChunkTopics(object):
    conceptChunks = None
    topicChunksConcepts = None
    conceptFile = "chunks.p"
    topicChunksFile = "TopicChunks.p"

    def __init__(self, conceptChunks=None):
        if conceptChunks == None:
            logger.info("Load Concepts from " + self.conceptFile)
            self.conceptChunks = Concepts.loadConcepts(self.conceptFile)
            logger.info("Loaded Concepts")
        else:
            self.conceptChunks = conceptChunks

        self.topicChunksConcepts = Concepts("TopicChunks", "TC")

    def getChunkTopicsConcepts(self):
        return self.topicChunksConcepts

    def getChunkTopics(self):        
        if len(self.topicChunksFile.getConcepts()) == 0:
            logger.info("Loading :" + os.getcwd() + os.sep + self.topicChunksFile)
            self.topicChunksConcepts = Concepts.loadConcepts(self.topicChunksFile)

        listTopics = list()

        cf = open(self.topicChunksFile[:-2] + ".txt", "wb")

        for conceptDoc in self.topicChunksConcepts.getConcepts().values():
            logger.debug("len %d" % len(conceptDoc.getConcepts()))
            if len(conceptDoc.getConcepts()) > 1:
                logger.debug("%d:%s" % (len(conceptDoc.getConcepts()), conceptDoc.name))
                listTopics.append((len(conceptDoc.getConcepts()), conceptDoc))
                for concept in conceptDoc.getConcepts().values():
                    logger.debug("--->" + concept.name)

        logger.info("---- Sorted Topics ----")
        cf.write("---- Sorted Topics ----" + os.linesep)
        
        lt = sorted(listTopics, key=lambda c: c[0], reverse=True)

        for x in lt:
            logger.info("%s" % x[1].name)
            cf.write(x[1].name + os.linesep)
            for concept in x[1].getConcepts().values():
                logger.info("--->%s" % concept.name)
                cf.write("--->" + concept.name + os.linesep)
        
        cf.close()

    def createChunkTopics(self):   
        tm = TopicsModel()

        logger.info("Load Documents from Concepts")
                                    
        documentsList, wordcount = tm.loadConceptsWords(self.conceptChunks)

        logger.info("Read " + str(len(documentsList)) + " Documents, with " + str(wordcount) + " words.")

        num_topics = int(wordcount * 0.10)
        #num_topics = 100
        
        logger.info("Compute Topics")
        topics = tm.computeTopics(documentsList, nt=num_topics)
                
        tm.logTopics(topics)

        logger.info("Saving Topics")
        topicsConcepts = tm.saveTopics(topics)

        logger.info("Complete createTopics")

        for topic in topicsConcepts.getConcepts().values():
            logger.info("topic : %s", topic.name)
            tcc = self.topicChunksConcepts.addConceptKeyType(topic.name, "TopicWord")

            for document in self.conceptChunks.getConcepts().values():
                logger.debug("document : %s", document.name)
                for sentence in document.getConcepts().values():
                    logger.debug("sentence : %s", sentence.name)
                    if sentence.name.find(topic.name, 0, len(sentence.name)) > 0:
                        logger.info("Topic: %s \t Sentence : %s", topic.name, sentence.name)
                        tcc.addConcept(sentence)

        Concepts.saveConcepts(self.topicChunksConcepts, self.topicChunksFile)

if __name__ == "__main__":
    ct = ChunkTopics(conceptChunks="chunks.p")
    ct.createChunkTopics()
    

