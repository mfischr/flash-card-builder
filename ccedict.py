__author__ = 'Michael'

import codecs
import logging

class Ccedict():

    def splitLine(self, line):
        """Returns simplified character, pinyin, and definitions in a set"""
        if (line.startswith("#")):
            return None

        trad_end = line.find(" ")
        pinyin_start = line.find("[")
        pinyin_end = line.find("]", pinyin_start)
        def_index = line.find("/", pinyin_end)
        def_last_index = line.rfind("/")  # Remove any trailing characters

        hanzi = line[trad_end:pinyin_start].strip()
        pinyin = line[pinyin_start + 1:pinyin_end]

        return {
                'id': "{0}[{1}]".format(hanzi, pinyin),
                'hanzi': hanzi,
                'pinyin': pinyin,
                'definition': line[def_index:def_last_index + 1][1:-1].split("/")
               }


    def __init__(self, file_name):
        """Constructs a Ccedict object from the given dictionary file."""
        self.words = {}
        with codecs.open(file_name, "r", "utf-8") as dict:
            for line in list(dict):

                word = self.splitLine(line)

                if (not word is None):
                    self.words[word["hanzi"]] = word

            logging.info("Loaded cedict ({0} words)".format(len(self.words.keys())))

