# Formats example sentence cards for Anki
#
# Rather than using Anki to do all the complicated substitution, we do it
# here because it's easier to write and debug.
#
# Fields of a card are as follows:
#   unique_name: something unique to identify the card. Hanzi is fine for now
#   hanzi_simplified: simplified hanzi
#   hanzi_traditional: traditional hanzi
#   pinyin: raw pinyin straight from CCEDICT
#   definition: raw definition text straight from CCEDICT.
#
#   produce_front: front of the card for producing the hanzi, given the
#     definition and example sentences.
#   produce_back: back of the card for producing the hanzi
#   recognize_front: front of the card for recognizing the hanzi
#   recognize_back: back of the card


_CARD_TEMPLATES = {
    '1-unique_name': "{word[hanzi]}",
    '2-hanzi_simplified': "{word[hanzi]}",
    '3-pinyin': "{word[pinyin]}",

    '4-produce_front': "{sentences[4][english]} / {sentences[4][chinese]}"
}

def format_card(word, sentences):
    """Returns a list of the fields to write to the card"""

    fields = []

    for key in sorted(_CARD_TEMPLATES.keys()):
        fields.append(_CARD_TEMPLATES[key].format(word = word, sentences = sentences))

    return fields
