import requests
import json

class Sentence():
    def __init__(self, chinese, english):
        self.chinese = chinese
        self.english = english
        return


def get_examples(word):
    """Downloads example sentences for a given word from Bing"""
    import urllib.parse
    from lxml import html

    base_url = "http://cn.bing.com/dict/search"
    query_string = urllib.parse.urlencode({ "q": word })

    response = requests.get(base_url + "?" + word)
    dom = html.fromstring(response.content)

    dom_sentences = dom.xpath('//*[@class="se_li"]')

    sentences = []

    for s in list(dom_sentences):
        english = "".join(s.xpath('.//*[@class="sen_en"]//text()'))
        chinese = "".join(s.xpath('.//*[@class="sen_cn"]//text()'))
        
        sentences.append({ "english": english, "chinese": chinese})

    return sentences



examples = get_examples("%E5%8F%96%E6%B6%88")
print("Retrieved {0} examples".format(len(examples)))

 
with open("sentences.json", "w") as out_file:
    json.dump(examples, out_file)
