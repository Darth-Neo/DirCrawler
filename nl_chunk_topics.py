#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib import Constants
from nl_lib import Concepts
from nl_lib import TopicsModel

num_topics = 100
similarity = 0.95

def createTopics(conceptFile):
    stopwords = list()
    stopwords.append("data")
    stopwords.append("applications")
    stopwords.append("systems")
    stopwords.append("s")
    stopwords.append("processes")
    stopwords.append("requirements")

    
    logger.info("Load Concepts from " + conceptFile)
    concepts = Concepts.Concepts.loadConcepts(conceptFile)
    logger.info("Loaded Concepts")

    tm = TopicsModel.TopicsModel()

    logger.info("Load Documents from Concepts")
    documentsList, wordcount = tm.loadWords(concepts)

    logger.info("Read " + str(len(documentsList)) + " Documents, with " + str(wordcount) + " words.")

    logger.info("Compute Topics")
    topics = tm.computeTopics(documentsList, nt=num_topics)

    tm.logTopics(topics)

    logger.info("Saving Topics")
    topicsConcepts = tm.saveTopics(topics)

    logger.info("Compute Similarity")

    conceptList = [x for x in concepts.dictChildrenType("Document").keys()]

    conceptsSimilarity = Concepts.Concepts("ConceptsSimilarity", "Similarities")

    # Compute similarity between documents / projects
    similarityThreshold = similarity
    
    for j in documentsList:
        indexNum = documentsList.index(j)
        logger.info("conceptList[" + str(indexNum) + "]=" + str(conceptList[indexNum]))
        logger.debug("documentsList[" + str(indexNum) + "]=" + str(j))
        
        pl = tm.computeSimilar(documentsList.index(j), documentsList, conceptList, similarityThreshold)

        if len(pl) != 0:
            logger.debug("   similarity above threshold")
            logger.debug("pl:" + str(pl))

            for l in pl:
                logger.info("l:" + str(l))
                ps = conceptsSimilarity.addConceptKeyType(l[0], "Similar")
                ps.addConceptKeyType(l[1], "Project")
                ps.count = TopicsModel.TopicsModel.convertMetric(l[2])
        else:
            logger.debug("   similarity below threshold")

    conceptsSimilarity.logConcepts()

    Concepts.Concepts.saveConcepts(conceptsSimilarity, Constants.similarityFile)

    logger.info("Complete createTopics")

if __name__ == "__main__":
    createTopics("chunks.p")



