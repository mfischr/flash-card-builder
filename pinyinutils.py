__author__ = 'Michael'
import re
import unittest

def _get_tone_character(ch, tone):
    """For ch = 'o' and tone = 3, returns 'ǒ'."""
    toneSymbols = "aāáǎàaeēéěèeiīíǐìioōóǒòouūúǔùuüǖǘǚǜü"  #ě (also works for a lot of em)
    toneCharacter = None

    chIndex = toneSymbols.find(ch)
    if chIndex == -1:
        raise "Couldn't find tone character for {0}!".format(ch)

    return toneSymbols[chIndex + tone]


def _replace_character_with_tone(rawPinyin, chars, tone):
    for i in range(0, len(rawPinyin)):
        ch = rawPinyin[i]
        if chars.find(ch) != -1:
            return rawPinyin.replace(ch, _get_tone_character(ch, tone))


def multiple_text_from_pinyin(text):
    """Given "dang1ran2", returns the pinyin with the accents.  This is a little hacky; it'll get confused
    if you give it "xian1shengzai4"
    """
    workingText = text
    completedWords = ""

    while True:
        matches = re.search("^([^\d^ ]+)(\d)?(\s)*", workingText)
        if (matches is None):
            break

        pinyinGroup = matches.group(1)

        if matches.group(2):
            pinyinGroup += matches.group(2)

        completedWords += _text_from_pinyin(pinyinGroup) + (matches.group(3) or "")

        workingText = workingText[len(matches.group(0)):]

    return completedWords


def _text_from_pinyin(numberPinyin):
    """Given "you3", returns "you", and so forth."""

    m = re.search("^([a-z:]{1,6})(\d)?$", numberPinyin.strip())
    if not m:
        # Maybe this is already accented pinyin?
        return numberPinyin
    else:
        if m.group(2):
            tone = int(m.group(2))
        else:
            tone = 5

        rawPinyin = m.group(1)
        rawPinyin = rawPinyin.replace("v", "ü")   # v->ü: Common shorthand
        rawPinyin = rawPinyin.replace("u:", "ü")   # u:->ü: CCEDICT style

        if rawPinyin.find("iu") > 0:
            pinyin = rawPinyin.replace("u", _get_tone_character("u", tone))
        elif rawPinyin.find("ui") > 0:
            pinyin = rawPinyin.replace("i", _get_tone_character("i", tone))
        else:
            # Priority vowels
            pinyin = _replace_character_with_tone(rawPinyin, "aeoü", tone)

            if pinyin is None:
                # Secondary vowels
                pinyin = _replace_character_with_tone(rawPinyin, "iu", tone)

                if pinyin is None:
                    # Just leave it the way it is (ex: "ng4")
                    pinyin = numberPinyin

        if pinyin is None:
            raise "Couldn't place tone mark for $rawPinyin!"

        return pinyin


class UnitTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pinyin(self):
        """Just various tests"""

        self.assertEqual("yóu", multiple_text_from_pinyin("you2"), "1")
        self.assertEqual("fú", multiple_text_from_pinyin("fu2"), "2")
        self.assertEqual("wángfújǐng", multiple_text_from_pinyin("wang2fu2jing3"), "3")
        self.assertEqual("lǜ yě", multiple_text_from_pinyin("lv4 ye3"), "4")
        self.assertEqual("lǚ xíng", multiple_text_from_pinyin("lu:3 xing2"), "5")
