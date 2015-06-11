import pinyinutils

# Formats example sentence cards for Anki
#
# Try to do as little formatting here as possible, since the editor
# in Anki is actually really good.  Here we only do all the reformatting
# and editing that is a pain to do in JS.

_TONE_COLOR_FORMAT = {
    '1': "<span class=\"tone1\">{0}</span>",
    '2': "<span class=\"tone2\">{0}</span>",
    '3': "<span class=\"tone3\">{0}</span>",
    '4': "<span class=\"tone4\">{0}</span>",
    '5': "<span class=\"tone5\">{0}</span>",
}

def format_card(word, sentences):
    """Returns a list of the fields to write to the card"""
    import json
    import re

    fields = []

    # 1. Unique Name (hanzi plus pinyin)
    fields.append(word['id'])

    # 2. Hanzi
    fields.append(word['hanzi'])

    # 3. Hanzi colorized based on tone color
    fields.append(_tone_color(word['hanzi'], word['pinyin'], _TONE_COLOR_FORMAT))

    # 4. Pinyin, accented
    fields.append(pinyinutils.multiple_text_from_pinyin(word['pinyin']))

    # 5. Definitions as JSON
    # Filter out the definitions that start with "CL: "
    nonClDefs = ((x if not re.search("^CL:", x) else None) for x in word['definition'])
    fields.append(json.dumps(list(nonClDefs)))

    # 6. Sentences as json, with the words clozed out
    # TODO: figure out how to properly clone this object
    sentences_clozed = json.loads(json.dumps(sentences))

    for sentence in sentences_clozed:
        cloze_text = "<span class=\"cloze-hidden\">" + ("##" * len(word['hanzi'])) + "</span><span class=\"cloze-visible\">" + word['hanzi'] + "</span>"
        sentence['chinese'] = sentence['chinese'].replace(word['hanzi'], cloze_text)

    fields.append(json.dumps(sentences_clozed))

    return fields

# Just takes the last characters from each pinyin syllable
def _extract_tones_from_pinyin(pinyin):
    pinyin_list = pinyin.split(" ")
    return list(x[-1:] for x in pinyin_list)

def _tone_color(hanzi, pinyin, tone_to_format_dict):
    tones = _extract_tones_from_pinyin(pinyin)

    output = ""
    for i in range(len(hanzi)):
        output += tone_to_format_dict[tones[i]].format(hanzi[i])

    return output
