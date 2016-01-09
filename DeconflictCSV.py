#
# deconflict csv as each row is a file
#
import os
import sys

from nl_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


def deconflict(csvFile):

    n = 0

    if not os.path.exists(csvFile):
        logger.error(u"%s : Does Not Exist!" % csvFile)
        return

    logger.info(u"%s" % os.getcwd())

    with open(csvFile, "r") as g:
        inputLines = g.readlines()

    input = "%s" % inputLines[0]

    for x in input.split("\r"):

        n += 1

        if n == 1:
            header = x
            continue

        try:
            y = x.split(u",")

            txtFile = u"%d_%s.txt" % (n, y[0])

            with open(txtFile, "w") as f:
                output = "%s. %s" % (y[2], y[1])
                f.write(output)
        except Exception, msg:
            logger.debug(u"%d: %s" % (n, msg))

if __name__ == u"__main__":
    os.chdir(u"dvc")

    csvFile = u"DVC.csv"

    deconflict(csvFile)