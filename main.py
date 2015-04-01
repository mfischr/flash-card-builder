import requests
import json
import sys
import os
from ccedict import Ccedict

# class Sentence():
#     def __init__(self, chinese, english):
#         self.chinese = chinese
#         self.english = english
#         return


def loadConfig(argv):
    # Should've passed the name of a text file in which to count words
    if (len(argv) == 2):
        with open(sys.argv[1], "r") as configFile:
            config = json.load(configFile)
            config['cedict_path'] = os.path.expanduser(config['cedict_path'])

            return config

    raise "No config specified."



def get_examples(word):
    """Downloads example sentences for a given word from Bing"""
    import urllib.parse
    from lxml import html

    base_url = "http://cn.bing.com/dict/search"
    query_string = urllib.parse.urlencode({ "q": word })

    response = requests.get(base_url + "?" + query_string)
    dom = html.fromstring(response.content)

    dom_sentences = dom.xpath('//*[@class="se_li"]')

    sentences = []

    for s in list(dom_sentences):
        english = "".join(s.xpath('.//*[@class="sen_en"]//text()'))
        chinese = "".join(s.xpath('.//*[@class="sen_cn"]//text()'))
        
        sentences.append({ "english": english, "chinese": chinese})

    return sentences



if __name__ == "__main__":

    config = loadConfig(sys.argv)

    dict = Ccedict(config['cedict_path'])

    print("Loaded cedict, {0} words".format(len(dict.words.keys())))



# with open("sentences.json", "w") as out_file:
#     json.dump(examples, out_file)
