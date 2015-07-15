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

    c = Concepts(u"GraphConcepts", u"GRAPH")

    logger.info(u"Loading Topics from : " + conceptFile)

    concepts = Concepts.loadConcepts(conceptFile)
    tc = TopicCloud(concepts, os.getcwd()+os.sep)
    tc.createTagCloud(topic)