__author__ = 'Michael'

import codecs
import logging

class Ccedict():

    @staticmethod
    def splitLine(line):
        """Returns simplified character, pinyin, and definitions in a set"""
        if (line.startswith("#")):
            return None

        pinyin_start = line.find("[")
        pinyin_end = line.find("]", pinyin_start)
        def_index = line.find("/", pinyin_end)
        def_last_index = line.rfind("/")  # Remove any trailing characters

        if (pinyin_start == -1 or
            pinyin_end == -1 or
            def_index == -1 or
            def_last_index == -1):
            return None

        hanzi = line[0:pinyin_start].strip().split(" ")[-1] # Simplified is the 2nd one
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

                word = Ccedict.splitLine(line)

                if (not word is None):
                    self.words[word["hanzi"]] = word

            logging.info("Loaded cedict ({0} words)".format(len(self.words.keys())))


# Cheap unit tests
if __name__ == "__main__":

    entry = Ccedict.splitLine(u"\u4fdd\u62a4")
    if (not entry is None):
        raise "Entry should be none"


    entry = Ccedict.splitLine(u"\u4fdd\u62a4 \u4fdd\u62a5 [pei2gen1] /bacon/")
    if (entry is None):
        raise "Entry is none"

    if (entry["id"] != u"\u4fdd\u62a5[pei2gen1]"):
        raise "Entry ID is wrong"

    if (entry["definition"][0] != "bacon"):
        raise "Definition is wrong"

    entry = Ccedict.splitLine(u"\u4fdd\u62a4 [pei2gen1] /bacon/")
    if (entry is None):
        raise "Entry is none"

    if (entry["id"] != u"\u4fdd\u62a4[pei2gen1]"):
        raise "Entry ID is wrong"

    if (entry["definition"][0] != "bacon"):
        raise "Definition is wrong"
