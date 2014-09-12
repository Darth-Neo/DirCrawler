#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
import os
import logging
from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, NetworkXGraph, Neo4JGraph
from nl_lib.Constants import *

logger = Logger.setupLogging(__name__)

logger.setLevel(logging.INFO)

gdb = "http://localhost:7474/db/data/"
#gdb = "http://10.92.82.60:7574/db/data/"

def addGraphNodes(graph, concepts, n=0):
    n += 1
    for c in concepts.getConcepts().values():
        logger.debug("%d : %d Node c : %s:%s" % (n, len(c.getConcepts()), c.name, c.typeName))
        graph.addConcept(c)
        if len(c.getConcepts()) != 0:
            addGraphNodes(graph, c, n)

def addGraphEdges(graph, concepts, n=0):
    n += 1
    i = 1
    for c in concepts.getConcepts().values():
        logger.debug("%d : %d Edge c : %s:%s" % (n, len(c.getConcepts()), c.name, c.typeName))
        if i == 1:
            p = c
            i += 1
        else:
            graph.addEdge(p, c)
        if len(c.getConcepts()) != 0:
            addGraphEdges(graph, c, n)

def graphConcepts(concepts, graph=None):

    #graph = Neo4JGraph(gdb)

    #logger.info("Clear the Graph @" + gdb)
    #graph.clearGraphDB()

    #graph = NetworkXGraph()
    graph = PatternGraph()

    logger.info("Adding nodes the graph ...")
    addGraphNodes(graph, concepts)
    logger.info("Adding edges the graph ...")
    addGraphEdges(graph, concepts)

    if isinstance(graph, Neo4JGraph):
        graph.setNodeLabels()

    if isinstance(graph, NetworkXGraph):
        #graph.G.remove_node("ProjectConceptsSimilarity")
        #graph.drawGraph("concepts.png")
        filename = "concepts.net"
        logger.info("Saving Graph - %s" % filename)
        graph.saveGraphPajek(filename)
        graph.saveGraph("concepts.gml")
        logger.info("Saving Graph - %s" % "concepts.gml")
        
    if isinstance(graph, PatternGraph):
        #graph.g.remove("ProjectConceptsSimilarity")
        logger.info("Exporting Graph")
        graph.exportGraph()
   
if __name__ == "__main__":
    #conceptFile = "documents.p"
    #conceptFile = "NVPChunks.p"
    #conceptFile = "chunks.p"
    #conceptFile = "topicsDict.p"
    #conceptFile = "TopicChunks.p"
    conceptFile = "ngrams.p"
    #conceptFile = "ngramscore.p"
    conceptFile = "ngramsubject.p"
    #conceptFile = "archi.p"

    listHomeDir = list()
    #listHomeDir.append(os.getcwd())
    #listHomeDir.append("C:\Users\morrj140\Dev\GitRepository\DirCrawler\SmartMedia_20140206_120122")
    #listHomeDir.append("C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\Estimates_20141205_124422")
    #homeDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\Requirements_20143004_160216"
    #homeDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\ExternalInterfaces_20141205_095115"
    #listHomeDir.append("C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\Services_20143004_101231")
    listHomeDir.append("/Users/morrj140/Development/GitRepository/DirCrawler")

    c = Concepts("GraphConcepts", "GRAPH")
    
    for conceptDir in listHomeDir:
        # Change current directory to enable to save pickles
        p, f = os.path.split(conceptDir)
        logger.info("Loading :" + conceptDir + os.sep + conceptFile)
        c.addConcept(Concepts.loadConcepts(conceptDir + os.sep + conceptFile))

    # c.logConcepts()
    
    graphConcepts(c)

    



