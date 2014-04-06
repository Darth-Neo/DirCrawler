#!/usr/bin/python
#
# Natural Language Processing of Filesystem
#
import os
import sys

from nl_phase_a_DirCrawl import *
from nl_phase_b_CreateChunks import *
from nl_phase_c_ChunkTopics import *
from nl_phase_e_Chunk_Topics import *
from nl_phase_f_graph_concepts import *
import time

logger = Logger.setupLogging(__name__)

def nl_phases():
    # measure process time
    t0 = time.clock()

    # measure wall time
    t1 = time.time()

    logger.debug("Number of arguments:" + str(len(sys.argv)) + "arguments.")
    logger.debug("Argument List:" + str(sys.argv))
    
    # Set the directory you want to start from
    rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture"
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture\\Accovia"
    #rootDir = "C:\\Users\morrj140\\Documents\\System Architecture\\OneSourceDocumentation"
    
    searchSubDir(rootDir)

    Concepts.saveConcepts(documentsConcepts, "documents.p")

    createChunks()

    createChunkTopics("chunks.p")

    getChunkTopics()

    graphConcepts()
    
if __name__ == "__main__":
    nl_phases()
    
