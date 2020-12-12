import json
import sys
import re
from pathlib import Path

space_cleaning_regex = re.compile(' ')
equals_regex = re.compile('=')
opening_bracket_regex = re.compile('{')
closing_bracket_regex = re.compile('}')
modifier_content_regex = re.compile(r'([a-zA-Z0-9._]+)')
modifier_name_regex = re.compile(r'([a-zA-Z_]+)')


def clean_file(string):
    return_string = re.sub(re.compile('#.*$', flags=re.MULTILINE), '', string)  # Clears out all comments
    return_string = re.sub(re.compile(' ', flags=re.MULTILINE), '', return_string)  # Replaces all unnecessary spaces
    return_string = re.sub(re.compile('\n+', flags=re.MULTILINE), ' ', return_string)  # Removes new lines
    return re.sub(re.compile('[\t]', flags=re.MULTILINE), '', return_string)  # Removes all tabs


def string_to_array_set(string, starting=0):
    temp_dict = {}  # Blank dictionary for the nested flow control to affect

    c = starting  # This, along with the later starting = c + 1 limits the search index so the dictionary is never
    # stuck in an infinite loop.
    while c < len(string):
        test = string[max(0, c - 5):min(c + 5, len(string))] # Used in Pycharm's debugging function to more easily see what letter c is referring to.
        if string[c] == "}":
            return [temp_dict, c]
        if string[c] == "=":
            if string[c + 1] == "{":
                modifier_name = re.search(modifier_name_regex, string[starting:c]).group(1)
                modifier_content = string_to_array_set(string, c + 2)
                temp_dict[modifier_name] = modifier_content[0]
                c = modifier_content[1]
            else:
                modifier_name = re.search(modifier_name_regex, string[starting:c]).group(1)
                modifier_content = re.search(modifier_content_regex, string[c:]).group(1)
                temp_dict[modifier_name] = modifier_content
                c += len(modifier_content)
            starting = c + 1
        c += 1

    return temp_dict


if __name__ == '__main__':
    modifier_regex = re.compile('^\t*([a-zA-Z_]+) *= *([a-zA-Z_0-9.-]+)$', flags=re.MULTILINE)
    with open(Path(sys.argv[1]), 'rt') as input_file:
        input_file_contents = input_file.read()
        converted_file = string_to_array_set(clean_file(input_file_contents))
        print(converted_file)
        json_data = json.dumps(converted_file)
        print(json_data)
        print(clean_file(input_file_contents))
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
