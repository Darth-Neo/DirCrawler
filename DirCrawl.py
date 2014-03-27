# Import the os module, for the os.walk function
import os
import sys

from docx import opendocx, getdocumenttext
import os
import csv
import Queue
import threading
import time

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib import Constants
from nl_lib import Concepts 
from nl_lib import PeopleText
from nl_lib import Tokens

from nltk.corpus import stopwords
from nltk import tokenize

def getText(filename):
    document = opendocx(filename)
    
    # Fetch all the text out of the document we just created
    paratextlist = getdocumenttext(document)

    # Make explicit unicode version
    newparatextlist = []
    for paratext in paratextlist:
        newparatextlist.append(paratext.encode("utf-8"))
        
    return newparatextlist

def getConcepts(fname, d):
    logger.info('\t%s' % fname)

    listText = getText(fname)
    
    for t in listText:
        d.addConceptKeyType(t.strip(), "Text")

    return listText

if __name__ == '__main__':
    documentsConcepts = Concepts.Concepts("DocumentConcepts", "Documents")
    
    # Set the directory you want to start from
    rootDir = '.'
    for dirName, subdirList, fileList in os.walk(rootDir):
        logger.info('Found directory: %s' % dirName)
        for fname in fileList:
            if fname[-5:] == ".docx":
                d = documentsConcepts.addConceptKeyType(fname, "Document")
                getConcepts(fname, d)

    Concepts.Concepts.saveConcepts(documentsConcepts, "documents.p")
            
