import os
import sys
import re
import time
import unicodedata

from CountTerms import *
from nl_lib import Logger
logger = Logger.setupLogging(__name__)
logger.setLevel(Logger.INFO)


def process(infFile, outfile):
    count_other = 0
    count_otrn = 0
    d = None

    pr = None

    rl = list()
    pt = list()
    PC = "~"
    error_count = 0

    start_time = time.time()
    strStartTime = time.asctime(time.localtime(start_time))
    logger.info(u"Start time : %s" % strStartTime)

    nrt = u""

    with open(outfile, u"w") as g:
        g.write("TRN,RT,RY,I|P,Count,Entry,EntryCount,Paren,ParenCount,Minus,MinusCount,Plus,PlusCount,Div,DivCount,LP,LPCount,CLP,CLPCount,Mult,MultCount,Entry_INI,Type,Len,Logic,Flag,INI_Line%s" % os.linesep)

        with open(infFile, u"r") as f:
            n = 0
            otrn = ""

            while True:
                r = unicode(f.readline().decode(u'ascii', u'ignore'))

                r = r.replace(",", PC)
                r = r.replace(os.linesep, ".")
                r = r.replace("\"", "'")
                r = r.replace("\n", "")
                r = r.replace("\r", "")

                n += 1

                if r == u"":
                    break

                if re.search(r"^#.*", r, re.M|re.I):
                    logger.debug(u"Comment - %s" % r)

                # OTran
                elif re.search(r"^OTRN.+", r, re.M|re.I):

                    ot = r[7:9]
                    rt = r[10:13]
                    it = r[14:15]

                    if len(pt) == 0:
                        pt = list()
                        pt.append(ot)

                    count, td, sc = process_equation(r[5:])

                    nrt = ot

                    l = u"OTRN,%s,%s,%s,%4d,%s,,,,,%s%s" % (ot, rt, it, count, sc, r, os.linesep)
                    logger.info(u"%s" % l)
                    g.write(l)

                    count_otrn += 1

                # OREC
                elif re.search(r"^OREC.+", r, re.M|re.I):

                    ot = r[7:9]
                    rf = r.split("~")[3]

                    count, td, sc = process_equation(r[5:])

                    rt = r[10:13]
                    l = u"OREC,%s,%s,%s,%4d,%s,,,,,%s%s" % (ot, rt, rf, count, sc, r, os.linesep)

                    logger.info(u"%s" % l)
                    g.write(l)

                # OGRP
                elif re.search(r"^OGRP.+", r, re.M|re.I):

                    count, td, sc = process_equation(r[5:])

                    l = u"OGRP,%s,%s,,%4d,%s,,,,,%s%s" % (nrt, rt, count, sc, r, os.linesep)

                    logger.info(u"%s" % l)
                    g.write(l)

                # OFLD
                elif re.search(r"^OFLD.+", r, re.M|re.I):

                    fn = u""
                    ft = u""
                    cv =u""
                    eq = u""
                    try:
                        rl = r.split(PC)
                        fn = rl[2]
                        ft = rl[3]
                        fnl = r[5]
                        cv = rl[6]
                        eq = rl[7]

                    except Exception, msg:
                        logger.error(u"%s" % msg)
                        error_count += 1

                    count, td, sc = process_equation(r[5:])

                    l = u"OFLD,%s,%s,,%4d,%s,%s,%s,%s,%s,%s%s" % (nrt, fn, count, sc, ft, fnl, cv, eq, r, os.linesep)

                    logger.info(u"%s" % l)
                    g.write(l)


                # OCON
                elif re.search(r"^OCON.+", r, re.M|re.I):

                    if nrt == u"":
                        nrt = u"begin"
                    else:
                        ot = r[:4]

                    rl = r.split(PC)
                    st = rl[1]

                    count, td, sc = process_equation(r[5:])

                    rt = r[:4]

                    l = u"%s,%s,,,%4d,%s,,,,,%s%s" % (rt, nrt, count, sc, r, os.linesep)

                    logger.info(u"%s" % l)
                    g.write(l)

                # Default
                elif re.search(r"^[A-Z=]{5}.+", r, re.M|re.I):

                    if nrt == u"":
                        nrt = u"begin"

                    count, td, sc = process_equation(r[5:])

                    rt = r[:4]

                    l = u"%s,%s,,,%4d,%s,,,,,%s%s" % (rt, nrt, count, sc, r, os.linesep)

                    logger.info(u"%s" % l)
                    g.write(l)

                else:
                    logger.debug(u"=====Skipped===== - %s" % r)

        logger.info("Error Count %d" % error_count)

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

        infile = cwd + os.sep + u"T_outver.ini"
        outFile = cwd + os.sep + u"extraxt.csv"

        process(infile, outFile)


