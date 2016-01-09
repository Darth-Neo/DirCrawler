#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
import os

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

import logging
logger.setLevel(logging.INFO)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts


def getChunkTopics():
    # conceptFile = u"documents.p"
    conceptFile = u"chunks.p"
    # conceptFile = u"topicsDict.p"
    # conceptFile = u"TopicChunks.p"
    # conceptFile = u"ngramsubject.p"

    conceptPathFile = os.getcwd() + os.sep + u"run" + os.sep + conceptFile

    logger.info(u"Loading :" + os.getcwd() + os.sep + u"run" + os.sep + conceptFile)
    concepts = Concepts.loadConcepts(conceptPathFile)

    listTopics = list()

    cf = open(conceptFile[:-2] + u".txt", u"wb")

    for conceptDoc in concepts.getConcepts().values():
        logger.debug(u"len %d" % len(conceptDoc.getConcepts()))
        if len(conceptDoc.getConcepts()) > 1:
            logger.debug(u"%d:%s" % (len(conceptDoc.getConcepts()), conceptDoc.name))
            listTopics.append((len(conceptDoc.getConcepts()), conceptDoc))
            for concept in conceptDoc.getConcepts().values():
                logger.debug(u"--->" + concept.name)

    logger.info(u"---- Sorted Topics ----")
    cf.write(u"---- Sorted Topics ----" + os.linesep)
    
    lt = sorted(listTopics, key=lambda c: c[0], reverse=True)

    for x in lt:
        logger.info(u"%s" % x[1].name)
        cf.write(x[1].name + os.linesep)
        for concept in x[1].getConcepts().values():
            logger.info(u"--->%s" % concept.name)
            cf.write(u"--->" + concept.name + os.linesep)
    
    cf.close()

if __name__ == u"__main__":
    getChunkTopics()

