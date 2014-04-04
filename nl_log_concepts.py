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
    conceptFile = "TopicChunks.p"
    
    logger.info("Loading :" + os.getcwd() + os.sep + conceptFile)
    concepts = Concepts.loadConcepts(conceptFile)

    listTopics = list()

    if True:
        cf = open(conceptFile[:-2] + ".txt", "wb")

        cf.write("Concepts from %s" % conceptFile)
        for conceptDoc in concepts.getConcepts().values():
            if len(conceptDoc.getConcepts()) > 1:
                print("%d:%s" % (len(conceptDoc.getConcepts()), conceptDoc.name))
                listTopics.append((len(conceptDoc.getConcepts()), conceptDoc.name))
                for concept in conceptDoc.getConcepts().values():
                    print "--->" + concept.name
                    cf.write(concept.name + os.linesep)

        cf.close()

    print "\nSorted List"
    lt = sorted(listTopics, key=lambda c: c[0], reverse=True)

    for x in lt:
        print x
                
    #concepts.logConcepts()
    #concepts.printConcepts()
    
        




