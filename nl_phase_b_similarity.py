#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.TopicsModel import TopicsModel

import Queue
import threading
import time

num_topics = 100
similarity = 0.95

ThreadDepth = 20
QueueDepth  = 1500
QueueDelta  = 50
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
        logger.info("Starting %s" % self.threadID)
        
        while not exitFlag:
            logger.debug("runAquire Queue Lock - ThreadID[%s]" % (self.threadID))
            queueLock.acquire()
            
            if workQueue.qsize() > 0:
                logger.debug("Get Queue - ThreadID[%s]" % (self.threadID))
                data = workQueue.get()
                
                logger.debug("Process Row - row[%s]" % (data[1]))
                self.npbt.doComputation(data[0], data[1])
                
                logger.debug("runRelease Queue Lock - ThreadID[%s]" % (self.threadID))
                queueLock.release()
            else:
                logger.debug("runRelease Queue Lock - ThreadID[%s]" % (self.threadID))
                queueLock.release()    
                
            time.sleep(1)
            
        logger.info("Exiting %s" % self.threadID)

class nl_phase_b_topics(object):
    conceptsSimilarity = None
    tm = None
    documentsList = None
    wordcount = None
    threads = None
    
    def __init__(self):
        self.threads = list()
    
    def createTopics(self, conceptsFile, conceptsSimilarityFile):
    
        logger.info("Load Concepts from " + conceptsFile)
        concepts = Concepts.loadConcepts(conceptsFile)
        logger.info("Loaded Concepts")

        self.tm = TopicsModel()

        logger.info("Load Documents from Concepts")
        self.documentsList, self.wordcount = self.tm.loadWords(concepts)

        logger.info("Read " + str(len(self.documentsList)) + " Documents, with " + str(self.wordcount) + " words.")

        logger.info("Compute Topics")
        topics = self.tm.computeTopics(self.documentsList, nt=num_topics)

        self.tm.logTopics(topics)

        logger.info("Saving Topics")
        topicsConcepts = self.tm.saveTopics(topics)

        logger.info("Compute Similarity")

        self.conceptsList = [x for x in concepts.dictChildrenType("Concepts").keys()]

        self.conceptsSimilarity = Concepts("ConceptsSimilarity", "Similarities")

        # Compute similarity between documents / concepts
        similarityThreshold = similarity

        # startup the threads
        for threadID in range(0,ThreadDepth):
            thread = myThread(threadID, self)
            thread.start()
            self.threads.append(thread)
        
        for j in self.documentsList:
            indexNum = self.documentsList.index(j)
            logger.info("conceptsList[" + str(indexNum) + "]=" + str(self.projectList[indexNum]))
            logger.debug("documentsList[" + str(indexNum) + "]=" + str(j))

            #self.doComputation(j, similarityThreshold)

            logger.debug("npbtAquire  Queue Lock")
            queueLock.acquire()
            logger.debug("npbtPut     Queue     ")
            rl = [j, similarityThreshold]
            while workQueue.qsize() == QueueDepth:
                time.sleep(1)
            workQueue.put(rl)
            queueLock.release()
            logger.debug("npbtRelease Queue Lock")

            qs = workQueue.qsize()
            if qs % QueueDelta == 0:
                logger.info("rQueue Size = %s" % qs)

        # Wait for queue to empty
        qs = workQueue.qsize()
        while qs != 0:
            time.sleep(1)
            qs = workQueue.qsize()
            if qs % QueueDelta == 0:
                logger.info("wQueue Size = %s" % qs)

        # Notify threads it's time to exit
        exitFlag = 1

        # Wait for all threads to complete
        for t in self.threads:
            logger.info("Waiting for thread %s to end..." % t)
            t.join(0.5)
            
        #self.conceptsSimilarity.logConcepts()

        Concepts.saveConcepts(self.conceptsSimilarity, conceptsSimilarityFile)

        logger.info("Complete createTopics")

    def doComputation(self, j, similarityThreshold):
        
        pl = self.tm.computeSimilar(self.documentsList.index(j), self.documentsList, self.conceptsList, similarityThreshold)

        if len(pl) != 0:
            logger.debug("   similarity above threshold")
            logger.debug("pl:" + str(pl))

            for l in pl:
                logger.info("l:" + str(l))
                ps = self.conceptsSimilarity.addConceptKeyType(l[0], "Similar")
                ps.count = TopicsModel.TopicsModel.convertMetric(l[2])
                #rt1 = ps.addConceptKeyType(str(l[3]), "SimilarTopics")
                #rt1 = len(l[3])
                pt = ps.addConceptKeyType(l[1], "Concept")
                #rt2 = pt.addConceptKeyType(str(l[4]), "ProjectTopics")
                #rt2.count = len(l[4])
                common = set(l[3]) & set(l[4])
                lc = [x for x in common]
                for x in common:
                    pc = pt.addConceptKeyType(x, "CommonTopic")
                    pc.count = len(lc)
                
        else:
            logger.debug("   similarity below threshold")

if __name__ == "__main__":
    npbt = nl_phase_b_topics()
    npbt.createTopics("documents.p", "documentsSimilarity.p")



