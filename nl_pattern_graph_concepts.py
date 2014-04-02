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
   
if __name__ == "__main__":
    listConceptFile = list()
    #listConceptFile.append("documents.p")
    listConceptFile.append("chunks.p")
    
    graph = NetworkXGraph()
    #graph = PatternGraph()

    for conceptFile in listConceptFile:
        logger.info("Loading :" + conceptFile)
        concepts = Concepts.loadConcepts(conceptFile)

        for c in concepts.getConcepts().values():
            graph.addConcepts(c)

    if isinstance(graph, PatternGraph):
        #graph.g.remove("ProjectConceptsSimilarity")
        logger.info("Exporting Graph")
        graph.exportGraph()

    if isinstance(graph, NetworkXGraph):
        #graph.G.remove_node("ProjectConceptsSimilarity")
        graph.drawGraph("concepts.png")
        filename = "concepts.net"
        logger.info("Saving Graph - %s" % filename)
        graph.saveGraphPajek(filename)





