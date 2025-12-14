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

def write_key_combination_chart() -> None:
    combination_letter = lettermap.CombinationLetter("data/google-books-common-words.txt")
    fileio.write_combination_ordered_chart("data/key_combination_chart.txt", combination_letter.combination_letter_data)

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
    # layout1:list[str] = "L O U F P E A SPACE T R X V H C M B Y _ J Q N I SPACE S D Z _ K G W".split(" ")
    layout2:list[str] = "P M Q V X SPACE T E S H U F O R C K W Z _ _ SPACE I N A D J Y L G B".split(" ")
    layout3:list[str] = "O U P M F E A SPACE T R X V H C L Y Q _ B J N I SPACE S D Z _ K G W".split(" ")
    layout4:list[str] = "K Y X V _ SPACE E A S D B P R L M G W Q Z _ SPACE T I N H J F O U C".split(" ")
    # keys on the same row are encouraged
    layout5:list[str] = "V W _ X _ SPACE T E H D P F O R M K G J Q Z SPACE A I S N B Y U L C".split(" ")
    layout6:list[str] = "P U Q V X SPACE E A R S B Y D L M K G _ Z _ SPACE T I N H J W O F C".split(" ")
    layout7:list[str] = "P B X Z _ SPACE E A S R V Y D L M U G Q J _ SPACE I T N H K W O F C".split(" ")
    with open("data/layout_visual.md", "w") as f:
        content = "\n\n".join([get_layout_visual(x) for x in [layout2, layout3, layout4, layout5, layout6, layout7]])
        f.write(content)

def write_edited_time_data() -> None:
    data = fileio.read_time_data("time_data/time_data_combined.txt")
    fileio.write_table("data/edited_time_data.txt", data)

write_edited_time_data()
