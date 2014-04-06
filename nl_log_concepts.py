#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
import os
from nl_lib.Constants import *
from nl_lib import Logger
from nl_lib.Concepts import Concepts

logger = Logger.setupLogging(__name__)
   
if __name__ == "__main__":
    #conceptFile = "documents.p"
    #conceptFile = "chunks.p"
    #conceptFile = "topicsDict.p"
    #conceptFile = "TopicChunks.p"
    conceptFile = "ngrams.p"
    #conceptFile = "ngramscore.p"
    
    logger.info("Loading :" + os.getcwd() + os.sep + conceptFile)
    concepts = Concepts.loadConcepts(conceptFile)

    listTopics = list()

    if conceptFile == "TopicChunks.p":
        cf = open(conceptFile[:-2] + ".txt", "wb")
 
        cf.write("Concepts from %s" % conceptFile)
        for conceptDoc in concepts.getConcepts().values():
           for concept in conceptDoc.getConcepts().values():
               logger.info(concept.name)
               cf.write("**" + concept.name + os.linesep)
           
           logger.info("%d:%s" % (abs(conceptDoc.count), conceptDoc.name))
           listTopics.append((abs(conceptDoc.count), conceptDoc.name))
           for concept in conceptDoc.getConcepts().values():
               logger.info( "--->" + concept.name)
               cf.write(concept.name + os.linesep)

        cf.close()

        logger.info( "---Sorted List---")
        lt = sorted(listTopics, key=lambda c: c[0], reverse=True)

        for x in lt:
            logger.info( x)
    else:
        concepts.logConcepts()
        #concepts.printConcepts()
    
        




