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

    def expand_config_path(key): config[key] = os.path.expanduser(config[key])

    if (len(argv) == 2):
        real_path = os.path.expanduser(argv[1])
        with codecs.open(real_path, "r", 'utf-8') as configFile:
            config = json.load(configFile)
            expand_config_path('cedict_file') #config['cedict_file'] = os.path.expanduser(config['cedict_file'])
            expand_config_path('hsk_word_list_file')
            config['log_file'] = os.path.expanduser(config['log_file'])
            config['sentence_cache_folder'] = os.path.expanduser(config['sentence_cache_folder'])
            config['exclusion_list'] = config['exclusion_list'].split(";")
            config['extra_words_file'] = os.path.expanduser(config['extra_words_file'])
            config['anki_import_folder'] = os.path.expanduser(config['anki_import_folder'])

            logging.basicConfig(filename = config['log_file'], level = logging.DEBUG)
            logging.info("Loaded config file from %s", config['log_file'])

            return config

    raise "No config specified."


# Random function for inspecting objects
def _inspect(obj):
    attrs = vars(obj)
    # {'kids': 0, 'name': 'Dog', 'color': 'Spotted', 'age': 10, 'legs': 2, 'smell': 'Alot'}
    # now dump this in some way or another
    print(', '.join("%s: %s" % item for item in attrs.items()))



def _init_logger(config):
    import logging
    import logging.handlers

    formatter = logging.Formatter(
        fmt = "%(asctime)s: %(filename)s:%(lineno)d %(levelname)s:%(name)s: %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S")
    handlers = [
        logging.handlers.RotatingFileHandler(config['log_file'], encoding = 'utf-8',
            maxBytes = 1000000, backupCount = 1),
        logging.StreamHandler()
        #logging.FileHandler(config['log_file'], encoding = 'utf-8'),
    ]
    root_logger = logging.getLogger()
    root_logger.handlers = []   # Default root logger contains a FileHandler that writes with cp1252 codec. Screw that.

    root_logger.setLevel(logging.DEBUG)
    for h in handlers:
        h.setFormatter(formatter)
        h.setLevel(logging.DEBUG)

        root_logger.addHandler(h)

    logging.info("Started logging")


def _words_from_hsk(path_pattern, hsk_level) -> list:
    wordList = []
    logging.debug(path_pattern.format(hsk_level))
    with codecs.open(path_pattern.format(hsk_level), "r", "utf-8") as words:
        for line in list(words):
            word = line.split("\t")[0]
            wordList.append(word)

    return wordList


def _words_from_text(filename) -> list:
    """
    Loads a list of words from a text file.
    """
    wordList = []
    with codecs.open(filename, 'r', 'utf-8') as words:
        for line in list(words):
            word = line.strip()
            if len(word) > 0:
                wordList.append(word)

    return wordList

def _merge_and_remove_duplicate_words(words_hsk, words_extra) -> list:
    # During the duplicate check, make a copy to preserve the original order
    merged = words_hsk.copy()
    merged.extend(words_extra)
    merged.sort()

    for i in range(1, len(merged)):
        if (merged[i] == merged[i - 1]):
            the_word = merged[i]

            logging.warning("Duplicate word in extra word list: {0}".format(the_word))
            while the_word in words_extra: words_extra.remove(the_word)

    words_all = words_hsk.copy()
    words_all.extend(words_extra)

    return words_all




def _assemble_card_info(words, dictionary, sentence_downloader) -> list:
    card_info = []
    excluded_count = 0

    def _is_in_exclusion_list(word) -> bool:
        return word['id'] in config['exclusion_list']

    for w in words:
        if w in dictionary.words:
            word = dictionary.words[w]
            if not _is_in_exclusion_list(word):
                sentences = sentence_downloader.get_sentences(w)
                card_info.append({'word': word, 'sentences': sentences})
            else:
                excluded_count += 1

        else:
            logging.warning("Dictionary doesn't have word {0}".format(w))

    logging.info("Excluded {0} words".format(excluded_count))
    return card_info


if __name__ == "__main__":

    config = _load_config(sys.argv)
    _init_logger(config)

    dictionary = Ccedict(config['cedict_file'])

    words_extra = _words_from_text(config['extra_words_file'])
    words_hsk = _words_from_hsk(config['hsk_word_list_file'], 4)

    logging.info("Loaded extra word list ({0} words)".format(len(words_extra)))
    logging.info("Loaded HSK list ({0} words)".format(len(words_hsk)))

    # temporary so I'm not inundated with new cards
    words_hsk = words_hsk[0:360]

    words_all = _merge_and_remove_duplicate_words(words_hsk, words_extra)

    # Load the stuff
    card_info = _assemble_card_info(words_all, dictionary, SentenceDownloader(config['sentence_cache_folder']))

    cards = [cardformat.format_card(x['word'], x['sentences']) for x in card_info]

    file_name = ankiutils.write_deck_for_import(config['anki_import_folder'], "all", cards)
