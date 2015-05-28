import sys
import os
import codecs
import logging
import json
import ankiutils
from ccedict import Ccedict
from sentences import SentenceDownloader
import cardformat


def _load_config(argv):
    """
    # Should've passed the name of a text file in which to count words
    :rtype : (dict) config dictionary
    """
    if (len(argv) == 2):
        real_path = os.path.expanduser(argv[1])
        with codecs.open(real_path, "r", 'utf-8') as configFile:
            config = json.load(configFile)
            config['cedict_file'] = os.path.expanduser(config['cedict_file'])
            config['log_file'] = os.path.expanduser(config['log_file'])
            config['sentence_cache_folder'] = os.path.expanduser(config['sentence_cache_folder'])

            logging.basicConfig(filename = config['log_file'], level = logging.DEBUG)
            logging.info("Loaded config file from %s", config['log_file'])

            return config

    raise "No config specified."


def _init_logger(config):
    import logging
    import logging.handlers
    formatter = logging.Formatter(
        fmt = u"%(asctime)s; %(filename)s:%(lineno)d %(levelname)s:%(name)s: %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S")
    handlers = [
        logging.handlers.RotatingFileHandler(config['log_file'], encoding = 'utf-8',
            maxBytes = 100000, backupCount = 1),
        logging.StreamHandler()
    ]
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    for h in handlers:
        h.setFormatter(formatter)
        h.setLevel(logging.DEBUG)

        root_logger.addHandler(h)

    logging.info("Started logging")





if __name__ == "__main__":

    config = _load_config(sys.argv)
    _init_logger(config)

    dict = Ccedict(config['cedict_file'])

    # Create a fake card
    words = config['temp_word_list'].split(";")
    sent = SentenceDownloader(config['sentence_cache_folder'])

    cards = []

    for w in words:
        sentences = sent.get_sentences(w)
        word = dict.words[w]
        cards.append(cardformat.format_card(word, sentences))

    file_name = ankiutils.write_deck_for_import("test", cards)

    logging.info("Wrote cards to '{0}'".format(file_name))
