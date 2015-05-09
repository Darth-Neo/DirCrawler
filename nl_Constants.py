#!/usr/bin/env python
#
# Constants
#
__VERSION__ = 0.1
__author__ = u'morrj140'

import os

# Common Filenames
homeDir = os.getcwd() + os.sep

documentsFile  = homeDir + u"documents.p"
projectsFile   = homeDir + u"projectsDict.p"
peopleFile     = homeDir + u"peopleDict.p"
wordsFile      = homeDir + u"wordsDict.p"
topicsFile     = homeDir + u"topicsDict.p"
sentencesFile  = homeDir + u"sentencesDict.p"
similarityFile = homeDir + u"similarityDict.p"

imageFile      = homeDir + u"Topics_Cloud.bmp"

gmlFile        = homeDir + u"Concepts.gml"

logFile        = homeDir + u"nl_phase_log.txt"
