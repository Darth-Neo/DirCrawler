#
# Crawl a directory for documents and pull out the text
#
from nl_lib import Logger

logger = Logger.setupLogging(__name__)
logger.setLevel(Logger.INFO)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

import nltk
import openxmllib
from pptx import Presentation
from Examples.docx import opendocx, getdocumenttext
import xlrd
from pyPdf import PdfFileReader

from traceback import format_exc

from BeautifulSoup import BeautifulSoup

# by importing the textract module, you will then enable its use
#import textract

if 'textract' in dir():
    TEXTRACT = True
    logger.info("Using textract parser")
else:
    TEXTRACT = False
    logger.info("Using custom parser")

stop.append("information")
stop.append("member")

import unicodedata

class DirCrawl(object):
    documentsConceptsFile = "documents.p"
    documentsConcepts = None

    wordsConceptsFile = "words.p"
    wordsConcepts = None
    
    def __init__(self):
        self.documentsConcepts = Concepts("DocumentConcepts", "Documents")
        self.wordsConcepts = Concepts("WordConcepts", "Words")

    def getDocumentsConcepts(self):
        return self.documentsConcepts

    def getWordsConcepts(self):
        return self.wordsConcepts

    def _saveConcepts(self):
        Concepts.saveConcepts(self.documentsConcepts, self.documentsConceptsFile)
        Concepts.saveConcepts(self.wordsConcepts, self.wordsConceptsFile)

    def _getOpenXmlText(self, filename, c):
        logger.debug("OpenXmlText: %s" % filename)

        try:

            doc = openxmllib.openXmlDocument(path=filename)

            logger.debug ("%s\n" % (doc.allProperties))

            ap = c.addConceptKeyType("allProperties","PROPERTIES")
            for x in doc.allProperties:
                logger.debug("cp %s:%s" % (x, doc.allProperties[x]))
                ap.addConceptKeyType(doc.allProperties[x], x)
        except:
            pass

    def _getPDFText(self, filename, d):
        logger.debug("filename: %s" % filename)
        newparatextlist = list()

        try:
            pdfDoc = PdfFileReader(file(filename, "rb"))

            pdfDict = pdfDoc.getDocumentInfo()

            for x in pdfDict.keys():
                d.addConceptKeyType(x[1:], pdfDict[x])

            #c.logConcepts()

            for page in pdfDoc.pages:
                text = page.extractText()
                if not isinstance(text, str):
                    unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')

                logger.debug("PDF : %s" % text)

                newparatextlist.append(text + ". ")

            return newparatextlist

        except:
            pass

    def _getPPTXText(self, filename):
        logger.debug("filename: %s" % filename)

        newparatextlist = list()

        try:

            prs = Presentation(filename)

            for slide in prs.slides:
                for shape in slide.shapes:
                    if not shape.has_text_frame:
                        continue
                    for paragraph in shape.text_frame.paragraphs:
                        for run in paragraph.runs:
                            logger.debug("PPTX : %s" % run.text)
                            if run.text != None:
                                if not isinstance(run.text, str):
                                    unicodedata.normalize('NFKD', run.text).encode('ascii', 'ignore')
                                newparatextlist.append(run.text + ". ")
        except:
            pass

        return newparatextlist

    def _getXLSText(self, filename):
        logger.debug("filename: %s" % filename)

        newparatextlist = list()

        try:


            workbook = xlrd.open_workbook(filename)

            #sheet = "Specific Requirements"
            #worksheet = workbook.sheet_by_name(sheet)

            CellTypes = ["Empty", "Text", "Number", "Date", "Boolean", "Error", "Blank"]

            for worksheet_name in workbook.sheet_names():
                worksheet = workbook.sheet_by_name(worksheet_name)
                num_rows = worksheet.nrows - 1
                num_cells = worksheet.ncols - 1
                curr_row = -1

                while curr_row < num_rows:
                    curr_row += 1
                    row = worksheet.row(curr_row)
                    logger.debug('Row: %s' % curr_row)
                    curr_cell = -1
                    while curr_cell < num_cells:
                        curr_cell += 1
                        # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                        cell_type = worksheet.cell_type(curr_row, curr_cell)
                        cell_value = worksheet.cell_value(curr_row, curr_cell)
                        if cell_type == 1:
                            if not isinstance(cell_value, str):
                                unicodedata.normalize('NFKD', cell_value).encode('ascii', 'ignore')
                            logger.debug("XLXS : %s" % cell_value)
                            newparatextlist.append(cell_value + ". ")
        except:
            pass

        return newparatextlist

    def _getDOCXText(self, filename):
        logger.debug("filename: %s" % filename)

        document = opendocx(filename)
        # Fetch all the text out of the document we just created

        paratextlist = getdocumenttext(document)

        # Make explicit unicode version
        newparatextlist = []
        for paratext in paratextlist:
            if not isinstance(paratext, str):
                unicodedata.normalize('NFKD', paratext).encode('ascii', 'ignore')
            logger.debug("DOCX : %s" % paratext)
            newparatextlist.append(paratext + ". ")
            
        return newparatextlist

    def _getTXT(self, filename):
        logger.debug("filename: %s" % filename)

        listText = list()

        soup = BeautifulSoup(open(filename))

        logger.debug("Soup: %s" % soup)

        st = soup.text

        for line in st.split(os.linesep):
            logger.debug("TXT : %s" % line)
            listText.append(line)

        return listText

    def _getConcepts(self, fname, d, w):
        listText = list()

        if TEXTRACT == True:
            text = textract.process(fname)
            if text != None or len(text) != 0:
                listText = text
        else:
            if fname[-5:] == ".docx":
                listText = self._getDOCXText(fname)
                self._getOpenXmlText(fname, d)
                logger.info("++Parsing = %s" % fname)
            elif fname[-5:] == ".pptx":
                listText = self._getPPTXText(fname)
                self._getOpenXmlText(fname, d)
                logger.info("++Parsing = %s" % fname)
            elif fname[-5:] == ".xlsx":
                listText = self._getXLSText(fname)
                self._getOpenXmlText(fname, d)
                logger.info("++Parsing = %s" % fname) 
            elif fname[-4:] == ".pdf":
                listText = self._getPDFText(fname, d)
                logger.info("++Parsing = %s" % fname)
            elif fname[-4:] in (".txt", ".xml", ".htm", ".csv"):
                listText = self._getTXT(fname)
                logger.info("++Parsing = %s" % fname)
            elif fname[-5:] in (".html", ".WSDL"):
                listText = self._getTXT(fname)
                logger.info("++Parsing = %s" % fname)
            elif fname[-4:] in (".xml"):
                listText = self._getTXT(fname)
                logger.info("++Parsing = %s" % fname)
            else:
                em = format_exc().split('\n')[-2]
                logger.warn("Warning: %s" % (em))

        if listText != None:
            for t in listText:
                if t != None:
                    try:
                        sentence = t.encode('ascii', errors="ignore").strip()
                        logger.debug("%s:Text : %s" % (type(sentence), sentence))
                        d.addConceptKeyType(sentence, "Text")
                        self._addWords(w, sentence)
                    except:
                        pass

        return listText

    def checkWordCaps(self, w):
        s = str()

    def _addWords(self, words, sentence):
            cleanSentence = ' '.join([word for word in sentence.split() if word not in stop])

            logger.debug("cs:%s" % cleanSentence)

            for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(cleanSentence)):


                logger.debug("Word: " + word + " POS: " + pos)
                c = words.addConceptKeyType(word, "WORD")
                c.addConceptKeyType(pos, "POS")

    def _checkFile(self, fname):
        logger.debug("filename: %s" % fname)

        d = Concepts(fname, "Document")
        w = Concepts(fname, "Document")

        listText = self._getConcepts(fname, d, w)

        if listText != None and len(listText) == 0:
            logger.warn("%s has no text" % (fname))
            return 0
        else:
            self.documentsConcepts.addConcept(d)
            self.wordsConcepts.addConcept(w)

            return 1
                
    def searchSubDir(self, subdir):
        numFilesParsed = 0
        for root, dirs, files in os.walk(subdir, topdown=True):
            for name in files:
                nameFile = os.path.join(root, name)
                numFilesParsed += self._checkFile(nameFile)

        self._saveConcepts()

        return numFilesParsed

if __name__ == '__main__':
    numFilesParsed = 0

    # Set the directory you want to start from
    rootDir = "/Users/morrj140/Documents/SolutionEngineering/DVC/pmo"

    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture"
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture\\\AccoviaReplacement"
    #rootDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\product_types"
    #rootDir = "C:\\Users\morrj140\\Documents\\System Architecture\\OneSourceDocumentation"
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture\\AccoviaReplacement\\Product"
    #rootDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\Issues"
    #rootDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\test"
    #rootDir = "/Users/morrj140/Development/GitRepository/DirCrawler/Examples"
    #rootDir = "/Users/morrj140/Documents/SolutionEngineering/CodeGen/NLP"
    #rootDir = "/Users/morrj140/Documents/SolutionEngineering/Services/export"

    dc = DirCrawl()
    
    numFilesParsed = dc.searchSubDir(rootDir)

    logger.info("Documents Parsed = %d" % numFilesParsed)

            
