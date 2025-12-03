"""The combination file data represents key combinations as a matrix. 
There is a column for each key and a row for each key. 
The value at the intersection of a row and column is the normalized distance
Note there are many redundancies since the distance from key A to key B is the same as from B to A.
"""

import sys
sys.path.append(".")
from typing import Any

def write_table(filepath:str, data:dict[str, dict[str, Any]], null_value:str="NA") -> str:
    """Assumes that each subdict has the same keys as the root dict
    Ex: data = {
        KeyA: {KeyA: value, KeyB: value},
        KeyB: {KeyA: value, KeyB: value}
    }
    """
    headers = data.keys()
    file_contents = f"_\t{"\t".join(headers)}\n"
    for i, key1 in enumerate(headers):
        file_contents += f"{key1}"
        for key2 in headers:
            value = data[key1][key2]
            num = null_value if value is None else value
            file_contents += f"\t{num}"
        file_contents += "\n"
    
    with open(filepath, "w") as f:
        f.write(file_contents)
    return file_contents

def write_md_table(filepath:str, data:dict[str, dict[str, Any]], decimals:int=3, null_value:str="NA") -> str:
    headers = data.keys()
    file_contents = f"||{"|".join(headers)}|\n"
    file_contents += f"|{"---|" * (len(headers)+1)}\n"
    for i, key1 in enumerate(headers):
        file_contents += f"|**{key1}**"
        for key2 in headers:
            value = data[key1][key2]
            num = null_value if value is None else round(value, decimals)
            file_contents += f"|{num}"
        file_contents += "|\n"
    
    with open(filepath, "w") as f:
        f.write(file_contents)
    return file_contents

def write_single(filepath:str, data:dict[str, float]) -> str:
    with open(filepath, "w") as f:
        text_content = "LETTER\tCOUNT\n"
        text_content += "\n".join([f"{letter}\t{count}" for letter, count in data.items()])
        f.write(text_content)
        return text_content

def write_combination_ordered_chart(filepath:str, data:dict[str, dict[str, float|None]]) -> str:
    letter_combos:set[str] = set()
    new_data:list[tuple[str, float]] = []
    for letter1, subdict in data.items():
        for letter2, value in subdict.items():
            letter_combo = letter1 + letter2
            if letter_combo in letter_combos or letter2 + letter1 in letter_combos:
                continue
            if value is None:
                continue
            letter_combos.add(letter_combo)
            new_data.append((letter_combo, value))
    new_data = sorted(new_data, key=lambda x: x[1], reverse=True)

    with open(filepath, "w") as f:
        content:str = "KEY\tVALUE\n"
        content += "\n".join([f"{key}\t{value}" for key, value in new_data])
        f.write(content)
        
def read_table(filepath:str, null_value:str="NA") -> dict[str, dict[str, float|None]]:
    with open(filepath, "r") as f:
        lines = f.read().split("\n")

        distribution_dict:dict[str, dict[str, float|None]] = {}

        column_headers = lines[0].split("\t")[1:]
        for line in lines[1:]:
            row = line.split("\t")
            for i, value in enumerate(row[1:]):
                key1 = column_headers[i]
                key2 = row[0]
                if key1 not in distribution_dict:
                    distribution_dict[key1] = {}
                distribution_dict[key1][key2] = None if value == null_value else float(value)
        
        return distribution_dict

def test_write_read(filepath:str, data:dict[str, dict[str, float|None]]) -> bool:
    write_table(filepath, data)
    output = read_table(filepath)
    return output == data