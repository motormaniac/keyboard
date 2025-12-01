import sys
sys.path.append(".")

from pysrc import keymap
from pysrc import lettermap
from pysrc import fileio

def write_combination_key_data() -> None:
    combination_key = keymap.CombinationKey()
    fileio.write_table("data/combination_key_data.txt", combination_key.combination_key_data)

def write_combination_key_md_data() -> None:
    combination_key = keymap.CombinationKey()
    fileio.write_md_table("data/combination_key_data.md", combination_key.combination_key_data)

def write_single_letter_data() -> None:
    single_letter = lettermap.SingleLetter("data/google-books-common-words.txt")
    with open("data/single_letter_frequencies.txt", "w") as f:
        text_content = "LETTER\tCOUNT\n"
        text_content += "\n".join([f"{letter}\t{count}" for letter, count in single_letter.single_letter_data.items()])
        f.write(text_content)

def write_combination_letter_data() -> None:
    combination_letter = lettermap.CombinationLetter("data/google-books-common-words.txt")
    fileio.write_table("data/combination_letter_data.txt", combination_letter.combination_letter_data)

write_combination_letter_data()