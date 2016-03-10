import os
import sys
import re
import time

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from nl_lib import Logger
logger = Logger.setupLogging(__name__)
logger.setLevel(Logger.DEBUG)

if __name__ == u"__main__":

    cwd = os.getcwd()
    logger.info(u"%s" % cwd)

    if True:
        filename = cwd + os.sep + u"outver.ini"
        cn = "OUTVER"
    else:
        filename = cwd + os.sep + u"inver.ini"
        cn = "INVER"

    n = 0

    dd = None
    ee = None

    concepts = Concepts(u"TRAN", cn)

    with open(filename, u"ro") as f:

        if True : # try:
            while True:
                r = f.readline()
                n += 1

                if r == "":
                    break

                qmatch = re.search(r"^#.+", r, re.M|re.I)
                # qmatch = re.match(r"^#+", r, re.M|re.I)

                logger.debug(u"%d" % n)

                if re.search(r"^# @.+", r, re.M|re.I):
                    key = r[1:-2].strip(" ")
                    logger.info(u"%d - %s %s" % (n, key, u"@SYM"))
                    d = concepts.addConceptKeyType(key, u"@SYM")

                elif re.search(r"^TRAN.+", r, re.M|re.I):
                    logger.debug(u"%d - Input Transaction" % n)
                    dd = concepts.addConceptKeyType(r, u"TRAN")

                elif re.search(r"^RECD.+", r, re.M|re.I):
                    logger.debug(u"%d - Input Record" % n)
                    ee = dd.addConceptKeyType(r, u"RECD")

                elif re.search(r"^FILD.+", r, re.M|re.I):
                    logger.debug(u"%d - Input Field" % n)
                    ee.addConceptKeyType(r, u"FILD")

                elif re.search(r"^AUDT.+", r, re.M|re.I):
                    logger.debug(u"%d - Audit Field" % n)
                    ee.addConceptKeyType(r, u"AUDT")

                elif re.search(r"^UPFS.+", r, re.M|re.I):
                    logger.debug(u"%d - UPFS Field" % n)
                    ee.addConceptKeyType(r, u"UPFS")

                elif re.search(r"^\s", r, re.M|re.I):
                    logger.debug(u"%d - Skip retunn line" % n)

                elif re.search(r"^#.+", r, re.M|re.I):
                    logger.debug(u"%d Skip comment line" % n)

                elif re.search(r"^.+\s", r, re.M|re.I):

                    # ugly way to remove new line and carrage return
                    r = r[:-2]

                    fld = r.split(u"=")

                    values = fld[1].split(",")
                    collection = fld[0] + "|" + values[0] + "|" + values[1]
                    logger.info(u"%d %s" % (n, collection))

                    d = concepts.addConceptKeyType(collection, u"PARSED")

                    logger.debug(u"%d fld : %s" % (n, fld))

                    for x in fld[1].split(u","):
                        logger.debug(u"x : %s" % x)
                        e = d.addConceptKeyType(x, u"Field")

                r = f.readline()
        else: # except Exception, m:
            pass
            logger.info(u"Ops %s" % m)

    # concepts.logConcepts()
    Concepts.saveConcepts(concepts, filename + u".p")
