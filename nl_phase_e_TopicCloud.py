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
    logger.info("Starting Tag Cloud...")

    tc = TopicCloud(concepts, os.getcwd()+os.sep)

    logger.info("Create Tag Cloud")

    # Note: the first parameter must match for a topic cloud image to be created!
    tc.createCloudImage(topic, size_x=1200, size_y=900, numWords=numWords, scale=scale)

    logger.info("Complete createTopicsCloud")


if __name__ == "__main__":

    os.chdir("." + os.sep + "t34_20151004_151638")

    conceptFile = None
    topic = None

    if False:
        conceptFile = "TopicChunks.p"
        topic = "Chunk"

    elif True:
        conceptFile = "topicsDict.p"
        topic="Topic"

    elif False:
        conceptFile = "archi.p"
        topic="name"

    elif False:
        conceptFile = "ngramsubject.p"
        topic="NGRAM"

    elif False:
        conceptFile = "req.p"
        topic = "Word"

    elif False:
        conceptFile = "chunks.p"
        #topic = "Lemma"
        topic = "SBJ"
        #topic = "OBJ"
        #topic = "VP"
        #topic = "NN"
        #topic = "NNP"

    elif False:
        conceptFile = "ngrams.p"
        topic = "NGRAM"

    logger.info("%s" % os.getcwd())

    c = Concepts("GraphConcepts", "GRAPH")

    logger.info("Loading Topics from : " + conceptFile)

    concepts = Concepts.loadConcepts(conceptFile)

    createTopicsCloud(concepts, topic, numWords=30, scale=0.2)
