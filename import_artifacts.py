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

NS_MAP={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}
XML_NS         =  NS_MAP["xsi"]
ARCHIMATE_NS   =  NS_MAP["archimate"]

ARCHI_TYPE = "{%s}type" % NS_MAP["xsi"]

ArtifactColumns = ["Artifact ID", "Artifact Name", "Owner Artifact ID", "Owner Artifact Name"]

CapabilityColumns = ["Capability Name","Capability Type","Capability Created Date","Capability Modified Date",
                     "Capability Hex ID","Capability Comment","Parent Capability Hex ID"]

FunctionColumns = ["Function Name","Function Created Date","Function Modified Date","Function Hex ID",
                   "Function Comment","Function Org Unit Name","Function Org Unit Hex ID","Function Project Hex ID"]

keyColumns = { "Artifact" : (0,2), "BusinessFunction" : (4, 6), "Function" : (3, 6), "Stakeholder" : (6, 3) }
nameColumns = { "Artifact" : (1,3), "BusinessFunction" : (0, 6), "Function" : (0, 5), "Stakeholder" : (5, 0) }

dictNode = dict()
dictRelation = dict()

def insertRelation(p, row, se, tag="element", eType="archimate:Artifact"):

    #<folder name="Relations" id="c1ff528d" type="relations">
    # <element xsi:type="archimate:AssociationRelationship" id="b0341e0e" source="ea7c85c4" target="e38ecb1d"/>

    # Generate 8 digit Hex number
    id = str(hex(random.randint(0, 16777215)))[-6:] + str(hex(random.randint(0, 16777215))[-2:])

    #name = row[1]
    in_id = eType[10:]
    colnum = nameColumns[in_id][0]

    if len(row[colnum].strip()) > 0:
        attrib = dict()
        attrib["id"] = id

        try:
            colnum = keyColumns[eType[10:]][0]
            NodeID1 = row[colnum].decode(encoding='UTF-8',errors='ignore')
            attrib["source"] = dictNode[NodeID1]

            colnum = keyColumns[eType[10:]][1]
            NodeID2 = row[colnum].decode(encoding='UTF-8',errors='ignore')
            attrib["target"] = dictNode[NodeID2]

            attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] = "archimate:AssociationRelationship"

            hash = NodeID1 + NodeID2

            if dictRelation.has_key(hash):
                return 0
            else:
                dictRelation[hash] = NodeID1 + NodeID2

            logger.debug("%s::%s" % (row[0], row[1]))

            elm = etree.Element(tag, attrib, nsmap=NS_MAP)
            se[0].insert(0, elm)

            return 1

        except:
            pass
            #logger.warn("Not Found : %s or %s" % (NodeID1, NodeID2))

    return 0


def insertNode(p, row, se, tag="element", eType="archimate:Artifact"):
    #<element xsi:type="archimate:Node" id="612a9b73" name="Linux Server"/>

    # Generate 8 digit Hex number
    id = str(hex(random.randint(0, 16777215)))[-6:] + str(hex(random.randint(0, 16777215))[-2:])

    attrib = dict()
    attrib["id"] = id
    in_id = eType[10:]
    colnum = nameColumns[in_id][0]
    attrib["name"] = row[colnum].decode(encoding='UTF-8',errors='ignore')
    attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] = eType

    colnum = keyColumns[in_id][0]

    if dictNode.has_key(row[colnum].decode(encoding='UTF-8',errors='ignore')):
        return 0
    else:
       dictNode[row[colnum].decode(encoding='UTF-8',errors='ignore')] = id

    logger.debug("%s::%s" % (row[0], row[1]))

    elm = etree.Element(tag, attrib, nsmap=NS_MAP)
    se[0].insert(0, elm)

    return 1

def insertIntoFolder(tree, folder, fileMetaEntity, eType):

    file = open(fileMetaEntity, "rb")
    reader = csv.reader(file)

    xp = "folder[@name='" + folder + "']"
    se = tree.xpath(xp)
    p = se[0].getparent()

    count = 0
    rownum = 0
    for row in reader:

        if rownum == 0:
            rownum += 1
            continue
        else:
            rownum += 1

        logger.debug("%d" % rownum)

        if len(row[0].strip()) == 0:
            break

        if folder == "Relations":
            count += insertRelation(p, row, se, eType=eType)
        else:
            count += insertNode(p, row, se, eType=eType)

    logger.info("%d inserted in %s" % (count, folder))

    file.close()

def outputXML(tree, filename="import_artifacts.archimate"):
    output = StringIO.StringIO()
    tree.write(output, pretty_print=True)

    logger.debug("%s" % (output.getvalue()))

    logger.info("Saved to : %s" % filename)

    f = open(filename,'w')
    f.write(output.getvalue())
    f.close()

    output.close()

if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Development/GitRepository/DirCrawler/CodeGen_v2.archimate"
    etree.QName(ARCHIMATE_NS, 'model')
    tree = etree.parse(fileArchimate)

    # Artifacts
    #fileMetaEntity = "/Volumes/user/Artifacts.csv"
    #p, fname = os.path.split(fileArchimate)
    #logger.info("Using : %s" % fileArchimate)
    #insertIntoFolder(tree, "Technology", fileMetaEntity, eType="archimate:Artifact")
    #insertIntoFolder(tree, "Relations", fileMetaEntity,  eType="archimate:Artifact")

    #Capability
    #fileMetaEntity = "/Users/morrj140/Development/GitRepository/DirCrawler/Mega/Capability.csv"
    #p, fname = os.path.split(fileArchimate)
    #logger.info("Using : %s" % fileArchimate)
    #insertIntoFolder(tree, "Business", fileMetaEntity, eType="archimate:BusinessFunction")
    #insertIntoFolder(tree, "Relations", fileMetaEntity, eType="archimate:BusinessFunction")

    #Functions
    fileMetaEntity = "/Users/morrj140/Development/GitRepository/DirCrawler/Mega/Function.csv"
    p, fname = os.path.split(fileArchimate)
    logger.info("Using : %s" % fileArchimate)
    insertIntoFolder(tree, "Business", fileMetaEntity, eType="archimate:BusinessFunction")

    #Function Organizations
    fileMetaEntity = "/Users/morrj140/Development/GitRepository/DirCrawler/Mega/Function.csv"
    p, fname = os.path.split(fileArchimate)
    logger.info("Using : %s" % fileArchimate)
    insertIntoFolder(tree, "Motivation", fileMetaEntity, eType="archimate:Stakeholder")
    insertIntoFolder(tree, "Relations", fileMetaEntity, eType="archimate:BusinessFunction")
    outputXML(tree)