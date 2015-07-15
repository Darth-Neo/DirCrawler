#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

import logging
logger.setLevel(logging.INFO)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.TopicsModel import TopicsModel

import Queue
import threading
import time

THREAD = False

num_topics = 100
num_words  = 100
similarity = 0.80

ThreadDepth = 10
QueueDepth  = 150
QueueDelta  = 5
exitFlag    = 0

queueLock = threading.Lock()
workQueue = Queue.Queue(QueueDepth)

class myThread (threading.Thread):
    threadID = None
    npbt = None
    
    def __init__(self, threadID, npbt):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.npbt = npbt
        
    def run(self):
        logger.info(u"Starting %s" % self.threadID)
        
        while not exitFlag:
            logger.debug(u"runAquire Queue Lock - ThreadID[%s]" % (self.threadID))
            queueLock.acquire()
            
            if workQueue.qsize() > 0:
                logger.debug(u"Get Queue - ThreadID[%s]" % (self.threadID))
                data = workQueue.get()
                
                logger.debug(u"Process Row - row[%s]" % (data[1]))
                self.npbt.doComputation(data[0], data[1])
                
                logger.debug(u"runRelease Queue Lock - ThreadID[%s]" % (self.threadID))
                queueLock.release()
            else:
                logger.debug(u"runRelease Queue Lock - ThreadID[%s]" % (self.threadID))
                queueLock.release()    
                
            time.sleep(1)
            
        logger.info(u"Exiting %s" % self.threadID)

class DocumentsSimilarity(object):
    concepts = None
    conceptsSimilarity = None
    tm = None
    documentsList = None
    wordcount = None
    threads = None
    topics = None
    topicConcepts = None
    
    def __init__(self):
        self.threads = list()
    
    def createTopics(self, conceptsFile):
    
        logger.info(u"Load Concepts from " + conceptsFile)
        self.concepts = Concepts.loadConcepts(conceptsFile)
        logger.info(u"Loaded Concepts")

        self.tm = TopicsModel()

        logger.info(u"Load Documents from Concepts")
        self.documentsList, self.wordcount = self.tm.loadConceptsWords(self.concepts)

        logger.info(u"Read " + str(len(self.documentsList)) + u" Documents, with " + str(self.wordcount) + u" words.")

        if self.wordcount == 0:
            logger.error(u"No topics to use!")
            return None

        logger.info(u"Compute Topics")
        self.topics = self.tm.computeTopics(self.documentsList, nt=num_topics, nw=num_words)

        logger.info(u"Log Topics")
        self.tm.logTopics(self.topics)

        self.listTopics = [unicode(x[0]).strip().replace(u"\"", u"") for x in self.topics]

        logger.info(u"Saving Topics")
        self.topicConcepts = self.tm.saveTopics(self.topics)

    def findSimilarties(self, conceptsSimilarityFile):

        logger.info(u"Compute Similarity")

        self.conceptsSimilarity = Concepts(u"ConceptsSimilarity", u"Similarities")

        # Compute similarity between documents / concepts
        similarityThreshold = similarity

        if THREAD:
            # startup the threads
            for threadID in range(0,ThreadDepth):
                thread = myThread(threadID, self)
                thread.start()
                self.threads.append(thread)

        for document in self.documentsList:
            indexNum = self.documentsList.index(document)

            df = self.concepts.getConcepts().keys()

            logger.info(u"Document %s" % (df[indexNum]))

            logger.info(u"  documentsList[" + str(indexNum) + u"]=" + str(document))

            # Show common topics
            d = [unicode(x).strip().replace(u"'", u"") for x in document]
            e = [unicode(y).strip().replace(u"\"", u"") for y in self.listTopics]

            s1 = set(e)
            s2 = set(d)
            common = s1 & s2
            lc = [x for x in common]
            logger.info(u"  Common Topics : %s" % (lc))

            if THREAD is False:
                self.doComputation(document, similarityThreshold)

            else:
                logger.debug(u"npbtAquire  Queue Lock")
                queueLock.acquire()
                logger.debug(u"npbtPut     Queue     ")
                rl = [document, similarityThreshold]
                while workQueue.qsize() == QueueDepth:
                    time.sleep(1)
                workQueue.put(rl)
                queueLock.release()
                logger.debug(u"npbtRelease Queue Lock")

                qs = workQueue.qsize()
                if qs % QueueDelta == 0:
                    logger.info(u"rQueue Size = %s" % qs)

                # Wait for queue to empty
                qs = workQueue.qsize()
                while qs != 0:
                    time.sleep(1)
                    qs = workQueue.qsize()
                    if qs % QueueDelta == 0:
                        logger.info(u"wQueue Size = %s" % qs)

                # Notify threads it's time to exit
                exitFlag = 1

                # Wait for all threads to complete
                for t in self.threads:
                    logger.info(u"Waiting for thread %s to end..." % t)
                    t.join(0.5)

        Concepts.saveConcepts(self.conceptsSimilarity, conceptsSimilarityFile)

        logger.info(u"Complete createTopics")

    def doComputation(self, j, similarityThreshold):
        
        pl = self.tm.computeSimilar(self.documentsList.index(j), self.documentsList, similarityThreshold)

        if len(pl) != 0:
            logger.debug(u"   similarity above threshold")
            logger.debug(u"   pl:" + str(pl))

            for l in pl:
                if l[1] != l[2]:
                    logger.debug(u"  l:" + str(l))
                    ps = self.conceptsSimilarity.addConceptKeyType(l[1], u"Similar")
                    ps.count = TopicsModel.convertMetric(l[0])
                    # rt1 = ps.addConceptKeyType(str(l[3]), "SimilarTopics")
                    # rt1 = len(l[3])
                    pt = ps.addConceptKeyType(l[2], u"Concept")
                    # rt2 = pt.addConceptKeyType(str(l[4]), "ProjectTopics")
                    # rt2.count = len(l[4])
                    common = set(l[1]) & set(l[2])
                    lc = [x for x in common]

                    logger.debug(u"  l[1] : %s" % (l[1]))
                    logger.debug(u"  l[2] : %s" % (l[2]))
                    logger.debug(u"  Common : %s" % (lc))
                    for x in common:
                        pc = pt.addConceptKeyType(x, u"CommonTopic")
                        pc.count = len(lc)
                
        else:
            logger.debug(u"   similarity below threshold")

if __name__ == u"__main__":
    os.chdir(u"run")

    npbt = DocumentsSimilarity()
    # npbt.createTopics("documents.p")
    npbt.createTopics(u"chunks.p")

    npbt.findSimilarties(u"documentsSimilarity.p")


