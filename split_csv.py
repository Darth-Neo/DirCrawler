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


def split(filename, des, d):

    with open(filename, "rb") as f:
        r = f.readlines()

        n = 0
        for x in r:

            try:
                of = "%s%d.csv" % (des, n)

                if x is None:
                    continue

                # sx = x.decode("ascii", errors="replace")
                sx = ''.join([i if ord(i) < 128 else ' ' for i in x])

                logger.info(u"%s ===> %s" % (of, sx))

                with open(of, "wb") as h:
                    h.write(sx)

                d[of] = x
                n += 1

            except Exception, msg:
                logger.error(u"%s" % msg)

    return d


if __name__ == u"__main__":


    os.chdir(u"/Users/morrj140/Development/GitRepository/DirCrawler/RTP/Similarity")

    sbd = u"./req/"

    try:
        for root, dirs, files in os.walk(sbd, topdown=True):
            for name in files:
                name = sbd + name
                os.remove(name)

        os.rmdir(u"req")

    except Exception, msg:
        logger.debug(u"...%s" % msg)

    os.mkdir(u"req")
    os.chdir(u"req")

    logger.info(u"%s" % os.getcwd())

    d = dict()

    d = split(u"../RTP_REQ.csv", u"br_", d)
    # d = split(u"../TR_201603251241.csv", u"tr_", d)

    with open("../req_dist.d", u"wb") as cf:
            pickle.dump(d, cf)

