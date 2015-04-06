__author__ = 'Michael'

import codecs

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

        return {
                "hanzi": line[trad_end:pinyin_start].strip(),
                "pinyin": line[pinyin_start:pinyin_end + 1],
                "definition": line[def_index:def_last_index + 1]
               }


    def __init__(self, file_name):
        """Constructs a Ccedict object from the given dictionary file."""
        self.words = {}
        with codecs.open(file_name, "r", "utf-8") as dict:
            for line in list(dict):

                word = self.splitLine(line)

                if (not word is None):
                    self.words[word["hanzi"]] = word

