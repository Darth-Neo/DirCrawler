import os
import sys
import re
import time
import unicodedata

from CountTerms import *
from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from nl_lib import Logger
logger = Logger.setupLogging(__name__)
logger.setLevel(Logger.INFO)


class OutVer(object):
    d = None
    concepts = None
    trnd = None

    def __init__(self, filename):
        self.filename = filename
        self.trnd = dict()
        self.concepts = Concepts(u"OTRN", u"Transaction")

    def setTran(self, r):
        otrn = r[:9]

        if otrn in self.trnd:
            # determnine unique tran
            logger.debug(u"%s - %s" % (r, otrn))
            self.d = self.trnd[otrn].addConceptKeyType(otrn, u"OTRN")
            self.d.addConceptKeyType(r, otrn)
        else:
            # determnine unique tran
            c = self.concepts.addConceptKeyType(otrn, u"OTRN")
            d = c.addConceptKeyType(r, u"ry")
            self.trnd[otrn] = c
            self.d = self.trnd[otrn]
            logger.debug(u"%s - %s" % (r, otrn))

        return self.d

    def setTranEnttries(self, r):

        if self.d is None:
            d = self.setTran(r)
        else:
            d = self.d

        return d

    def setEntity(self, r):

        otrn = r[:9]
        ty = otrn[:-4]

        self.setTranEnttries()

        ty = r[:-4]

        self.d.addConceptKeyType(r, otrn)
        nc = process_equation(r)
        # e.addConcept(nc)

    def process(self):
        count_other = 0
        count_otrn = 0
        d = None

        with open(filename, u"ro") as f:
            n = 0

            while True:
                r = unicode(f.readline().decode(u'ascii', u'ignore'))
                n += 1

                if r == u"":
                    break

                if re.search(r"^#.*", r, re.M|re.I):
                    logger.debug(u"Comment - %s" % r)

                elif re.search(r"^OTRN.+", r, re.M|re.I):
                    self.setTran(r)
                    logger.info(u"OTRN %s" % r[:-1])
                    count_otrn += 1

                # elif re.search(r"^[A-Z=]{5}.+", r, re.M|re.I):
                #    self.setEntity(r)
                #    count_other += 1
                #    logger.info(u"%d    %s" % (count_other, r))

                else:
                    logger.debug(u"=====Skipped===== - %s" % r)

        return self.concepts

if __name__ == u"__main__":

    cwd = os.getcwd()

    filename = cwd + os.sep + u"outver.ini"

    p = OutVer(filename)

    concepts = p.process()

    Concepts.saveConcepts(concepts, filename + u".p")

    # concepts.logConcepts()
