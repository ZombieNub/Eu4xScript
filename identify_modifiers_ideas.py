"""
Identifies modifiers in common/ideas folder

Idea
EU4 has a specific structure regarding it's idea modifiers that can make it easy to figure out where the modifiers are.
The previous naive implementation, which is looking at every line for specific features, catches conditions and AI
factors as well, which requires filtering out, resulting in a large and slow filter list. A new implementation that
can well where the modifiers based on the whole file's contents should let the whole program run far smoother and cut
down on the amount of words in the filter list.

Notes
I plan on relegating this script only to files in the common/ideas folder, but if the rest of the Eu4 modifiers carry
the same structure, I will expand this script to those as well.
Turns out python's RegEx (re) has a lot of helpful functions that I will find very useful, like re.findall and
re.finditer
In reforming the RegEx, I need to achieve a few things
1. Allow use of filters inside the RegEx itself, and break it up for clarification
    (https://stackoverflow.com/questions/2078915/a-regular-expression-to-exclude-a-word-string)
2. Remove the multiline and instead have it find multiple matches at once throughout the whole file.
    (https://stackoverflow.com/questions/4697882/how-can-i-find-all-matches-to-a-regular-expression-in-python)
"""

import sys
import os
from pathlib import Path
import re
from collections import Counter
from typing import TextIO


def regex_find_modifiers_and_apply_scale(file, scale=10):
    """
    Finds every modifier in the file, and stores it in an array.
    :param file: Input file where EU4 ideas are stored.
    :param scale: Number that every modifier is multiplied by. Defaults to 10.
    :return : New output file where the modifiers found have been multiplied by scale
    """
    print("Hello!")  # Test function to get the errors to shut up for a bit


if __name__ == '__main__':
    """
    If run directly, returns a list of all modifiers found in a file, including line number.
    Of course right now it doesn't do that since I haven't written it yet.
    """
    print("Hello!")  # Test function
