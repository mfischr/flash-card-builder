import os
import os.path
import codecs
import logging
import osutils

def _remove_newlines(s):
    return s.replace("\n", "\\n").replace("\r", "\\r")

def write_deck_for_import(folder, file_tag, cards):
    """Writes out the cards for import into Anki.  The file used for import is a temporary file.
    Cards is a list of lists which have the properties to write to the cards.
    """
    os.makedirs(folder, exist_ok=True)
    file_name = os.path.join(folder, "cards-{0}.txt".format(file_tag))

    with codecs.open(file_name, "w", "utf-8") as file:
        file.write("\t".join(['Z'] * len(cards[0])))  # Add a dummy card to ensure the delimiter is detected correctly
        file.write("\n")

        for card in cards:
            file.write("\t".join([_remove_newlines(field) for field in card]))
            file.write("\n")

    logging.info("Wrote {0} cards to '{1}'".format(len(cards), file_name))

    return file_name
