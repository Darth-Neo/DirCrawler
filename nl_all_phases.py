#!/usr/bin/python
#
# Natural Language Processing of Information
#
import os
import sys

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

import logging
logger.setLevel(logging.INFO)

from nl_phase_a_DirCrawl import *
from nl_phase_b_CreateChunks import *
from nl_phase_c_Topics import *
from nl_phase_d_find_collocations import *
#from nl_phase_e_TopicCloud import *
from nl_phase_f_graph_concepts import *
import time

GRAPH = False
DIRECTORY = True

def nl_phases():
    numFilesParsed = 0

    logger.debug("Number of arguments:" + str(len(sys.argv)) + "arguments.")
    logger.debug("Argument List:" + str(sys.argv))
    
    # Set the directory you want to start from
    rootDir = "/Users/morrj140/Documents/SolutionEngineering/DVC"

    if DIRECTORY == True:
        # Change current directory to enable to save pickles
        p, f = os.path.split(rootDir)

        homeDir = os.getcwd() + os.sep + f + "_" + time.strftime("%Y%d%m_%H%M%S")

        if not os.path.exists(homeDir):
            os.makedirs(homeDir)
        os.chdir(homeDir)

    # measure process time, wall time
    t0 = time.clock()
    t1 = time.time()
    
    # nl_phase_a
    logger.info("Directory Crawl")
    dc = DirCrawl()
    numFilesParsed = dc.searchSubDir(rootDir)
   
    # nl_phase_b
    logger.info("Create Chunks")
    chunks = Chunks(dc.getDocumentsConcepts())
    chunks.createChunks()

    # nl_phase_c
    logger.info("create Topics")
    npbt = DocumentsSimilarity()
    npbt.createTopics("chunks.p")
    #npbt.findSimilarties("documentsSimilarity.p")
    
    # nl_phase_d
    logger.info("find_collocations")
    fc = Collocations("chunks.p")
    fc.find_collocations()
    conceptsNGram, conceptsNGramScore, conceptsNGramSubject = fc.getCollocationConcepts()

    # nl_phase_e
    #logger.info("createTopicCloud for Subjects")
    #createTopicsCloud(conceptsNGramSubject, "NGRAM", numWords=50, scale=1.5)

    if GRAPH == True:
        # nl_phase_f
        logger.info("graphConcepts")
        #listConcepts = list()
        #graphConcepts(dc.getDocumentsConcepts())
        #graphConcepts(chunks.getChunkConcepts())
        #graphConcepts(ct.getChunkTopicsConcepts())
        graphConcepts(conceptsNGram)
        #graphConcepts(conceptsNGramScore)
        graphConcepts(conceptsNGramSubject)

    # Conclude Batch Run
    # Timer
    logger.info("Documents Parsed = %d" % numFilesParsed)

    # measure wall time
    localtime = time.asctime( time.localtime(t1))
    logger.info("Start      time : %s" % localtime)
    
    localtime = time.asctime( time.localtime(time.time()) )
    logger.info("Completion time : %s" % localtime)

    # measure process time
    timeTaken = (time.clock() - t0)
    minutes = timeTaken / 60
    hours = minutes / 60
    logger.info("Process Time = %4.2f seconds, %d Minutes, %d hours" % (timeTaken, minutes, hours))

if __name__ == "__main__":
    nl_phases()

        
