#!/usr/bin/python
#
# Natural Language Processing of Information
#
import os
import sys
from os import path

from nl_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts

def getText(concepts):

    text = ""

    for k, v in concepts.getConcepts().items():
        text = text + " " + v.name

    return text

if __name__ == "__main__":
    conceptFile = "words.p"

    os.chdir("." + os.sep + "DVC_20151204_140520")

    concepts = Concepts.loadConcepts(conceptFile)

    if False:
        d = path.dirname(__file__)

        # Read the whole text.
        text = open(path.join(d, 'log.txt')).read()
    else:
        text = getText(concepts)

    tags = make_tags(get_tag_counts(text), maxsize=120)

    # Should be one of Nobile, Old Standard TT, Cantarell, Reenie Beanie, Cuprum, Molengo, Neucha, Philosopher,
    # Yanone Kaffeesatz, Cardo, Neuton, Inconsolata, Crimson Text, Josefin Sans, Droid Sans, Lobster, IM Fell DW Pica,
    # Vollkorn, Tangerine, Coustard, PT Sans Regular

    create_tag_image(tags, 'cloud_large.png', size=(900, 600)) # fontname='Arial')

    # Separate into a list of (word, frequency).
    #words = wordcloud.process_text(text)

    # Compute the position of the words.
    #elements = wordcloud.fit_words(words)

    # Draw the positioned words to a PNG file.
    #wordcloud.draw(elements, path.join(d, 'log.png'))
