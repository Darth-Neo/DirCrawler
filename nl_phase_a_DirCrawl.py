# Import the os module, for the os.walk function
import sys
import os
import csv
import glob

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib import Constants
from nl_lib import Concepts 

from pptx import Presentation
from docx import opendocx, getdocumenttext
import xlrd
from pyPdf import PdfFileReader

documentsConcepts = Concepts.Concepts("DocumentConcepts", "Documents")

def getPDFText(filename):
    logger.info("filename: %s" % filename)
    newparatextlist = []

    input = PdfFileReader(file(filename, "rb"))
    for page in input.pages:
        text = page.extractText()
        logger.debug("PDF : %s" % text)
        newparatextlist.append(text + ". ")

    return newparatextlist

def getPPTXText(filename):
    logger.info("filename: %s" % filename)
    
    prs = Presentation(filename)

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

    return newparatextlist

def getXLSText(filename):
    logger.info("filename: %s" % filename)

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
            # print 'Row:', curr_row
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

def getDOCXText(filename):
    logger.info("filename: %s" % filename)

    document = opendocx(filename)
    
    # Fetch all the text out of the document we just created
    paratextlist = getdocumenttext(document)

    # Make explicit unicode version
    newparatextlist = []
    for paratext in paratextlist:
        logger.debug("DOCX : %s" % paratext)
        newparatextlist.append(paratext + ". ")
        
    return newparatextlist

def getConcepts(fname, d):
    listText = list()

    if fname[-5:] == ".docx":
        listText = getDOCXText(fname)
    elif fname[-5:] == ".pptx":
        listText = getPPTXText(fname)
    elif fname[-5:] == ".xlsx":
        listText = getXLSText(fname)
    elif fname[-4:] == ".pdf":
        listText = getPDFText(fname)
   
    for t in listText:
        if t != None:
            sentence = t.strip()
            logger.debug("Text : %s" % sentence)
            d.addConceptKeyType(sentence, "Text")
        
    return listText

def checkFile(fname):
    logger.debug("filename: %s" % fname)
            
    d = documentsConcepts.addConceptKeyType(fname, "Document")
    getConcepts(fname, d)

    #logger.warn("File could not be parsed : %s" % fname)
            
def searchSubDir(subdir):
    for root, dirs, files in os.walk(subdir, topdown=False):
        for name in files:
            nameFile = os.path.join(root, name)
            checkFile(nameFile)
  
if __name__ == '__main__':  
    # Set the directory you want to start from
    #rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture"
    rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture\\Accovia"
    #rootDir = "C:\\Users\morrj140\\Documents\\System Architecture\\OneSourceDocumentation"
    
    searchSubDir(rootDir)

    Concepts.Concepts.saveConcepts(documentsConcepts, "documents.p")
            
