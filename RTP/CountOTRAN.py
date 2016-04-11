import os
import sys
import re
import time
import unicodedata

from CountTerms import *
from nl_lib import Logger
logger = Logger.setupLogging(__name__)
logger.setLevel(Logger.INFO)

listOREQ = list()


def addCountToDict(type, d):
    if type in d:
        d[type] += 1
    else:
        d[type] = 1

    return d


def checkRecord(st):

    global listOREQ

    os = u","
    l = st.split(u"=")
    cv = l[1]

    for a, b, c, d in listOREQ:
        if d == cv:
            os = a + u"," + c
            break

    return os


def process(infFile, outfile):
    PC = ","

    error_count = 0
    dCount = dict()
    line_count = 0

    start_time = time.time()
    strStartTime = time.asctime(time.localtime(start_time))
    logger.info(u"Start time : %s" % strStartTime)

    nrt = u""

    s = u"([{+-/*ABC"
    count, td, sc, terms = process_equation(s)

    with open(outfile, u"w") as g:
        g.write("Line,RT,RY,HT,Field,Count,%s,Type,Len,Logic,Line%s" % (terms, os.linesep))

        Show_OFLD_Only = True
        Show_OTRN = False
        Show_OREC = False
        Show_Line = False

        with open(infFile, u"r") as f:
            n = 0
            otrn = ""

            while True:

                r = unicode(f.readline().decode(u'ascii', u'ignore'))

                r = r.replace(os.linesep, ".")
                r = r.replace("\"", "'")
                r = r.replace("\\", "")
                r = r.replace("\n", "")
                r = r.replace("\r", "")

                rl = r.split(PC)

                if Show_Line:
                    endl = "%s%s" % (r, os.linesep)
                else:
                    endl = "%s" % os.linesep

                if r == u"":
                    break

                n += 1

                # Comment
                if re.search(r"^#.*", r, re.M|re.I):
                    logger.debug(u"Comment - %s" % r)

                # OTran
                elif re.search(r"^OTRN.+", r, re.M|re.I):

                    addCountToDict(r[:4], dCount)

                    ot = rl[2]
                    rt = rl[1]
                    it = rl[3]

                    if it[0] == u"I":
                        continue

                    count, td, sc, terms = process_equation(r[5:])

                    nrt = ot

                    l = u"OTRN,%s,%s,,,%4d,%s,,,,%s" % (ot, rt, count, sc, endl)
                    logger.info(u"%s" % l)

                    if Show_OFLD_Only is not True or Show_OTRN is True:
                        line_count += 1
                        g.write("%d,%s" % (line_count, l))

                # OREC
                elif re.search(r"^OREC.+", r, re.M|re.I):

                    addCountToDict(r[:4], dCount)

                    ot = rl[2]
                    rf = rl[1]
                    rv = rl[3]
                    rt = rl[7]

                    nl = list()
                    nl.append(ot)
                    nl.append(rf)
                    nl.append(rv)
                    nl.append(rt)
                    listOREQ.append(nl)

                    count, td, sc, terms = process_equation(r[5:])

                    l = u"OREC,%s,%s,%s,%4d,%s,,,,%s" % (ot, rf, rt, count, sc, endl)
                    logger.info(u"%s" % l)

                    if Show_OFLD_Only is not True or Show_OREC is True:
                        line_count += 1
                        g.write("%d,%s" % (line_count, l))

                # OGRP
                elif re.search(r"^OGRP.+", r, re.M|re.I):

                    addCountToDict(r[:4], dCount)

                    count, td, sc, terms = process_equation(r[5:])

                    l = u"OGRP,%s,%s,,%4d,%s,,,,%s" % (nrt, rt, count, sc, endl)
                    logger.debug(u"%s" % l)

                    if Show_OFLD_Only is not True:
                        line_count += 1
                        g.write("%d,%s" % (line_count, l))

                # OFLD
                elif re.search(r"^OFLD.+", r, re.M|re.I):

                    ft = fn = fl = fd = cv = ""

                    addCountToDict(r[:4], dCount)

                    try:
                        fd = rl[0]
                        fn = rl[2]
                        ft = rl[3]
                        fl = rl[4]
                        cv = rl[6]

                    except Exception, msg:
                        logger.error(u"%s" % msg)
                        error_count += 1

                    count, td, sc, terms = process_equation(cv)

                    v = checkRecord(fd)

                    if len(v) == 1:
                        continue

                    if not fl.isdigit():
                        fl = "G"

                    l = u"%s,%s,%s,%4d,%s,%s,%s,%s,,%s" % (v, rf, fn, count, sc, ft, fl, cv, endl)
                    logger.info(u"%s" % l)

                    if Show_OFLD_Only is True:
                        line_count += 1
                        g.write("%d,%s" % (line_count, l))

                # OCON
                elif re.search(r"^OCON.+", r, re.M|re.I):

                    addCountToDict(r[:4], dCount)

                    if nrt == u"":
                        nrt = u"begin"
                    else:
                        ot = r[:4]

                    rl = r.split(PC)
                    st = rl[1]

                    count, td, sc, terms = process_equation(r[5:])

                    rt = r[:4]

                    l = u"%s,%s,,,%4d,%s,,,,%s" % (rt, nrt, count, sc, endl)
                    logger.debug(u"%s" % l)

                    if Show_OFLD_Only is not True:
                        line_count += 1
                        g.write("%d,%s" % (line_count, l))

                else:
                    addCountToDict(r[:4], dCount)
                    logger.debug(u"=====Skipped===== - %s" % r)

        logger.info(u"Line  Count %d" % line_count)
        logger.info(u"Error Count %d" % error_count)

        for k, v in dCount.items():
            logger.info(u"%s Count = %d" % (k, v))

    return


def test_process():
    cwd = os.getcwd()
    infile = cwd + os.sep + u"test.ini"
    outFile = cwd + os.sep + u"testt.csv"

    process(infile, outFile)

if __name__ == u"__main__":

    if False:
        test_process()

    else:
        cwd = os.getcwd()

        infile = cwd + os.sep + u"OPVER.ini"
        outFile = cwd + os.sep + u"extract.csv"

        process(infile, outFile)


