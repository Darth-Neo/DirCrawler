﻿#!/usr/bin/python
#
# Natural Language Processing of Information
#
import os
from subprocess import call
import sys

from nl_lib import Logger
logger = Logger.setupLogging(__name__)
logger.setLevel(Logger.INFO)

from nl_phase_a_DirCrawl import *
from nl_phase_b_CreateChunks import *
from nl_phase_c_Topics import *
from nl_phase_d_find_collocations import *
from nl_phase_e_TopicCloud import *
from nl_phase_f_graph_concepts import *
import time

GRAPH = False
DIRECTORY = True


def nl_phases(rootDir):

    if not os.path.isdir(rootDir):
        logger.error(u"Directory does not exist!")
        return

    if rootDir is None:
        logger.error(u"Nothing to work with!")
        return

    numFilesParsed = 0

    logger.debug(u"Number of arguments:%s arguments." % (len(sys.argv)))
    logger.debug(u"Argument List:" + str(sys.argv))

    if DIRECTORY:
        # Change current directory to enable to save pickles
        p, f = os.path.split(rootDir)

        homeDir = os.getcwd() + os.sep + f + u"_" + time.strftime(u"%Y%d%m_%H%M%S")

        if not os.path.exists(homeDir):
            os.makedirs(homeDir)
        os.chdir(homeDir)

    # measure process time, wall time
    t0 = time.clock()
    t1 = time.time()
    
    # nl_phase_a
    logger.info(u"Directory Crawl")
    dc = DirCrawl()
    numFilesParsed = dc.searchSubDir(rootDir)
   
    # nl_phase_b
    logger.info(u"Create Chunks")
    chunks = Chunks(dc.getDocumentsConcepts())
    chunks.createChunks()

    # nl_phase_c
    logger.info(u"create Topics")
    npbt = DocumentsSimilarity()
    npbt.createTopics(u"chunks.p")
    # npbt.findSimilarties("documentsSimilarity.p")
    
    # nl_phase_d
    logger.info(u"find_collocations")
    fc = Collocations(u"chunks.p")
    fc.find_collocations()
    conceptsNGram, conceptsNGramScore, conceptsNGramSubject = fc.getCollocationConcepts()

    # nl_phase_e
    logger.info(u"createTopicCloud for Subjects")
    createTopicsCloud(conceptsNGramSubject, u"NGRAM", numWords=50, scale=1.5)

    if GRAPH:
        if False:
            graph = PatternGraph()
        else:
            graph = GraphVizGraph()

        # nl_phase_f
        logger.info(u"graphConcepts")

        cg = ConceptsGraph(graph=graph, fileImage=u"GraphConcetps.png")

        cg.conceptsGraph(conceptsNGramSubject)

    # Conclude Batch Run
    # Timer
    logger.info(u"Documents Parsed = %d" % numFilesParsed)

    # measure wall time
    localtime = time.asctime(time.localtime(t1))
    logger.info(u"Start      time : %s" % localtime)
    
    localtime = time.asctime(time.localtime(time.time()) )
    logger.info(u"Completion time : %s" % localtime)

    # measure process time
    timeTaken = (time.clock() - t0)
    minutes = timeTaken % 60
    hours = minutes / 60
    logger.info(u"Process Time = %4.2f seconds, %d Minutes, %d hours" % (timeTaken, minutes, hours))

if __name__ == u"__main__":

    # Set the directory you want to start from
    # rootDir = "/Users/morrj140/Documents/SolutionEngineering/DVC"
    # rootDir = "/Users/morrj140/Documents/SolutionEngineering/Facilities Operation Management"
    # rootDir = "/Users/morrj140/Documents/SolutionEngineering/Digital Access Management/Merchandise Vision Replacement/REQ2"
    rootDir = "/Users/morrj140/Documents/SolutionEngineering/DVC"

    nl_phases(rootDir)