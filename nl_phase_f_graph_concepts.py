#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
import os
from nl_lib.Logger import *
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, GraphVizGraph, NetworkXGraph
from nl_lib.Constants import *

logger = setupLogging(__name__)
logger.setLevel(DEBUG)

def logGraph(gl, title, scale=1):
    logger.info(u"---%s---" % title)
    n = 0
    for x in gl:
        n += 1
        if isinstance(gl, dict):
            logger.info(u"%s [%d]:%s=%3.4f" % (title, n, x, gl[x]*scale))

        else:
            logger.info(u"%s [%d]" % (x, n))

if __name__ == u"__main__":
    # conceptFile = u"documents.p"
    # conceptFile = u"words.p"
    # conceptFile = u"NVPChunks.p"
    # conceptFile = u"chunks.p"
    # conceptFile = u"topicsDict.p"
    # conceptFile = u"TopicChunks.p"
    # conceptFile = u"ngrams.p"
    # conceptFile = u"ngramscore.p"
    conceptFile = u"ngramsubject.p"

    logger.info(u"%s" % os.getcwd())
    os.chdir(u"." + os.sep + u"run")

    concepts = Concepts.loadConcepts(conceptFile)

    if logger.getEffectiveLevel() == DEBUG:
        concepts.logConcepts()

    # graph = PatternGraph()
    # graph = GraphVizGraph()
    graph = NetworkXGraph(conceptFile[:-2]+u".png")

    graph.addGraphNodes(concepts)
    graph.addGraphEdges(concepts)

    if len(concepts.getConcepts()) < 0:
        logger.error(U"Zero Concepts")

    else:
        if isinstance(graph, NetworkXGraph):
            graph.drawGraph(GML_ONLY=True)

        elif isinstance(graph, GraphVizGraph):
            graph.exportGraph()

        elif isinstance(graph, PatternGraph):
            graph.exportGraph()


