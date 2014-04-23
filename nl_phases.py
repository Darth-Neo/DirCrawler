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
from nl_find_collocations import *
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
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture"
    rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture\\\AccoviaReplacement"
    #rootDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\product_types"
    #rootDir = "C:\\Users\morrj140\\Documents\\System Architecture\\OneSourceDocumentation"
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture\\AccoviaReplacement\\ProductProgram\\functionality"
    
    searchSubDir(rootDir)

    Concepts.saveConcepts(documentsConcepts, "documents.p")
            
    createChunks()

    find_collocations("documents.p")

    getChunkTopics()

    graphConcepts()

    createChunkTopics("chunks.p")
    
if __name__ == "__main__":
    nl_phases()
    
