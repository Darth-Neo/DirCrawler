#!/usr/bin/python
#
# Natural Language Processing of Information
#
import os
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

import logging
logger.setLevel(logging.INFO)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

if __name__ == "__main__":
    #conceptFile = "documents.p"
    #conceptFile = "words.p"
    #conceptFile = "chunks.p"
    #conceptFile = "topicChunks.p"
    conceptFile = "topicsDict.p"
    #conceptFile = "documentsSimilarity.p"
    #conceptFile = "NVPChunks.p"
    #conceptFile = "ngrams.p"
    #conceptFile = "ngramscore.p"
    #conceptFile = "ngramsubject.p"
    #conceptFile = "archi.p"
    #conceptFile = "pptx.p"

    #dir = "/Users/morrj140/Development/GitRepository/DirCrawler/DVC_20150201_102155"
    dir = os.getcwd()

    filePath = dir + os.sep + conceptFile
    #filePath = conceptFile

    logger.info("Loading :" + filePath)
    concepts = Concepts.loadConcepts(filePath)

    concepts.logConcepts()
    #concepts.printConcepts()
    
        




