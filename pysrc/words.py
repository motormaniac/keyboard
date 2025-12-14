import sys
sys.path.append(".")

CHARACTERS = ["e","a","s","i","t","n"]

output_words = []

with open("data/words.txt", "r") as f:
    # each word is separated by a newline
    for word in f:
        word = word.strip()
        valid_word = True
        for char in word:
            if char not in CHARACTERS:
                valid_word = False
        if valid_word:
            output_words.append(word)

with open("data/practice_words.txt", "w") as f:
    f.write(" ".join(output_words))