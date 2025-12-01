import pandas as pd

class SingleLetter():
    """Proportionally how likely each character is (0-1) where 1 is most likely
    Usually SPACE is 1.0 since space is the most common.
    """
    def __init__(self, filename:str) -> None:
        self.word_data = pd.read_csv(filename, delimiter="\t", keep_default_na=False, na_values=[''])
        self._single_letter_counts:dict[str, int] = self.count_single_letters()
        self.max_single_letter_count:float = max(self._single_letter_counts.values())

        self.single_letter_data:dict[str, float] = dict(
            [(key, float(value)/self.max_single_letter_count)\
            for key, value in self._single_letter_counts.items()]
        )

    def count_single_letters(self) -> dict[str, int]:
        """Count single letters in the words DataFrame."""
        letter_counts: dict[str, int] = {"SPACE":0}
        for index, word, count in self.word_data.itertuples():
            for letter in word:
                if letter in letter_counts:
                    letter_counts[letter] += count
                else:
                    letter_counts[letter] = count
            # assume that each word includes one space
            letter_counts["SPACE"] += count
        return letter_counts
    
class CombinationLetter:
    """Produces a matrix that represents the complexity between two keys. Normalized value (0-1) where 1 is preferrable.
    Example Table:
    data = {
        A:{
            A:None,
            B:0.1,
            C:0.2,
        },
        B:{
            A:0.1,
            B:None,
            C:0.3,
        },
        C:{
            A:0.2,
            B:0.3,
            C:None,
        }
    }
    The combination of the same letter is always None.
    Note order does not matter. data[A][B] == data[B][A]

    Possible Letters: SPACE, A, B, C...X, Y, Z
    """
    def __init__(self, filename:str) -> None:
        self.word_data = pd.read_csv(filename, delimiter="\t", keep_default_na=False, na_values=[''])
        self._combination_letter_counts = self.get_combination_letter_counts()
        # the maximum value in the combination_letter_data dict
        self.max_combination_letter = max(
            [max(
                [distance for distance in val.values() if distance is not None]
            ) for val in self._combination_letter_counts.values()]
        )
        self.combination_letter_data:dict[str, dict[str, float|None]] = dict(\
            [(key1, \
                dict([(key2, None if value is None else (float(value) / self.max_combination_letter))\
                for key2, value in subdict.items()])\
            ) for key1, subdict in self._combination_letter_counts.items()]\
        )
    
    def get_combination_letter_counts(self) -> dict[str, dict[str, int|None]]:
        """Count bigrams in the words DataFrame."""
        headers = ["SPACE","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        # empty table filled with 0s
        bigram_counts: dict[str, dict[str, int|None]] = dict(
            [(char, \
                dict([(char, 0) for char in headers])\
            ) for char in headers]
        )

        bigram_counts["SPACE"]["SPACE"] = None

        for index, word, count in self.word_data.itertuples():
            # beginning of word is
            bigram_counts["SPACE"][word[0]] += count
            bigram_counts[word[0]]["SPACE"] += count

            bigram_counts["SPACE"][word[-1]] += count
            bigram_counts[word[-1]]["SPACE"] += count

            for i in range(len(word) - 1):
                char1 = word[i]
                char2 = word[i+1]
                if char1 == char2:
                    bigram_counts[char1][char2] = None
                    bigram_counts[char2][char1] = None
                    continue
                bigram_counts[char1][char2] += count
                bigram_counts[char2][char1] += count
        return bigram_counts
