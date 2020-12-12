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
Due to restructuring, this file will be used for all possible files that can be modified.
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
from typing import TextIO, IO


# Current up to date Regex: (It works, but it's stupidly large
# (?<!ai_will_do|modifier\s*=\s*{\n\s*factor\s*=\s*[0-9.-]+\n\s*(?:[a-zA-Z_0-9=. -]+\n\s*)*)(?<=(?:{\n\s*(?:\s*#[\s\w\(\)]+)?)|(?:\s*[a-zA-Z_]+\s*=\s*[0-9.-]+\s*(?:\s*#[\s\w\(\)]+\n\s*)?))(?<=\s*)(?!factor|province_id)([a-zA-Z_]+)\s*=\s*([0-9.-]+)
# I don't know why and I don't want to know why but Python's implementation of RegEx doesn't support repetition in the
# lookbehinds. Looks like I'll have to get more creative with my RegEx now. Keeping the old RegEx for later reference.
# This may requires some planning.

class IdentifyModifiers:
    """
    Broad class for changing modifiers
    """
    def __init__(self):
        modifier_regex = re.compile(
            r"	*[a-zA-Z_]+ *= *{\n(?:\s*[a-zA-Z_]+ *= *(?:[0-9.-]|(?:(?:yes)|(?:no)))+\s*\n)+\s*}")

    def modify_ideas(file: str, scale: float = 10) -> IO:
        """
        Finds every modifier in the file, and stores it in an array. Note: Currently doesn't work, this only describes
        the intended implementation.
        :param file: Input file where EU4 ideas are stored. (Must include directory)
        :param scale: Number that every modifier is multiplied by. Defaults to 10.
        :return IO: New output file where the modifiers found have been multiplied by scale
        """

        print("Hello!")  # Test function to get the errors to shut up for a bit
        input_file = open(Path(file),
                          'rt')  # Get the input file and put it into input_file, accounting for OS differences
        return input_file  # Return the file


if __name__ == '__main__':
    """
    If run directly, returns a list of all modifiers found in a file, including line number.
    Of course right now it doesn't do that since I haven't written it yet.
    """
    # print("Hello!")  # Test function
    test_file = IdentifyModifiers.modify_ideas(
        'testing/00_basic_ideas.txt')  # Grab a test file and put it into the function
    for i in test_file.readlines():
        print(i, end="")  # Read the output of the function to make sure it works.
    test_file.close()
