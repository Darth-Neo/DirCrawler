#
# deconflict csv as each row is a file
#
import os
import sys
from nl_lib.Concepts import *

from nl_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


def breakoutCSV(csvFile):

    n = 0

    if not os.path.exists(csvFile):
        logger.error(u"%s : Does Not Exist!" % csvFile)
        return

    logger.info(u"%s" % os.getcwd())

    with open(csvFile, "r") as g:
        inputLines = g.readlines()

    input = "%s" % inputLines[0]

    for x in input.split("\r"):

        n += 1

        if n == 1:
            header = x
            continue

        try:
            y = x.split(u",")

            txtFile = u"%d_%s.txt" % (n, y[0])

            with open(txtFile, "w") as f:
                output = "%s. %s" % (y[2], y[1])
                f.write(output)

        except Exception, msg:
            logger.debug(u"%d: %s" % (n, msg))

def findTextClusters():
    os.chdir(u"run")

    docConceptFile = u"documents.p"
    logger.info(u"Loading :" + docConceptFile)
    docConcepts = Concepts.loadConcepts(docConceptFile)

    dc = docConcepts.getConcepts()

    simConceptFile = u"documentsSimilarity.p"
    logger.info(u"Loading :" + simConceptFile)
    simConcepts = Concepts.loadConcepts(simConceptFile)

    for rdoc in simConcepts.getConcepts().values():
        simHead, simTail = os.path.split(rdoc.name)
        dcvfilename = dc[rdoc.name]
        dcvn = dcvfilename.getConcepts().values()[0]

        logger.info(u"%s - %s     " % (simTail[:-4].split(u"_")[0], dcvn.name.strip(u"\"")))
        logger.debug(u"%s[%s]" % (simTail, dcvn.name))
        logger.debug(u"%s[%s]" % (dcvfilename.name, dcvn.name))

        for v in rdoc.getConcepts().values():
            vHead, vTail = os.path.split(v.name)
            sdc = dc[v.name]

            sdcvn = sdc.getConcepts().values()[0].name

            logger.info(u"    %s - %s" % (vTail[:-4].split(u"_")[0], sdcvn))



if __name__ == u"__main__":

    # os.chdir(u"dvc")
    # csvFile = u"DVC.csv"
    # breakoutCSV(csvFile)

    findTextClusters()


