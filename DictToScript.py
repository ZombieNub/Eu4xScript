import os
import re
import sys
from typing import Dict

from Scale_Ideas import ScaleModifiers
from ScriptToJSON import conv_file_read

number_tag_regex = re.compile(r'[0-9-]+_')


def dict_to_script(input_file: Dict, layer: int = 0):
    temp_script = ""
    for k, v in input_file.items():
        k_shaved = re.sub(number_tag_regex, '', k)
        if isinstance(v, dict):
            temp_script += (("    " * layer) + k_shaved + " = {\n" + (dict_to_script(v, layer + 1)) + (
                    "    " * layer) + "}\n")
        else:
            # special case time!
            if v == "ThirdRome":
                v = "\"Third Rome\""
            temp_script += (("    " * layer) + k_shaved + " = " + str(v) + "\n")
    return temp_script


if __name__ == "__main__":
    converted_file = conv_file_read(sys.argv[1])
    converted_file = ScaleModifiers.modify_ideas(converted_file, float(sys.argv[2]))
    script = dict_to_script(converted_file)
    if os.path.exists("00_basic_ideas.txt"):
        os.remove("00_basic_ideas.txt")
    with open('00_basic_ideas.txt', 'w', encoding='utf-8') as f:
        f.write(script)
