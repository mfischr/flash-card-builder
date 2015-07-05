# flash-card-builder
Builds Mandarin Chinese flash cards using example sentences from online dictionaries.

## What is this?
This generates a bunch of fill-in-the-blank flash cards that can be directly imported into Anki. Sorry, simplified Chinese only for now.

For more detail, see the below section **What is this, really?**

## Getting set up
1. Verify that the paths in config.json are what you want them to be.
2. Download the resources: HSK word list and frequency order, and CC-CEDICT. Links in config.json.
3. Run the program. It will take a while, as it's downloading definition pages for hundreds of words and parsing out the example sentences.
4. When it's done, you'll have cards-all.txt, which is tab-delimited and can be imported directly into Anki.
5. Import into Anki, using tab \t as the delimiter.
6. Create new cards, using anki-card.css and anki-card.html as templates.

## What is this, really?
When I was taking classes, I'd create cloze deletion cards (fill-in-the-blank cards) with the new phrases using an example sentence from class. Same thing with ChinesePod and the dialogues there.

Drilled that for a long time, learned 1,000 cards or so. Result: When the card came up, I'd scan the sentence, recognize some detail in it, then remember what the word was from that detail. I rarely used any of those words in conversation. Fail.

Here's the deal. Language production is all about translating the feeling of some situation or idea in your head, into a word that describes it. It's like seeing a picture of a tomato and thinking "tomato", except you can't take a picture of everything, so it's more like playing Taboo (that party game) with yourself. The key in building cards is to find some way to put your mind in that situation where you need that word, but without invoking any incidental detail that's tied to the word. For example, imagine you have a cloze card for the word 准确 and the sentence talks about the accuracy of the weather forecast. After you drill that card for a couple weeks, as soon as you see the card with 天气预报 on the second line of text, you'll immediately know it's 准确. Congratulations, you have learned nothing.

The solution? You need some way to generate cards from a larger pool of example sentences, so when the card comes up it shows a random one of 10 sentences. So I wrote this to scrape example sentences for HSK <n> words from Bing 词典. Each word gets 10 sentences, and when the card is shown one of the random sentences gets selected (Anki cards support JavaScript, which is awesome). I've done most of HSK 4 this way and it works wayyyy better than before.
