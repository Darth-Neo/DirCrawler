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

    spaces = " " * n

    for p in pc.values():
        if p.name.find(term, 0, len(term)) > 0:
            logger.info("%sTerm : %s[%s]->Count=%s" % (spaces, p.name, p.typeName, p.count))
        findConcepts(term, p, n+1)

   
if __name__ == "__main__":
    conceptFile = "documents.p"
    #conceptFile = "chunks.p"
    #conceptFile = "topicsDict.p"
    #conceptFile = "TopicChunks.p"
    #conceptFile = "ngrams.p"
    #conceptFile = "ngramscore.p"
    #conceptFile = "ngramsubject.p"
    #conceptFile = "NVPChunks.p"
    
    logger.info("Loading :" + os.getcwd() + os.sep + conceptFile)
    concepts = Concepts.loadConcepts(conceptFile)

    listTopics = list()

    term = "Product"

    findConcepts(term, concepts)

        




