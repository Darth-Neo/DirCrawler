from nl_lib.Concepts import Concepts

from nl_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

if __name__ == u"__main__":

    if True:
        conceptFile = u"outver.ini.p"
        searchTrans = "OFLD|1226"
    else:
        conceptFile = u"inver.ini.p"
        searchTrans = "*"

    logger.info(u"Loading :" + conceptFile)
    concepts = Concepts.loadConcepts(conceptFile)

    if True:
        # concepts.logConcepts()

        on = concepts.name
        tn = concepts.typeName
        logger.info(u"%s,%s" % (on, tn))

        for otrn in concepts.getConcepts().values():
            logger.info(u"    %s[%s]" % (otrn.name, otrn.typeName))
            for entries in otrn.getConcepts().values():
                logger.info(u"        %s[%s]" % (entries.name, entries.typeName))
                for se in otrn.getConcepts().values():
                    logger.info(u"            %s[%s]" % (se.name, se.typeName))

    else:
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

