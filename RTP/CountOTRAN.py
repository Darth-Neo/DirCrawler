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
    ocon_count = 0
    otrn_count = 0
    rec_count = 0
    field_count = 0
    error_count = 0
    ogrp_count = 0

    start_time = time.time()
    strStartTime = time.asctime(time.localtime(start_time))
    logger.info(u"Start time : %s" % strStartTime)

    nrt = u""

    # st = "Vars"
    # st = "["
    # st = "{"
    # st = "("
    # st = "minus"
    # st = "plus"
    # st = "div"
    # st = "mult"



    with open(outfile, u"w") as g:
        g.write("TRN,RT,RY,I|P,Count,Var,SBR,CBR,PRN,Minus,Plus,Div,Mult,Type,Len,Logic,Line%s" % os.linesep)

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

                if False:
                    endl = "%s%s" % (r, os.linesep)
                else:
                    endl = "%s" % os.linesep

                n += 1

                if r == u"":
                    break

                if re.search(r"^#.*", r, re.M|re.I):
                    logger.debug(u"Comment - %s" % r)

                # OTran
                elif re.search(r"^OTRN.+", r, re.M|re.I):

                    otrn_count += 1

                    ot = r[7:9]
                    rt = r[10:13]
                    it = r[14:15]

                    if len(pt) == 0:
                        pt = list()
                        pt.append(ot)

                    count, td, sc = process_equation(r[5:])

                    nrt = ot

                    l = u"OTRN,%s,%s,%s,%4d,%s,,,,%s" % (ot, rt, it, count, sc, endl)
                    logger.info(u"%s" % l)
                    g.write(l)

                    count_otrn += 1

                # OREC
                elif re.search(r"^OREC.+", r, re.M|re.I):

                    rec_count += 1

                    ot = r[7:9]
                    rf = r.split(PC)[3]

                    count, td, sc = process_equation(r[5:])

                    rt = r[10:13]
                    l = u"OREC,%s,%s,%s,%4d,%s,,,,%s" % (ot, rt, rf, count, sc, endl)

                    logger.info(u"%s" % l)
                    g.write(l)

                # OGRP
                elif re.search(r"^OGRP.+", r, re.M|re.I):

                    ogrp_count += 1

                    count, td, sc = process_equation(r[5:])

                    l = u"OGRP,%s,%s,,%4d,%s,,,,%s" % (nrt, rt, count, sc, endl)

                    logger.debug(u"%s" % l)
                    g.write(l)

                # OFLD
                elif re.search(r"^OFLD.+", r, re.M|re.I):

                    field_count += 1

                    fnl = u""
                    fn = u""
                    ft = u""
                    cv = u""
                    eq = u""
                    try:
                        rl = r.split(PC)
                        fn = rl[2]
                        ft = rl[3]
                        fnl = r[5]
                        cv = rl[6]
                        eq = r.split("=")[1]

                    except Exception, msg:
                        logger.error(u"%s" % msg)
                        error_count += 1

                    count, td, sc = process_equation(r[5:])

                    l = u"OFLD,%s,%s,,%4d,%s,%s,%s,%s,%s" % (nrt, fn, count, sc, ft, fnl, r[5:], endl)

                    logger.debug(u"%s" % l)
                    g.write(l)


                # OCON
                elif re.search(r"^OCON.+", r, re.M|re.I):

                    ocon_count += 1

                    if nrt == u"":
                        nrt = u"begin"
                    else:
                        ot = r[:4]

                    rl = r.split(PC)
                    st = rl[1]

                    count, td, sc = process_equation(r[5:])

                    rt = r[:4]

                    l = u"%s,%s,,,%4d,%s,,,,%s" % (rt, nrt, count, sc, endl)

                    logger.debug(u"%s" % l)
                    g.write(l)

                # Default
                elif re.search(r"^[A-Z=]{5}.+", r, re.M|re.I):

                    if nrt == u"":
                        nrt = u"begin"

                    count, td, sc = process_equation(r[5:])

                    rt = r[:4]

                    l = u"%s,%s,,,%4d,%s,,,,%s" % (rt, nrt, count, sc, endl)

                    logger.debug(u"%s" % l)
                    g.write(l)

                else:
                    logger.debug(u"=====Skipped===== - %s" % r)

        logger.info(u"Error Count %d" % error_count)
        logger.info(u"OTRN  Count %d" % otrn_count)
        logger.info(u"REC   Count %d" % rec_count)
        logger.info(u"FLD   Count %d" % field_count)
        logger.info(u"ORGP  Count %d" % ogrp_count)

        ogrp_count

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


