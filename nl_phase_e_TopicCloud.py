#! env python
#
# Natural Language Processing of Information
#
import os

from nl_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.TopicCloud import TopicCloud

def createTopicsCloud(concepts, topic, numWords=30, scale=1):
    logger.info(u"Starting Tag Cloud...")

    tc = TopicCloud(concepts, os.getcwd()+os.sep)

    logger.info(u"Create Tag Cloud")

    # Note: the first parameter must match for a topic cloud image to be created!
    tc.createTagCloud(topic, size_x=1200, size_y=900, numWords=numWords, scale=scale)

    logger.info(u"Complete createTopicsCloud")


if __name__ == u"__main__":

    os.chdir(u"." + os.sep + u"run")

    conceptFile = None
    topic = None

    if False:
        conceptFile = u"TopicChunks.p"
        topic = u"Chunk"

    elif True:
        conceptFile = u"topicsDict.p"
        topic = u"Topic"

    elif False:
        conceptFile = u"archi.p"
        topic = u"name"

    elif False:
        conceptFile = u"ngramsubject.p"
        topic = u"NGRAM"

    elif False:
        conceptFile = u"req.p"
        topic = u"Word"

    elif False:
        conceptFile = u"chunks.p"
        # topic = u"Lemma"
        topic = u"SBJ"
        # topic = u"OBJ"
        # topic = u"VP"
        # topic = u"NN"
        # topic = u"NNP"

    elif False:
        conceptFile = u"ngrams.p"
        topic = u"NGRAM"

    logger.info(u"%s" % os.getcwd())

    c = Concepts(u"GraphConcepts", u"GRAPH")

    logger.info(u"Loading Topics from : " + conceptFile)

    concepts = Concepts.loadConcepts(conceptFile)

    createTopicsCloud(concepts, topic, numWords=30, scale=0.2)
