"""The combination file data represents key combinations as a matrix. 
There is a column for each key and a row for each key. 
The value at the intersection of a row and column is the normalized distance
Note there are many redundancies since the distance from key A to key B is the same as from B to A.
"""

import sys
sys.path.append(".")
from typing import Any

def write_table(filename:str, data:dict[str, dict[str, Any]]) -> str:
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
            file_contents += f"\t{data[key1][key2]}"
        file_contents += "\n"
    
    with open(filename, "w") as f:
        f.write(file_contents)
    return file_contents

def write_md_table(filename:str, data:dict[str, dict[str, Any]], decimals:int=3) -> str:
    headers = data.keys()
    file_contents = f"||{"|".join(headers)}|\n"
    file_contents += f"|{"---|" * (len(headers)+1)}\n"
    for i, key1 in enumerate(headers):
        file_contents += f"|**{key1}**"
        for key2 in headers:
            num = round(data[key1][key2], decimals)
            file_contents += f"|{num}"
        file_contents += "|\n"
    
    with open(filename, "w") as f:
        f.write(file_contents)
    return file_contents
    
def read_table(filename:str) -> dict[str, dict[str, float]]:
    with open(filename, "r") as f:
        lines = f.read().split("\n")

        distribution_dict:dict[str, dict[str, float]] = {}

        column_headers = lines[0].split("\t")[1:]
        for line in lines[1:]:
            row = line.split("\t")
            for i, value in enumerate(row[1:]):
                key1 = row[0]
                key2 = column_headers[i]
                if key1 not in distribution_dict:
                    distribution_dict[key1] = {}
                distribution_dict[key1][key2] = float(value)
        
        return distribution_dict
