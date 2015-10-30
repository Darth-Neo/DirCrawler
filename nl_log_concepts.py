#!/usr/bin/python
#
# Natural Language Processing of Information
#
import os
from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


def yns():
    topicsFile = u"topicsDict.p"
    logger.info(u"Loading :" + topicsFile)
    topics = Concepts.loadConcepts(topicsFile).getConcepts()

    conceptFile = u"ngramsubject.p"
    filePath = conceptFile
    logger.info(u"Loading :" + filePath)
    concepts = Concepts.loadConcepts(filePath)

    if True:
        td = dict()

        for k, v in concepts.getConcepts().items():
            logger.info(u"%s" % k)

            if k in topics:
                td[k] = v.dictChildrenType(u"NGRAM")
                v.logConcepts()
                # logger.info(u"    %s" % (k))

        for k, v in td.items():
            print(u"==>%s[%s]" % (k, v))

    elif False:
        concepts.logConcepts()

    elif False:
        concepts.printConcepts()


if __name__ == u"__main__":

    logger.info(u"%s" % os.getcwd())
    os.chdir(u"." + os.sep + u"run")

    # conceptFile = u"documents.p"
    # conceptFile = u"words.p"
    # conceptFile = u"chunks.p"

    # conceptFile = u"topicChunks.p"
    # conceptFile = u"topicsDict.p"

    # conceptFile = u"documentsSimilarity.p"
    # conceptFile = u"NVPChunks.p"
    # conceptFile = u"ngrams.p"
    # conceptFile = u"ngramscore.p"

    conceptFile = u"ngramsubject.p"

    logger.info(u"Loading :" + conceptFile)
    concepts = Concepts.loadConcepts(conceptFile)

    concepts.logConcepts()





