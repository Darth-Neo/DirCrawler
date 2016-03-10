from nl_lib.Concepts import Concepts

from nl_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

if __name__ == u"__main__":

    if False:
        conceptFile = u"OUTVER.ini.p"
        searchTrans = "OFLD|1226"
    else:
        conceptFile = u"INVER.ini.p"
        searchTrans = "*"

    logger.info(u"Loading :" + conceptFile)
    concepts = Concepts.loadConcepts(conceptFile)

    # concepts.logConcepts()

    m = 0
    for k, v in concepts.getConcepts().items():
        kt = k[0:9]
        if kt == searchTrans or searchTrans == "*":
            logger.info("%d %s" % (m, k))
            m += 1

            n = 0
            for k1, v1 in v.getConcepts().items():
                logger.info("%d        %s" % (n, k1))
                n += 1

