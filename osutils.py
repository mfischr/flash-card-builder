import os
import shutil
__author__ = 'Michael'

def ensure_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def clear_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def make_valid_filename(str):
    """
    From http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python
    """
    return "".join((x if x.isalnum() else "_") for x in str)

