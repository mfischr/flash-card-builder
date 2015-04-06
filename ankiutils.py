import os.path
import codecs

def _remove_newlines(s):
    return s.replace("\n", "\\n").replace("\r", "\\r")

def write_deck_for_import(file_tag, cards):
    """Writes out the cards for import into Anki.  The file used for import is a temporary file.
    Cards is a list of dictionaries which have the properties unique_name, front, back.
    """
    file_name = os.path.expandvars("$Temp\\cards-{0}.txt".format(file_tag))

    with codecs.open(file_name, "w", "utf-8") as file:
        file.write("Z\tZ\tZ\n")  # Add a dummy card to ensure the delimiter is detected correctly
        for card in cards:
            file.write("{0}\t{1}\t{2}\n".format(card['id'], _remove_newlines(card['front']), _remove_newlines(card['back'])))

    return file_name
