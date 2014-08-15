#!/usr/bin/python
#
# Archimate to Concepts
#
import sys
import os
import StringIO
import csv
import random
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}

XML_NS         =  "http://www.w3.org/2001/XMLSchema-instance"
ARCHIMATE_NS   =  "http://www.archimatetool.com/archimate"
NS_MAP = {"xsi": XML_NS, "archimate" : ARCHIMATE_NS}

ARCHI_TYPE = "{http://www.w3.org/2001/XMLSchema-instance}type"

Columns = ["Artifact ID", "Artifact Name", "Owner Artifact ID", "Owner Artifact Name"]
dictNode = dict()


def insertArtifactRelations(p, row, se):

    #<folder name="Relations" id="c1ff528d" type="relations">
    # <element xsi:type="archimate:AssociationRelationship" id="b0341e0e" source="ea7c85c4" target="e38ecb1d"/>

    # Generate 8 digit Hex number
    id = str(hex(random.randint(0, 16777215)))[-6:] + str(hex(random.randint(0, 16777215))[-2:])
    name = row[1]
    tag = "element"
    type = "archimate:AssociationRelationship"

    if len(row) == 4 and len(row[2].strip()) > 0:
        attrib = dict()
        attrib["id"] = id

        try:
            ArtifactID = row[0].decode(encoding='UTF-8',errors='ignore')
            attrib["source"] = dictNode[ArtifactID]

            OwnerArtifactID = row[2].decode(encoding='UTF-8',errors='ignore')
            attrib["target"] = dictNode[OwnerArtifactID]

            attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] = type

            logger.info("%s::%s" % (row[0], row[1]))

            elm = etree.Element(tag, attrib, nsmap=NS_MAP)
            se[0].insert(0, elm)

        except:
            logger.warn("Not Found : %s or %s" % (ArtifactID, OwnerArtifactID))


def insertArtifacts(p, row, se):
    #<element xsi:type="archimate:Node" id="612a9b73" name="Linux Server"/>

    # Generate 8 digit Hex number
    id = str(hex(random.randint(0, 16777215)))[-6:] + str(hex(random.randint(0, 16777215))[-2:])
    name = row[1]
    tag = "element"
    type = "archimate:Artifact"

    attrib = dict()
    attrib["id"] = id
    attrib["name"] = row[1].decode(encoding='UTF-8',errors='ignore')
    attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] = type

    logger.info("%s::%s" % (row[0], row[1]))

    elm = etree.Element(tag, attrib, nsmap=NS_MAP)
    se[0].insert(0, elm)

    #Columns = ["Artifact ID", "Artifact Name", "Owner Artifact ID", "Owner Artifact Name"]
    dictNode[row[0].decode(encoding='UTF-8',errors='ignore')] = id

    ##<property key="a" value="b"/>
    #attrib["ArtifactID"]   =

def insertIntoFolder(tree, folder, fileMetaEntity):

    file = open(fileMetaEntity, "rb")
    reader = csv.reader(file)

    xp = "folder[@name='" + folder + "']"
    se = tree.xpath(xp)
    p = se[0].getparent()

    logger.info("%s - %d" % (se, len(se)))

    rownum = 0
    for row in reader:

        if rownum == 0:
            rownum += 1
            continue
        else:
            rownum += 1

        logger.info("%d" % rownum)

        if len(row[0].strip()) == 0:
            break

        if folder == "Relations":
            insertArtifactRelations(p, row, se)
        else:
            insertArtifacts(p, row, se)

    file.close()

def outputXML(tree, filename="import_artifacts.archimate"):
    output = StringIO.StringIO()
    tree.write(output, pretty_print=True)

    logger.info("%s" % (output.getvalue()))

    f = open(filename,'w')
    f.write(output.getvalue())
    f.close()

    output.close()

if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/DNX Phase 2/DNX Phase 2 0.8.archimate"
    fileMetaEntity = "/Users/morrj140/Development/GitRepository/DirCrawler/Artifacts.csv"

    p, fname = os.path.split(fileArchimate)
    logger.info("Using : %s" % fileArchimate)

    etree.QName(ARCHIMATE_NS, 'model')

    tree = etree.parse(fileArchimate)

    insertIntoFolder(tree, "Technology", fileMetaEntity)

    insertIntoFolder(tree, "Relations", fileMetaEntity)

    outputXML(tree)