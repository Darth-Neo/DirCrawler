#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
import os
from nl_lib.Constants import *
from nl_lib import Logger
from nl_lib.Concepts import Concepts

logger = Logger.setupLogging(__name__)

def getChunkTopics():
    #conceptFile = "documents.p"
    #conceptFile = "chunks.p"
    #conceptFile = "topicsDict.p"
    #conceptFile = "TopicChunks.p"
    conceptFile = "ngramsubject.p"

    logger.info("Loading :" + os.getcwd() + os.sep + conceptFile)
    concepts = Concepts.loadConcepts(conceptFile)

    listTopics = list()

    cf = open(conceptFile[:-2] + ".txt", "wb")

    for conceptDoc in concepts.getConcepts().values():
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

if __name__ == "__main__":
    getChunkTopics()

