#
# Crawl a directory for documents and pull out the text
#
import os
import sys
from docx import Document

import unicodedata
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph

from nl_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


def docxText(df, of):

    with open(of, "w") as f:
        document = Document(df)

        lp = list()

        nt = 0

        parent_elm = document.element.body

        for child in parent_elm.iterchildren():

            if isinstance(child, CT_P):
                p = Paragraph(child, document)
                pt = unicodedata.normalize(u'NFKD', p.text).encode(u'ascii', u'ignore')

                if len(pt) > 0:
                    ps = p.style.name
                    logger.debug(u"%s" % ps)
                    psr = ps[:7]
                    if psr == u"Heading":
                        po = (u"%s[%s]" % (p.style.name, p.text)).strip()
                        logger.debug(u"%s" % po)
                        fpo = po.encode(u'ascii', u'ignore') + os.linesep
                        f.write(fpo)
                    else:
                        # po = "R%s[%s]" % (p.style.name, p.text)
                        # logger.info(po)
                        # fpo = po.encode(u'ascii', u'ignore') + os.linesep
                        # f.write(fpo)
                        pass

            elif isinstance(child, CT_Tbl):

                table = Table(child, document)
                nt += 1
                nc = table._column_count

                nr = 0
                for row in table.rows:
                    nr += 1

                    rs = u""
                    try:
                        cl = list()

                        for n in range(0, nc):
                            try:

                                txt = u"%s" % row.cells[n].paragraphs[0].text
                                rs += txt + u","

                                logger.debug(u"%d => %s" % (n, txt))

                            except Exception, msg:
                                logger.debug(u"Opps %s" % msg)

                        if len(rs) > 0:
                            rs = unicodedata.normalize(u'NFKD', rs).encode(u'ascii', u'ignore')
                            f.write(rs + os.linesep)

                    except Exception, msg:
                        logger.error(u"%s" % msg)

                    logger.debug(u"    row = %d" % nr)

                logger.info(u"table = %d" % nt)

                f.write(os.linesep)
                # f.write("New Table%s" % os.linesep)
                # f.write(os.linesep)


if __name__ == u'__main__':
    # Set the directory you want to start from
    df = os.getcwd() + os.sep + u"designoverview.docx"
    of = u"tables3.csv"
    docxText(df, of)
