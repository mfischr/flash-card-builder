# flash-card-builder
Builds Mandarin Chinese flash cards using example sentences from iCIBA句库 (iciba.com).

## What is this?
This generates a bunch of fill-in-the-blank flash cards that can be directly imported into Anki. Sorry, simplified Chinese only for now.

For more detail, see the below section **What is this, really?**

## Getting set up
0. Install packages. You'll need `requests` and `lmxl` (on Windows, get lxml from [this precompiled wheel site](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml))
1. Download CC-CEDICT (URL is in config.json). Update the path in config.json.
2. Create a file with the list of words you want, one per line. Save it as UTF-8 and update the path in config.json.
3. Run the program. It will take a while, as it's downloading definition pages for hundreds of words and parsing out the example sentences.
4. When it's done, you'll have cards-all.txt, which is tab-delimited and can be imported directly into Anki.
5. In Anki, import `Example Deck.apkg` as a new deck.  Open the deck and import cards (Ctrl+I), using \t as the delimiter, and allowing HTML in fields.

## What is this, really?
When I was taking Chinese classes, I'd create cloze deletion cards (fill-in-the-blank cards) with the new phrases using an example sentence from class. Same thing with ChinesePod and the dialogues there.

Drilled that for a long time, learned 1,000 cards or so. Result: When the card came up, I'd scan the sentence, recognize some detail in it, then remember what the word was from that detail. I rarely used any of those words in conversation. Fail.

Here's the deal. Language production is all about translating the feeling of some situation or idea in your head, into a word that describes it. It's like seeing a picture of a tomato and thinking "tomato", except you can't take a picture of everything, so it's more like playing Taboo (that party game) with yourself. The key in building cards is to find some way to put your mind in that situation where you need that word, but without invoking any incidental detail that's tied to the word. For example, imagine you have a cloze card for the word 准确 and the sentence talks about the accuracy of the weather forecast. After you drill that card for a couple weeks, as soon as you see the card with 天气预报 on the second line of text, you'll immediately know it's 准确. Congratulations, you have learned nothing.

The solution? You need some way to generate cards from a larger pool of example sentences, so when the card comes up it shows a random one of 10 sentences. So I wrote this to scrape example sentences for words from iCIBA句库 (was using Bing before, but the Chinese on some of the sentences was weird). Each word gets 10 sentences, and when the card is shown one of the random sentences gets selected (Anki cards support JavaScript, which is awesome).
