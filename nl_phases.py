#!/usr/bin/python
#
# Natural Language Processing of Filesystem
#
import os
import sys

from nl_phase_a_DirCrawl import *
from nl_phase_b_CreateChunks import *
from nl_phase_c_ChunkTopics import *
from nl_phase_d_TopicCloud import *
from nl_phase_e_Chunk_Topics import *
from nl_phase_f_graph_concepts import *
from nl_find_collocations import *
import time

logger = Logger.setupLogging(__name__)

def nl_phases():
    numFilesParsed = 0

    logger.debug("Number of arguments:" + str(len(sys.argv)) + "arguments.")
    logger.debug("Argument List:" + str(sys.argv))
    
    # Set the directory you want to start from
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture"
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture\\\AccoviaReplacement"
    #rootDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\product_types"
    #rootDir = "C:\\Users\morrj140\\Documents\\System Architecture\\OneSourceDocumentation"
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture\\AccoviaReplacement\\ProductProgram\\functionality"
    #rootDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\Issues"
    #rootDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\product_types"
    rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture\\AccoviaReplacement\\Product"
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture\\AccoviaReplacement\\Order"

    # Change current directory to enable to save pickles
    p, f = os.path.split(rootDir)
    homeDir = os.getcwd() + os.sep + f + "_" + time.strftime("%Y%d%m_%H%M%S")
    if not os.path.exists(homeDir):
        os.makedirs(homeDir)

    os.chdir(homeDir)

    # measure process time
    t0 = time.clock()

    # measure wall time
    t1 = time.time()
    
    # nl_phase_a
    numFilesParsed = searchSubDir(rootDir)
    
    Concepts.saveConcepts(documentsConcepts, "documents.p")

    # nl_phase_b
    logger.info("Create Chunks")        
    createChunks()

    time.sleep(0.25)

    # nl_phase_c
    logger.info("createChunkTopics")
    createChunkTopics("chunks.p")

    # nl_phase_e
    logger.info("getChunkTopics")
    getChunkTopics()

    # nl_phase_c
    logger.info("find_collocations") 
    find_collocations("documents.p")

    # nl_phase_d
    logger.info("graphConcepts")
    graphConcepts()

    # nl_phase_d
    createTopicsCloud()

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
    
