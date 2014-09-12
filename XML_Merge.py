__author__ = 'morrj140'

import lxml.etree
merged = lxml.etree.Element('book')
for xml_file in xml_files:
    for merge_chapter in lxml.etree.parse(xml_file):
        try:
            chapter = merged.xpath('chapter[@id=%s]' % merge_chapter.get('id'))[0]
            for merge_sentence in merge_chapter:
                try:
                    sentence = chapter.xpath('sentence[@id=%s]' % merge_sentence.get('id'))[0]
                    for merge_word in merge_sentence:
                        try:
                            word = sentence.xpath('word[@id=%s]' % merge_word.get('id'))[0]
                            for data in merge_word:
                                try:
                                    word.xpath(data.tag)[0]
                                except IndexError:
                                    # add newly discovered word data
                                    word.append(data)
                        except IndexError:
                            # add newly discovered word
                            sentence.append(merge_word)
                except IndexError:
                    # add newly discovered sentence
                    chapter.append(merge_sentence)
        except IndexError:
            # add newly discovered chapter
            merged.append(merge_chapter)