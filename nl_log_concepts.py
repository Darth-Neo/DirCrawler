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
    conceptFile = "documents.p"
    #conceptFile = "chunks.p"
    conceptFile = "topicsDict.p"
    
    logger.info("Loading :" + os.getcwd() + os.sep + conceptFile)
    concepts = Concepts.loadConcepts(conceptFile)

    if False:
        cf = open(conceptFile[:-2] + ".txt", "wb")

        cf.write("Concepts from %s" % conceptFile)
        for conceptDoc in concepts.getConcepts().values():
            for concept in conceptDoc.getConcepts().values():
                print concept.name
                cf.write(concept.name + os.linesep)

        cf.close()
                
    concepts.logConcepts()
    #concepts.printConcepts()
    
        




