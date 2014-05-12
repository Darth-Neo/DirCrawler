#
# Crawl a directory for documents and pull out the text
#
import sys
import os
import csv
import glob

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

import nltk
from nltk import tokenize, tag, chunk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

from pptx import Presentation
from docx import opendocx, getdocumenttext
import xlrd
from pyPdf import PdfFileReader

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
    
    def _getPDFText(self, filename):
        logger.debug("filename: %s" % filename)
        newparatextlist = []

        pdfDoc = PdfFileReader(file(filename, "rb"))
        
        pdfDict = pdfDoc.getDocumentInfo()
        c = Concepts(filename, "PDF")
        for x in pdfDict.keys():
            c.addConceptKeyType(x[1:], pdfDict[x])
        
        #c.logConcepts()
        
        for page in pdfDoc.pages:
            text = page.extractText()
            logger.debug("PDF : %s" % text)
            newparatextlist.append(text + ". ")

        return newparatextlist

    def _getPPTXText(self, filename):
        logger.debug("filename: %s" % filename)
        
        prs = Presentation(filename)

        cp = prs.core_properties

        c = Concepts(cp.title, "PPTX")  
        c.addConceptKeyType(cp.author, "author")
        c.addConceptKeyType(cp.category, "category")
        c.addConceptKeyType(cp.comments, "comments")
        c.addConceptKeyType(cp.content_status, "content_status")
        c.addConceptKeyType(cp.created, "created")
        c.addConceptKeyType(cp.identifier, "identifier")
        c.addConceptKeyType(cp.keywords, "keywords")
        c.addConceptKeyType(cp.language, "language")
        c.addConceptKeyType(cp.last_modified_by, "last_modified_by")
        c.addConceptKeyType(cp.last_printed, "last_printed")
        c.addConceptKeyType(cp.modified, "modified")
        c.addConceptKeyType(cp.revision, "revision")
        c.addConceptKeyType(cp.subject, "subject")
        c.addConceptKeyType(cp.title, "title")
        c.addConceptKeyType(cp.version, "version")

        #c.logConcepts()

        newparatextlist = []

        for slide in prs.slides:
            for shape in slide.shapes:
                if not shape.has_textframe:
                    continue
                for paragraph in shape.textframe.paragraphs:
                    for run in paragraph.runs:
                        logger.debug("PPTX : %s" % run.text)
                        if run.text != None:
                            newparatextlist.append(run.text + ". ")
        return newparatextlist, c

    def _getXLSText(self, filename):
        logger.debug("filename: %s" % filename)

        newparatextlist = []
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
                        logger.debug("XLXS : %s" % cell_value)
                        newparatextlist.append(cell_value + ". ")

        return newparatextlist

    def _getDOCXText(self, filename):
        logger.debug("filename: %s" % filename)

        document = opendocx(filename)
        
        # Fetch all the text out of the document we just created
        paratextlist = getdocumenttext(document)

        # Make explicit unicode version
        newparatextlist = []
        for paratext in paratextlist:
            logger.debug("DOCX : %s" % paratext)
            newparatextlist.append(paratext + ". ")
            
        return newparatextlist

    def _getConcepts(self, fname, d, w):
        listText = list()
         
        #try:
        if fname[-5:] == ".docx":
            listText = self._getDOCXText(fname)
            logger.info("++Parsing = %s" % fname) 
        elif fname[-5:] == ".pptx":
            listText, cp = self._getPPTXText(fname)
            d.addConcept(cp)
            logger.info("++Parsing = %s" % fname) 
        elif fname[-5:] == ".xlsx":
            listText = self._getXLSText(fname)
            logger.info("++Parsing = %s" % fname) 
        elif fname[-4:] == ".pdf":
            listText = self._getPDFText(fname)
            logger.info("++Parsing = %s" % fname) 

        

        for t in listText:
            if t != None:
                sentence = t.strip()
                logger.debug("Text : %s" % sentence)
                d.addConceptKeyType(sentence, "Text")
                self._addWords(w, sentence)           
    #except:
        #    e = sys.exc_info()[0]
        #    logger.error("%s" % e)
        #    logger.info("**Failed Parsing = %s" % fname)
        
        return listText

    def _addWords(self, words, sentence):
            cleanSentence = ' '.join([word for word in sentence.split() if word not in stop])

            for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(cleanSentence)):                
                logger.debug("Word: " + word + " POS: " + pos)
                c = words.addConceptKeyType(word, "WORD")
                c.addConceptKeyType(pos, "POS")

    def _checkFile(self, fname):
        logger.debug("filename: %s" % fname)
                
        d = self.documentsConcepts.addConceptKeyType(fname, "Document")
        w = self.wordsConcepts.addConceptKeyType(fname, "Document")
        
        listText = self._getConcepts(fname, d, w)

        #logger.warn("File could not be parsed : %s" % fname)

        if listText == None:
            return 0
        else:
            return 1
                
    def searchSubDir(self, subdir):
        numFilesParsed = 0
        for root, dirs, files in os.walk(subdir, topdown=False):
            for name in files:
                nameFile = os.path.join(root, name)
                numFilesParsed += self._checkFile(nameFile)

        self._saveConcepts()

        return numFilesParsed

if __name__ == '__main__':
    numFilesParsed = 0
    # Set the directory you want to start from
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture"
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture\\\AccoviaReplacement"
    #rootDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\product_types"
    #rootDir = "C:\\Users\morrj140\\Documents\\System Architecture\\OneSourceDocumentation"
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture\\AccoviaReplacement\\Product"
    #rootDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\Issues"
    rootDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\test"

    dc = DirCrawl()
    
    numFilesParsed = dc.searchSubDir(rootDir)

    logger.info("Documents Parsed = %d" % numFilesParsed)

            
