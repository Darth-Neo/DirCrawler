#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
import os
from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, NetworkXGraph
from nl_lib.Constants import *

logger = Logger.setupLogging(__name__)

def createGraph(graph, concepts):
    for c in concepts.getConcepts().values():
        for d in c.getConcepts().values():
            logger.info("Node d : %s" % d.name)
            graph.addConcepts(d)

    for c in concepts.getConcepts().values():
        i = 0
        logger.info("Edge c : %s" % c.name)
        for d in c.getConcepts().values():
            logger.info("Edge d : %s" % d.name)
            if i == 0:
                parentNode = d
            else:
                graph.addEdge(parentNode, d)
                logger.info("Edge %s-%s" % (parentNode.name, d.name))
            i += 1

def graphConcepts():
    
    listConceptFile = list()
    #listConceptFile.append("documents.p")
    #listConceptFile.append("NVPChunks.p")
    #listConceptFile.append("TopicChunks.p")
    #listConceptFile.append("chunks.p")
    #listConceptFile.append("topicsDict.p")
    #listConceptFile.append("TopicChunks.p")
    listConceptFile.append("ngrams.p")
    #listConceptFile.append("ngramscore.p")

    for conceptFile in listConceptFile:
        logger.info("Loadng :" + conceptFile)
        concepts = Concepts.loadConcepts(conceptFile)
    
        graph = NetworkXGraph()
        #graph2 = PatternGraph()

        createGraph(graph, concepts)
        
    if isinstance(graph, NetworkXGraph):
        #graph.G.remove_node("ProjectConceptsSimilarity")
        #graph.drawGraph("concepts.png")
        filename = "concepts.net"
        logger.info("Saving Graph - %s" % filename)
        graph.saveGraphPajek(filename)
        graph.saveGraph("concepts.gml")
        
    if isinstance(graph, PatternGraph):
        #graph.g.remove("ProjectConceptsSimilarity")
        logger.info("Exporting Graph")
        graph.exportGraph()

   
if __name__ == "__main__":
    graphConcepts()



