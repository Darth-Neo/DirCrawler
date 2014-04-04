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

def createGraph(graph):
    for conceptFile in listConceptFile:
        logger.info("Loading :" + conceptFile)
        concepts = Concepts.loadConcepts(conceptFile)

        for c in concepts.getConcepts().values():
            for d in c.getConcepts().values():
                for e in d.name.split():
                    graph.addConcepts(Concepts(e, d.typeName))

        for c in concepts.getConcepts().values():
            for d in c.getConcepts().values():
                i = 0
                for e in d.name.split():
                    if i == 0:
                        parentNode = Concepts(e, d.typeName)
                    else:
                        graph.addEdge(parentNode, Concepts(e, d.typeName))
                    i += 1
    
   
if __name__ == "__main__":
    listConceptFile = list()
    #listConceptFile.append("documents.p")
    #listConceptFile.append("NVPChunks.p")
    listConceptFile.append("Chunks.p")
    
    graph1 = NetworkXGraph()
    createGraph(graph1)
    
    graph2 = PatternGraph()
    createGraph(graph2)
        
    if isinstance(graph1, NetworkXGraph):
        #graph.G.remove_node("ProjectConceptsSimilarity")
        #graph.drawGraph("concepts.png")
        filename = "concepts.net"
        logger.info("Saving Graph - %s" % filename)
        graph1.saveGraphPajek(filename)
        graph1.saveGraph("concepts.gml")
        
    if isinstance(graph2, PatternGraph):
        #graph.g.remove("ProjectConceptsSimilarity")
        logger.info("Exporting Graph")
        graph2.exportGraph()





