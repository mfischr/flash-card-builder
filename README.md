# flash-card-builder
Builds Mandarin Chinese flash cards using example sentences from iCIBA句库 (iciba.com).

## What is this?
This generates a bunch of fill-in-the-blank flash cards that can be directly imported into Anki. Sorry, simplified Chinese only for now.

For more detail, see the below section **What is this, really?**

## Getting set up
0. Install packages. You'll need `requests` and `lxml` (on Windows, get lxml from [this precompiled wheel site](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml))
1. Download CC-CEDICT (URL is in config.json). Update the path in config.json.
2. Create a file with the list of words you want, one per line. Save it as UTF-8 and update the path in config.json.
3. Run the program. It will take a while, as it's downloading definition pages for hundreds of words and parsing out the example sentences.
4. When it's done, you'll have cards-all.txt, which is tab-delimited and can be imported directly into Anki.
5. In Anki, import `Example Deck.apkg` as a new deck. This gives you two cards per word: one for recognizing the word, and one for producing it given a sentence (honestly, I've shied away from using the Produce card in my own learning; see below)
6. Whenever you add cards, just open the deck and import (Ctrl+I), using \t as the delimiter, and allowing HTML in fields.

## How to use flash cards
Everyone has their own language learning strategy, so what I say here may not apply to you. But here's what I've found out:

1. I do way better learning words in context (such as an essay or a TV commercial; a single example sentence isn't enough). For words I learn like this and practice a lot for at least a day, retention is somewhere around 90% for the first few days, 20% after a couple weeks, and 5% after a couple months. I have a terrible memory.
2. For words that I didn't learn in context, retention is much lower.
3. For a word to stick, I need to recognize it in another completely different context. This has to happen before I forget the word, obviously.

So the question is how to keep myself from forgetting the word before I see it again, and the answer is flash cards. For me, this is the only effective use for flash cards. But even with the flash cards, there's a time limit: if it's been a couple months and I haven't seen the word anywhere (including the original context), I've pretty much completely forgotten the word and need to relearn it.

## How to misuse cloze deletion cards
When I was taking Chinese classes, I'd create cloze deletion cards (fill-in-the-blank cards) with the new phrases using an example sentence from class. Same thing with ChinesePod and the dialogues there.

Drilled that for a long time, learned 1,000 cards or so. Result: I almost never used any of those words. Why? Imagine you have a cloze card for the word 准确 and in the sentence someone is complaining (开玩笑吧!) about how the weather forecast is never (___) 准确. However, humans are good at shortcuts, so after you drill that card for a couple weeks, on seeing 开玩笑吧 you'll just reflexively come up with 准确 for. Congratulations, you have learned nothing.

Here's the deal. Language production is all about translating the feeling of some situation or idea in your head, into a word that describes it. It's like seeing a picture of a tomato and thinking "tomato", except you can't take a picture of everything, so it's more like playing Taboo (that party game) with yourself. The key in building cards is to find some way to put your mind in many different situations where you need to produce that word, and to do so as naturally as possible. Cloze deletion cards don't really do that.

(Here's another way I noticed that this was a problem: every now and then a curious kid would sit next to me on the subway. He'd want to do my flash cards with me, but he, a native speaker, would rarely get the cards right. That seemed strange to me)

One partial solution? To prevent yourself from picking up random details in example sentences, you need some way to generate cards from a larger pool of examples. So I wrote this to scrape example sentences for words from iCIBA句库 (was using Bing before, but the Chinese on some of the sentences was weird). Each word gets 10 sentences, and when the card is shown one of the random sentences gets selected (Anki cards support JavaScript, which is awesome).

Another solution: as a hint, maybe show the first letter of the pinyin of each character. This will help you disambiguate cards that could be filled in with more than one word.
