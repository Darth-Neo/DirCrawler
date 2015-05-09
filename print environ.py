#!/usr/bin/env python

import os
import sys

variable = sys.argv


def enVar(variable):
    """
    This function returns all the environment variable set on the machine or in active project.
    if environment variable name is passed to the enVar function it returns its values.
    """
    nVar = len(sys.argv)-1
    if len(variable) == 1: # if user entered no environment variable name
        for index, each in enumerate(sorted(os.environ.iteritems())):
            print index, each
    else: # if user entered one or more than one environment variable name
        for x in range(nVar):
            x+=1
            if os.environ.get(variable[x].upper()): # convertes to upper if user mistakenly enters lowecase
                print u"%s : %s" %  (variable[x].upper(), os.environ.get(variable[x].upper()))
            else:
                print u'Make sure the Environment variable "%s" exists or spelled correctly.' % variable[x]

enVar(variable)

if False:
    print os.environ[u'USERNAME']
    print os.environ[u'USERDOMAIN']
    print os.environ[u'USERDNSDOMAIN']
