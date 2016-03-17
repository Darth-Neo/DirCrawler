#!/usr/bin/env python
import re

from nl_lib import Logger
logger = Logger.setupLogging(__name__)
logger.setLevel(Logger.DEBUG)


def process_equation(s):

    logger.debug(u"Input %s" % s)
    count = 0
    td = dict()

    vb0 = re.findall(r"[A-Za-z_]+", s)
    td["Vars"] = len(vb0)

    vb1 = re.findall(r"\[[A-Za-z_]+\]", s)
    td["["] = len(vb1)

    vb2 = re.findall(r"\{[A-Za-z_]+\}", s)
    td["{"] = len(vb2)

    vb3 = re.findall(r"\([A-Za-z_]+\)", s)
    td["("] = len(vb3)

    vb4 = re.findall(r".+[-]+.+", s)
    td["minus"] = len(vb3)

    vb5 = re.findall(r".+[+]+.+", s)
    td["plus"] = len(vb3)

    vb6 = re.findall(r".+[/]+.+", s)
    td["div"] = len(vb3)

    vb7 = re.findall(r".+[*]+.+", s)
    td["mult"] = len(vb3)

    sc = u""
    for k, v in td.items():
        logger.debug(u"'%s' ['%s']" % (k, v))
        count += v
        sc += u"'%s', %d, " % (k, v)

    return count, td, sc


def test_process_equation():
    s = "[AMOUNT] < 0 || [AUTH_CODE] == 'CREDIT' + {JS} || [AUTH_CODE] == ' CREDIT' * (js)|| [AUTH_CODE] == '  CREDIT' - [js] || [AUTH_CODE] == 'REDIT' \ [js]"

    count, td, sc = process_equation(s)

    assert(td["Vars"] == 13)

    assert(td["["] == 7)

    assert(td["{"] == 1)

    assert(td["("] == 1)

    assert(td["minus"] == 1)

    assert(td["plus"] == 1)

    assert(td["div"] == 1)

    assert(td["mult"] == 1)

    logger.debug(u"Count : %d" % count)

if __name__ == u"__main__":
    test_process_equation()