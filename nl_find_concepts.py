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


def findConcepts(term, concepts, n=0):
    pc = concepts.getConcepts()

    spaces = u" " * n

    for p in pc.values():
        if p.name.find(term, 0, len(term)) > 0:
            logger.info(u"%sTerm : %s[%s]->Count=%s" % (spaces, p.name, p.typeName, p.count))
        findConcepts(term, p, n+1)

   
if __name__ == u"__main__":
    # conceptFile = u"documents.p"
    conceptFile = u"chunks.p"
    # conceptFile = u"topicsDict.p"
    # conceptFile = u"TopicChunks.p"
    # conceptFile = u"ngrams.p"
    # conceptFile = u"ngramscore.p"
    # conceptFile = u"ngramsubject.p"
    # conceptFile = u"NVPChunks.p"
    
    logger.info(u"Loading :" + os.getcwd() + os.sep + conceptFile)
    concepts = Concepts.loadConcepts(conceptFile)

    listTopics = list()

    term = u"Product"

    findConcepts(term, concepts)

        




