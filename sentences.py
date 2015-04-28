# Gets example sentences from the internet
import os
import shutil
import unittest
import logging
import json
import codecs
import requests
import urllib.parse

def _ensure_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def _clear_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def _make_valid_filename(str):
    """
    From http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python
    """
    return "".join((x if x.isalnum() else "_") for x in str)


class SentenceDownloader:
    _BING_SENTENCES_BASE_URL = "http://cn.bing.com/dict/search"

    def __init__(self, sentence_cache_folder):
        self.sentence_cache_folder = sentence_cache_folder
        self.download_count = 0
        _ensure_dir(self.sentence_cache_folder)


    def _download_bing_sentences(self, word):
        """
        Downloads example sentences for the given word, getting it from the
        cache if possible.  Returns the content of the html page.
        :param word: hanzi of word to search for
        :return:
        """

        query_string = urllib.parse.urlencode({ "q": word })
        url = SentenceDownloader._BING_SENTENCES_BASE_URL + "?" + query_string

        cache_file = os.path.join(self.sentence_cache_folder, _make_valid_filename(url) + ".txt")

        if not os.path.exists(cache_file):
            logging.info("Requesting content from '%s'", url)

            response = requests.get(url)
            self.download_count += 1
            response_as_text = response.content.decode(encoding = response.encoding)

            with codecs.open(cache_file, 'w', 'utf-8') as file:
                file.write(response_as_text)

            logging.info("Saved content to '%s'", cache_file)
            return response_as_text

        else:
            logging.debug("Loading cached content from '%s'", cache_file)

            with codecs.open(cache_file, 'r', 'utf-8') as file:
                return file.read()



    def get_sentences(self, word):
        """Downloads example sentences for a given word from Bing"""
        from lxml import html

        content = self._download_bing_sentences(word)
        dom = html.fromstring(content)

        dom_sentences = dom.xpath('//*[@class="se_li"]')

        logging.debug("  get_sentences: [xx] parsing %d sentences", len(dom_sentences))

        sentences = []

        for s in list(dom_sentences):
            english = "".join(s.xpath('.//*[@class="sen_en"]//text()'))
            chinese = "".join(s.xpath('.//*[@class="sen_cn"]//text()'))

            sentences.append({ "english": english, "chinese": chinese})

        return sentences



class UnitTests(unittest.TestCase):
    _TEMP_SENTENCE_CACHE_FOLDER = os.path.expandvars("$Temp\\sentences_py_unittest_cache")

    def setUp(self):
        _clear_dir(UnitTests._TEMP_SENTENCE_CACHE_FOLDER)

    def tearDown(self):
        pass

    def test_clean_download(self):
        """Should download sentences for a given word, and use cache"""
        me = SentenceDownloader(UnitTests._TEMP_SENTENCE_CACHE_FOLDER)

        test_word = u"\u4fdd\u62a4"
        sentences = me.get_sentences(test_word) # bao3hu4, protect

        self.assertEqual(len(sentences), 10, "sentence count")
        self.assertTrue(sentences[0]['chinese'].find(test_word) >= 0, "downloaded sentence contains word")

        sentences2 = me.get_sentences(test_word) # same thing
        self.assertEqual(1, me.download_count, "download count")
        self.assertEqual(json.dumps(sentences), json.dumps(sentences2), "sentences downloaded should be identical")


