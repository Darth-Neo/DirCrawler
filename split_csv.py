#!/usr/bin/python
#
# Natural Language Processing of Information
#
import os
import sys
from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from nl_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


def split(filename,des):
    r = list()

    with open(filename, "rb") as f:
        r = f.readlines()

    s = r[0].split("\r")

    n = 0
    for x in s:
        of = "%s%d.csv" % (des, n)
        logger.info(u"%s ===> %s" % (of, x.decode("utf8", errors="replace")))

        with open(of, "wb") as h:
            h.write(x)

        n += 1

    return r

if __name__ == u"__main__":

    os.chdir(u"RTP/BR_TR")

    try:
        os.rmdir(u"req")

    except Exception, msg:
        logger.debug(u"...%s" % msg)

    os.mkdir(u"req")
    os.chdir(u"req")

    logger.info(u"%s" % os.getcwd())

    split(u"../BR_201603251241.csv", u"br_")
    split(u"../TR_201603251241.csv", u"tr_")

