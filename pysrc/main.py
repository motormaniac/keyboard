import sys
sys.path.append(".")

from pysrc import keymap
from pysrc import lettermap
from pysrc import fileio

def write_single_key_data() -> None:
    with open ("data/single_key_data.txt", "w") as f:
        f.write("\t".join([str(x) for x in keymap.single_key_distribution]))

def write_combination_key_data() -> None:
    combination_key = keymap.CombinationKey()
    fileio.write_table("data/combination_key_data.txt", combination_key.combination_key_data)

def write_combination_key_md_data() -> None:
    combination_key = keymap.CombinationKey()
    fileio.write_md_table("data/combination_key_data.md", combination_key.combination_key_data)

def write_single_letter_data() -> None:
    single_letter = lettermap.SingleLetter("data/google-books-common-words.txt")
    fileio.write_single("data/single_letter_frequencies.txt", single_letter.single_letter_data)

def write_combination_letter_data() -> None:
    combination_letter = lettermap.CombinationLetter("data/google-books-common-words.txt")
    fileio.write_table("data/combination_letter_data.txt", combination_letter.combination_letter_data)

def write_combination_letter_md_data() -> None:
    combination_letter = lettermap.CombinationLetter("data/google-books-common-words.txt")
    fileio.write_md_table("data/combination_letter_data.md", combination_letter.combination_letter_data)

def test_write_read() -> None:
    combination_letter = lettermap.CombinationLetter("data/google-books-common-words.txt")
    print(fileio.test_write_read("test.txt", combination_letter.combination_letter_data))

def visualize_keymap() -> None:
    key_map:list[str] = ["K","P","T","Y","J","I","O","A","E","G","Z","SPACE","U","_","_","M","C","N","F","W","L","H","D","S","B","R","SPACE","V","X","Q"]
    # key_map:list[str] = keymap.key_list
    with open("data/layout_visual.md", "w") as f:
        f.write(f"""|{key_map[10]}|{key_map[11]}|{key_map[12]}|{key_map[13]}|{key_map[14]}||{key_map[25]}|{key_map[26]}|{key_map[27]}|{key_map[28]}|{key_map[29]}|
|---|---|---|---|---|---|---|---|---|---|---|
|{key_map[5]}|{key_map[6]}|{key_map[7]}|{key_map[8]}|{key_map[9]}||{key_map[20]}|{key_map[21]}|{key_map[22]}|{key_map[23]}|{key_map[24]}|
|{key_map[0]}|{key_map[1]}|{key_map[2]}|{key_map[3]}|{key_map[4]}||{key_map[15]}|{key_map[16]}|{key_map[17]}|{key_map[18]}|{key_map[19]}|
""")

write_single_key_data()
