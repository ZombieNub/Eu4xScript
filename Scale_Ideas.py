"""
Edits idea modifiers in Eu4 scripts.

I'm only happy that due to ScriptToJSON.py I no longer have to do such much RegEx futzing or planning.
"""
import json
import os
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
    def modify_ideas(modifiers_dict: Dict, scale=10):
        temp_dict = {}
        for k, v in modifiers_dict.items():
            if k == "trigger" or k == "ai_will_do":
                temp_dict[k] = v
                continue
            if isinstance(v, dict):
                temp_dict[k] = ScaleModifiers.modify_ideas(v, scale)
            else:
                if isinstance(v, float) or isinstance(v, int):
                    print(f"{k}: {v} -> {v*scale}")
                    temp_dict[k] = v * scale
                else:
                    temp_dict[k] = v
        return temp_dict



if __name__ == '__main__':
    converted_file = ScriptToJSON.conv_file_read(sys.argv[1])
    new_dict = ScaleModifiers.modify_ideas(converted_file)
    if os.path.exists("dataScaled.json"):
        os.remove("dataScaled.json")
    with open('dataScaled.json', 'w', encoding='utf-8') as f:
        json.dump(new_dict, f, indent=4, ensure_ascii=False)
