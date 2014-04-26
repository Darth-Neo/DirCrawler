#!/usr/bin/python
#
# Natural Language Processing of Information
#
import os
import sys

from nl_phase_a_DirCrawl import *
from nl_phase_b_CreateChunks import *
from nl_phase_c_ChunkTopics import *
from nl_phase_d_find_collocations import *
from nl_phase_e_TopicCloud import *
from nl_phase_f_graph_concepts import *
import time

logger = Logger.setupLogging(__name__)

def nl_phases():
    numFilesParsed = 0

    logger.debug("Number of arguments:" + str(len(sys.argv)) + "arguments.")
    logger.debug("Argument List:" + str(sys.argv))
    
    # Set the directory you want to start from
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture"
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture\\\AccoviaReplacement"
    #rootDir = "C:\\Users\morrj140\\Documents\\System Architecture\\OneSourceDocumentation"
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture\\AccoviaReplacement\\ProductProgram\\functionality"
    #rootDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\Issues"
    rootDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\product_types"
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture\\AccoviaReplacement\\Product"
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture\\AccoviaReplacement\\Order"

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
    logger.info("createChunkTopics")
    ct = ChunkTopics(chunks.getChunkConcepts())
    ct.createChunkTopics()

    # nl_phase_d
    logger.info("find_collocations")
    fc = Collocations(dc.getDocumentsConcepts())
    fc.find_collocations()
    conceptsNGram, conceptsNGramScore, conceptsNGramSubject = fc.getCollocationConcepts()

    # nl_phase_e
    logger.info("createTopicCloud for Subjects")
    createTopicsCloud(conceptsNGram, "NGRAM")
    
    # nl_phase_f
    logger.info("graphConcepts")
    listConcepts = list()
    #listConcepts.append(dc.getDocumentsConcepts())
    #listConcepts.append(chunks.getChunkConcepts())
    #listConcepts.append(ct.getChunkTopicsConcepts())
    listConcepts.append(conceptsNGram)
    #listConcepts.append(conceptsNGramScore)
    listConcepts.append(conceptsNGramSubject)
    graphConcepts(listConcepts)

    # Conclude Batch Run
    # Timer
    logger.info("Documents Parsed = %d" % numFilesParsed)

    # measure wall time
    localtime = time.asctime( time.localtime(t1))
    logger.info("Start      time : %s" % localtime)
    
    localtime = time.asctime( time.localtime(time.time()) )
    logger.info("Completion time : %s" % localtime)

    # measure process time
    logger.info("Process Time = %4.2f seconds" % (time.clock() - t0))

if __name__ == "__main__":
    nl_phases()
    
