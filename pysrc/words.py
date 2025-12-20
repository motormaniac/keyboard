import sys
sys.path.append(".")
from random import shuffle

ADDED_CHARACTERS = [
    ["e","a","s","i","t","n"],
    ["r", "h"],
    ["p", "u"],
    ["l","f"],
    ["d", "o"],
    ["m", "c"],
    ["y", "w"],
    ["b", "g"],
    ["v", "j"],
    ["z", "k"],
    ["x", "q"],
]

WORD_MAX = 500 # maximum words to generate per line. -1 means unlimited
current_characters:list[str] = []
output_lines:list[str] = []

word_list = []
with open("data/google-10000-english-no-swears.txt", "r") as f:
    word_list = [word.strip() for word in f.readlines()]
    shuffle(word_list)

# each word is separated by a newline
for new_characters in ADDED_CHARACTERS:
    current_characters += new_characters
    print(current_characters)
    this_line:str = ""
    word_count = 0
    for word in word_list:
        if not WORD_MAX == -1 and word_count >= WORD_MAX:
            break
        word = word.strip()
        only_has_allowed_letters = True
        # check that the word contains only allowed characters
        for char in word:
            if char not in current_characters:
                only_has_allowed_letters = False
        if not only_has_allowed_letters:
            continue
        # check that at least one of the added chars exists
        contains_new_letters = False
        for char in new_characters:
            if char in word:
                contains_new_letters = True
                break
        if not contains_new_letters:
            continue
        this_line += f"'{word}', "
        word_count += 1
    output_lines.append(f"\n\t'{", ".join(new_characters)}': [{this_line}],")
    print(word_count)

with open("data/practice_words.txt", "w") as f:
    f.write(f"{{{"".join(output_lines)}\n}}")
