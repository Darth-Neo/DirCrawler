#!/usr/bin/python
#
# Natural Language Processing of Information
#

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from nl_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


if __name__ == u"__main__":

    # os.chdir(u"test")
    os.chdir(u"run")

    logger.info(u"%s" % os.getcwd())

    # conceptFile = u"documents.p"
    # conceptFile = u"words.p"
    # conceptFile = u"chunks.p"

    # conceptFile = u"topicChunks.p"
    # conceptFile = u"topicsDict.p"

    conceptFile = u"documentsSimilarity.p"
    # conceptFile = u"NVPChunks.p"
    # conceptFile = u"ngrams.p"
    # conceptFile = u"ngramscore.p"

    # conceptFile = u"ngramsubject.p"

    logger.info(u"Loading :" + conceptFile)
    concepts = Concepts.loadConcepts(conceptFile)

    concepts.logConcepts()
    # concepts.printConcepts()

