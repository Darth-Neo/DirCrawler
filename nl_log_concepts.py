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

if __name__ == u"__main__":

    # conceptFile = u"documents.p"
    # conceptFile = u"words.p"
    conceptFile = u"chunks.p"

    # conceptFile = u"topicChunks.p"
    # conceptFile = u"topicsDict.p"

    # conceptFile = u"documentsSimilarity.p"
    # conceptFile = u"NVPChunks.p"
    # conceptFile = u"ngrams.p"
    # conceptFile = u"ngramscore.p"
    # conceptFile = u"ngramsubject.p"

    logger.info(u"%s" % os.getcwd())
    os.chdir(u"." + os.sep + u"run")

    filePath = conceptFile
    # filePath = conceptFile

    logger.info(u"Loading :" + filePath)
    concepts = Concepts.loadConcepts(filePath)

    concepts.logConcepts()
    # concepts.printConcepts()





