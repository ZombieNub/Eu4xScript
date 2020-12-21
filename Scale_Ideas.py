"""
Edits idea modifiers in Eu4 scripts.

I'm only happy that due to ScriptToJSON.py I no longer have to do such much RegEx futzing or planning.
"""
import json
import os
import re
import sys
from typing import Dict

import ScriptToJSON


class ScaleModifiers:
    """
    Broad class for changing modifiers
    """

    def __init__(self):
        pass

    @staticmethod
    def modify_ideas(modifiers_dict: Dict, scale: float = 10, debug_print=False) -> Dict:
        """
        Static method that scales up every modifier by a certain amount, skipping triggers and AI modifiers.

        :param debug_print: Set to true to see what every number is changed to.
        :param modifiers_dict: Input nested dict
        :param scale: Number to scale up modifiers by
        :return: Modified nested dict
        """
        temp_dict = {}
        number_tag_regex = re.compile(r'[0-9-]+_')
        for k, v in modifiers_dict.items():
            k_shaved = re.sub(number_tag_regex, '', k)
            if k_shaved == "trigger" or k_shaved == "ai_will_do":  # Skip over conditionals and AI modifiers to prevent
                # either from breaking
                temp_dict[k] = v
            elif isinstance(v, dict):  # Loops through nested dictionaries using recursion
                temp_dict[k] = ScaleModifiers.modify_ideas(v, scale)
            else:
                if isinstance(v, float) or isinstance(v, int):  # Are we dealing with a numbered modifier?
                    if debug_print:
                        print(f"{k}: {v} -> {round(v * scale, 5)}")
                    temp_dict[k] = round(v * scale, 5)  # Round is used to remove floating point artifacts
                else:
                    temp_dict[k] = v
        return temp_dict


if __name__ == '__main__':
    converted_file = ScriptToJSON.conv_file_read(sys.argv[1])
    new_dict = ScaleModifiers.modify_ideas(converted_file, 10)
    if os.path.exists("dataScaled.json"):
        os.remove("dataScaled.json")
    with open('dataScaled.json', 'w', encoding='utf-8') as f:
        json.dump(new_dict, f, indent=4, ensure_ascii=False)
