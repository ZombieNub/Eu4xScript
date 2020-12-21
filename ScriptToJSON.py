"""
Hosts functions designed to easily convert a Clausewitz Engine script file to JSON.
"""

import json
import os
import sys
import re
from pathlib import Path
from typing import Dict

modifier_content_regex = re.compile(r'([a-zA-Z0-9._-]+)')
modifier_name_regex = re.compile(r'([a-zA-Z_]+)')


def clean_file(string: str) -> str:
    """
    Cleans up the string's contents to make parsing the string faster without eliminating functionality.

    :param string: String
    :return: String
    """
    return_string = re.sub(re.compile('#.*$', flags=re.MULTILINE), '', string)  # Clears out all comments
    return_string = re.sub(re.compile(' ', flags=re.MULTILINE), '', return_string)  # Replaces all unnecessary spaces
    return_string = re.sub(re.compile('\n+', flags=re.MULTILINE), ' ', return_string)  # Removes new lines
    return re.sub(re.compile('[\t]', flags=re.MULTILINE), '', return_string)  # Removes all tabs


def unique_key_id(string: str, input_dict: Dict) -> str:
    val = 0
    string_prefix = str(val) + "_"
    temp_string = string_prefix + string
    while temp_string in input_dict:
        val += 1
        string_prefix = str(val) + "_"
        temp_string = string_prefix + string
    return temp_string


def string_to_dict_set(string: str, starting: int = 0) -> [Dict, int]:
    """
    Converts cleaned string to nested dict. clean_file recommended.

    :param string: String
    :param starting: Search starting point. Not meant to be assigned outside of this function.
    :return: Nested dict
    """

    temp_dict = {}  # Blank dictionary for the nested flow control to affect

    c = starting  # This, along with the later starting = c + 1 limits the search index so the dictionary is never
    # stuck in an infinite loop.
    while c < len(string):
        # test = string[max(0, c - 5):min(c + 5, len(string))]  # Used in debugging function to more easily
        # see what letter c is referring to.
        if string[c] == "}":  # If we have reached the end of a category of modifiers, etc.
            return [temp_dict, c]  # Used to send the temp_dict back up the recursion function
        if string[c] == "=":  # If a new modifier or category has been found
            if string[c + 1] == "{":  # If we have found a category
                modifier_name = re.search(modifier_name_regex, string[starting:c]).group(1)  # Find the category name
                modifier_name = unique_key_id(modifier_name, temp_dict)
                modifier_content = string_to_dict_set(string, c + 2)  # Find the category contents using recursion
                temp_dict[modifier_name] = modifier_content[0]  # Add the category and contents to temp_dict
                c = modifier_content[1]  # Skip c past the combined category name and contents to avoid repetition
            else:  # If we have found a modifier

                modifier_name = re.search(modifier_name_regex, string[starting:c]).group(1)  # Find the modifier name
                modifier_name = unique_key_id(modifier_name, temp_dict)
                modifier_content = re.search(modifier_content_regex, string[c:]).group(1)  # Find the modifier contents
                try:
                    temp_dict[modifier_name] = float(modifier_content)  # If the value is a number convert it to a float
                except ValueError:
                    temp_dict[modifier_name] = modifier_content  # Else, keep it as a string
                c += len(modifier_content)  # Skip c past the modifier contents to avoid repetition
            starting = c + 1  # Advance starting to avoid repetition
        c += 1  # Advance the while loop

    return [temp_dict, c]  # Necessary to avoid returning a NoneType


def conv_file_read(file: str):
    """
    Convenient file reading and conversion function to simplify later code.

    :param file: Input file
    :return: Nested dict
    """
    with open(Path(file), 'rt') as input_file:
        input_file_contents = input_file.read()
    return string_to_dict_set(clean_file(input_file_contents))[0]


if __name__ == '__main__':
    converted_file = conv_file_read(sys.argv[1])
    if os.path.exists("data.json"):
        os.remove("data.json")
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(converted_file, f, indent=4, ensure_ascii=False)
