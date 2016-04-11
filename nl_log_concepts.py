#!/usr/bin/python
#
# Natural Language Processing of Information
#
import os
import sys
import pickle
from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from nl_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

failures = 0


def check(c, d):
    global failures
    f = u"not found"

    s = os.path.basename(c)

    logger.info("s : %s" % s)

    try:
        logger.info("d[s] : %s" % d[s])
        g = d[s]
        f = g.decode("ascii", errors="replace")
        logger.info("f : %s" % f)

    except Exception, msg:
        failures += 1
        logger.error(u"%d %s" % (failures, msg))

    return f


def logConcepts(c, d, nf, m=0, n=0):
    pc = c.getConcepts()
    spaces = u"" # u"    " * n
    f = logger.info

    for p in pc.values():
        # pp(u"%s%s[%d]{%s}->Count=%s" % (spaces, p.name, len(p.name), p.typeName, p.count))
        f = check(p.name, d)

        try:
            g = u"".join([c for c in f if c < 127])

        except Exception, msg:
            logger.warn(u"%s" % msg)

        if n > 0:
            nf.write("%d,%d,,%s%s%s" % (m, n, spaces, g, os.linesep))
        else:
            m += 1
            nf.write("%d,%d,%s%s%s" % (m, n, spaces, g, os.linesep))

        logConcepts(p, d, nf, m, n+1)


if __name__ == u"__main__":

    # os.chdir(u"test")
    os.chdir(u"run")

    logger.info(u"%s" % os.getcwd())

    # conceptFile = u"req_dist.d"

    # conceptFile = u"documents.p"
    # conceptFile = u"words.p"
    # conceptFile = u"chunks.p"

    # conceptFile = u"topicChunks.p"
    # conceptFile = u"topicsDict.p"

    conceptFile = u"documentsSimilarity.p"
    # conceptFile = u"NVPChunks.p"`
    # conceptFile = u"ngrams.p"
    # conceptFile = u"ngramscore.p"
    # conceptFile = u"ngramsubject.p

    logger.info(u"Loading :" + conceptFile)
    concepts = Concepts.loadConcepts(conceptFile)

    if False:
        with open("req_dist.d", "rb") as cf:
            d = pickle.load(cf)

        try:

            with open("Sim.csv", "wb") as nf:
                logConcepts(concepts, d, nf)

        except KeyboardInterrupt, msg:
            logger.info(u"Bye")

    elif False:
        for x in concepts.getConcepts():
            logger.info("%x" % d[x])

            for y in x.getConcepts():
                logger.info("%x" % y.name)

            concepts.printConcepts()
    elif False:
        # concepts.printConcepts()
        concepts.logConcepts()

    else:
        concepts.printConcepts()

