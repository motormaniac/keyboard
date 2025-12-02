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

def get_layout_visual(layout:list[str]) -> str:
    return f"""|{layout[10]}|{layout[11]}|{layout[12]}|{layout[13]}|{layout[14]}||{layout[25]}|{layout[26]}|{layout[27]}|{layout[28]}|{layout[29]}|
|---|---|---|---|---|---|---|---|---|---|---|
|{layout[5]}|{layout[6]}|{layout[7]}|{layout[8]}|{layout[9]}||{layout[20]}|{layout[21]}|{layout[22]}|{layout[23]}|{layout[24]}|
|{layout[0]}|{layout[1]}|{layout[2]}|{layout[3]}|{layout[4]}||{layout[15]}|{layout[16]}|{layout[17]}|{layout[18]}|{layout[19]}|
"""

def visualize_keymap() -> None:
    layout1:list[str] = "O U P M F E A SPACE T R X V H C L Y Q _ B J N I SPACE S D Z _ K G W".split(" ")
    layout2:list[str] = "K Y X V _ SPACE E A S D B P R L M G W Q Z _ SPACE T I N H J F O U C".split(" ")
    with open("data/layout_visual.md", "w") as f:
        f.write(f"{get_layout_visual(layout1)}\n\n{get_layout_visual(layout2)}"
)
# write_single_key_data()
# write_combination_key_data()
visualize_keymap()