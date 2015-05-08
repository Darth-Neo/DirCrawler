__author__ = 'morrj140'

from nl_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

try:
    import textract
except:
    pass

if 'textract' in dir():


    TEXTRACT = True
    logger.info("Using textract parser")

    logger.info ("PDF ...")
    text = textract.process('./Examples/example.pdf')
    logger.info(text[0:20])

    logger.info ("PPTX ...")
    text = textract.process('./Examples/example.pptx')
    logger.info(text[0:20])

    logger.info ("XLSX ...")
    text = textract.process('./Examples/example.xlsx')
    logger.info(text[0:20])

    logger.info ("DOCX ...")
    text = textract.process('./Examples/example.docx')
    logger.info(text[0:20])

    logger.info ("txt ...")
    text = textract.process('./Examples/example.txt')
    logger.info(text[0:20])

    if False:
        logger.info ("jpg ...")
        text = textract.process('./Examples/example.jpg')
        logger.info(text[0:20])

        logger.info ("png ...")
        text = textract.process('./Examples/example.png')
        logger.info(text[0:20])