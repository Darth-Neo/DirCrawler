#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
import os
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

import logging
logger.setLevel(logging.INFO)

from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, GraphVizGraph
from nl_lib.Constants import *

class ConceptsGraph(object):

    def __init__(self, graph=None, fileImage=None):
        self.threshold=0.0005

        if graph is None:
            # self.graph = PatternGraph()
            self.graph = GraphVizGraph()
        else:
            self.graph = graph

        if fileImage is None:
            self.fileImage = u"example.png"
        else:
            self.fileImage = fileImage

        #
        # Hack to get GraphViz to work
        #
        os.environ[u'PATH'] = u"%s:/Users/morrj140/local/homebrew/bin/" % os.environ[u'PATH']



    def addGraphNodes(self, concepts, n=0):

        n += 1

        for c in concepts.getConcepts().values():
                logger.info(u"%d : %d Node c : %s:%s" % (n, len(c.getConcepts()), c.name, c.typeName))

                c.name = c.name[:20]

                self.graph.addConcept(c)

                if len(c.getConcepts()) > self.threshold:
                    self.addGraphNodes(c, n)

    def addGraphEdges(self, concepts, n=0):
        n += 1

        self.graph.addConcept(concepts)

        for c in concepts.getConcepts().values():

            logger.debug(u"%d : %d %s c : %s:%s" % (n, len(c.getConcepts()), concepts.name, c.name, c.typeName))

            self.graph.addConcept(c)

            self.graph.addEdge(concepts, c)

            if len(c.getConcepts()) != 0:
                self.addGraphEdges(c, n)

    def conceptsGraph(self, concepts):

        logger.info(u"Adding %s nodes the graph ..." % type(self.graph))
        self.addGraphNodes(concepts)

        logger.info(u"Adding %s edges the graph ..." % type(self.graph))
        self.addGraphEdges(concepts)

        if isinstance(self.graph, GraphVizGraph):
            self.graph.exportGraph(filename=self.fileImage)
            logger.info(u"Saved Graph - %s" % self.fileImage)

        if isinstance(self.graph, PatternGraph):
            # graph.g.remove("ProjectConceptsSimilarity")
            logger.info(u"Exporting Graph")
            self.graph.exportGraph()

    def logGraph(self, gl, title, scale=1):
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
    # conceptFile = u"archi.p"

    logger.info(u"%s" % os.getcwd())

    os.chdir(u"." + os.sep + u"t34_20151004_151638")

    if False:
        graph = PatternGraph()
    else:
        graph = GraphVizGraph()

    concepts = Concepts.loadConcepts(conceptFile)

    # c.logConcepts()
    
    cg = ConceptsGraph(graph=graph, fileImage=conceptFile[:-2]+u".png")

    cg.conceptsGraph(concepts)

    



