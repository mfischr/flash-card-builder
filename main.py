import sys
import os
import logging
import json
import ankiutils
from ccedict import Ccedict
from sentences import SentenceDownloader

# class Sentence():
#     def __init__(self, chinese, english):
#         self.chinese = chinese
#         self.english = english
#         return


def _load_config(argv):
    """
    # Should've passed the name of a text file in which to count words
    :rtype : (dict) config dictionary
    """
    if (len(argv) == 2):
        real_path = os.path.expanduser(argv[1])
        with open(real_path, "r") as configFile:
            config = json.load(configFile)
            logging.basicConfig(filename = config['log_file'], level = logging.DEBUG)
            logging.info("Loaded config file from %s", config['log_file'])

            config['cedict_path'] = os.path.expanduser(config['cedict_path'])

            return config

    raise "No config specified."







if __name__ == "__main__":

    config = _load_config(sys.argv)

    dict = Ccedict(config['cedict_path'])

    print("Loaded cedict, {0} words".format(len(dict.words.keys())))

    # Create a fake card
    words = config['temp_word_list'].split(";")

    

    # for word in words:
    #     entry = dict.words[word]
    #     cards.append({'id': word, 'front': })
    #
    # file_name = ankiutils.write_deck_for_import("test", cards)
    #
    # print("Wrote cards to {0}".format(file_name))
