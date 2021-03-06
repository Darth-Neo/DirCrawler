#!/usr/bin/env python
import re

from nl_lib import Logger
logger = Logger.setupLogging(__name__)
logger.setLevel(Logger.INFO)


def addList(s, vb, t):
    tl = list()
    tl.append(s)
    tl.append(len(vb))
    t.append(tl)

    return tl


def process_equation(s):

    logger.debug(u"Input %s" % s)

    count = 0
    t = list()

    vb = re.findall(r"[$A-Za-z_]+", s)
    st = "Vars"
    addList(st, vb, t)

    vb = re.findall(r"\[[$A-Za-z_:-]+\]", s)
    st = "["
    addList(st, vb, t)

    vb = re.findall(r"\{[A-Za-z_]+\}", s)
    st = "{"
    addList(st, vb, t)

    vb = re.findall(r"\([A-Za-z_]+\)", s)
    operation = len(vb)
    st = "("
    addList(st, vb, t)

    vb = re.findall(r".+[-].+", s)
    operation += len(vb)
    st = "-"
    addList(st, vb, t)

    vb = re.findall(r".+[+]+.+", s)
    operation += len(vb)
    st = "+"
    addList(st, vb, t)

    vb = re.findall(r".+[/]+.+", s)
    operation += len(vb)
    st = "/"
    addList(st, vb, t)

    vb = re.findall(r".+[*]+.+", s)
    operation += len(vb)
    st = "*"
    addList(st, vb, t)

    terms = u"%s," % "Op"
    sc = u"%d," % operation

    for x in t:
        terms += "%s," % x[0]
        sc += "%s," % x[1]
        count += x[1]

    terms = terms[:-1]
    sc = sc[:-1]

    return count, t, sc, terms


def test_process_equation():
    s = "[--:NEW]+[AMOUNT] < 0 || [AUTH_CODE] == 'CREDIT' + {JS} || [AUTH_CODE] == ' CREDIT' * (js)|| [AUTH_CODE] == '  CREDIT' - [js] || [AUTH_CODE] == 'REDIT' \ [js]"

    count, t, sc, terms = process_equation(s)

    assert(t[0][1] == 14)

    assert(t[1][1] == 8)

    assert(t[2][1] == 1)

    assert(t[3][1] == 1)

    assert(t[4][1] == 1)

    assert(t[5][1] == 1)

    assert(t[6][1] == 0)

    assert(t[7][1] == 1)

    logger.info(u"Count : %d" % count)

if __name__ == u"__main__":
    test_process_equation()