#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
import os
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

import logging
logger.setLevel(logging.INFO)

import networkx as nx

from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, NetworkXGraph, Neo4JGraph, GraphVizGraph
from nl_lib.Constants import *

gdb = "http://localhost:7474/db/data/"
#gdb = "http://10.92.82.60:7574/db/data/"

def addGraphNodes(graph, concepts, n=0):
    if n == 0:
        n += 1
        addGraphNodes(graph, concepts, n)
    else:
        n += 1

    for c in concepts.getConcepts().values():
        logger.debug("%d : %d Node c : %s:%s" % (n, len(c.getConcepts()), c.name, c.typeName))

        ct = c.name.strip("\"").split(" ")
        logger.info("ct : %s" % ct)
        if len(ct) == 3:
            if ct[0] == ct[1] or ct[0] == ct[2]:
                logger.info("skip ct : %s" % ct)
                continue

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

def graphConcepts(concepts, graph=None, filename="example.png"):

    #graph = Neo4JGraph(gdb)

    #logger.info("Clear the Graph @" + gdb)
    #graph.clearGraphDB()

    graph = NetworkXGraph()
    #graph = PatternGraph()
    #graph = GraphVizGraph()

    logger.info("Adding nodes the graph ...")
    addGraphNodes(graph, concepts)
    logger.info("Adding edges the graph ...")
    addGraphEdges(graph, concepts)

    if isinstance(graph, GraphVizGraph):
        graph.exportGraph(filename=filename)
        logger.info("Saved Graph - %s" % filename)

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

        gl = nx.connected_components(graph.G) # [[1, 2, 3], ['spam']]
        logGraph(gl, "Connected")

        gl = nx.clustering(graph.G)
        logGraph(gl, "Cluster")

        gl = nx.closeness_centrality(graph.G)
        logGraph(gl, "Closeness")

        gl = nx.betweenness_centrality(graph.G)
        logGraph(gl, "Betweenness_Centrality")

        gl = nx.pagerank(graph.G)
        logGraph(gl, "Page Rank")

        gl = nx.hits(graph.G)
        logGraph(gl, "Hits")

        gl = nx.authority_matrix(graph.G)
        #logGraph(gl, "authority_matrix")

        gl = nx.minimum_spanning_tree(graph.G)
        logGraph(gl, "minimum_spanning_tree")

    if isinstance(graph, PatternGraph):
        #graph.g.remove("ProjectConceptsSimilarity")
        logger.info("Exporting Graph")
        graph.exportGraph()

def logGraph(gl, title, scale=1):
    logger.info("---%s---" % title)
    n = 0
    for x in gl:
        n += 1
        if isinstance(gl, dict):
            logger.info("%s [%d]:%s=%3.4f" % (title, n, x, gl[x]*scale))

        else:
            logger.info("%s [%d]" % (x, n))


if __name__ == "__main__":
    #conceptFile = "documents.p"
    #conceptFile = "words.p"
    #conceptFile = "NVPChunks.p"
    #conceptFile = "chunks.p"
    #conceptFile = "topicsDict.p"
    #conceptFile = "TopicChunks.p"
    #conceptFile = "ngrams.p"
    #conceptFile = "ngramscore.p"
    conceptFile = "ngramsubject.p"
    #conceptFile = "archi.p"

    listHomeDir = list()
    listHomeDir.append("/Users/morrj140/Development/GitRepository/DirCrawler/DVC_20150501_143307")
    #listHomeDir.append(os.getcwd())
    #listHomeDir.append("C:\Users\morrj140\Dev\GitRepository\DirCrawler\SmartMedia_20140206_120122")
    #listHomeDir.append("C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\Estimates_20141205_124422")
    #homeDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\Requirements_20143004_160216"
    #homeDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\ExternalInterfaces_20141205_095115"
    #listHomeDir.append("C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\Services_20143004_101231")
    #listHomeDir.append("/Users/morrj140/Development/GitRepository/DirCrawler")

    #listHomeDir.append("/Users/morrj140/Development/GitRepository/DirCrawler/Research_20141709_104529")

    #listHomeDir.append("/Users/morrj140/Development/GitRepository/DirCrawler/CodeGen_20142710_153333")

    c = Concepts("GraphConcepts", "GRAPH")
    
    for conceptDir in listHomeDir:
        # Change current directory to enable to save pickles
        p, f = os.path.split(conceptDir)
        logger.info("Loading :" + conceptDir + os.sep + conceptFile)
        c.addConcept(Concepts.loadConcepts(conceptDir + os.sep + conceptFile))

    # c.logConcepts()
    
    graphConcepts(c, filename="DVC.png")

    



