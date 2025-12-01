# taken directly from research paper
single_key_distribution:list[float] = [
    3.32, 4.12, 4.22, 3.82, 3.15,
    5.15, 5.25, 5.35, 5.25, 4.05,
    3.73, 3.73, 3.93, 3.15, 1.76,
]

key_list:list[str] = [
    "000", "010", "020", "030", "040",
    "100", "110", "120", "130", "140",
    "200", "210", "220", "230", "240",
    "001", "011", "021", "031", "041",
    "101", "111", "121", "131", "141",
    "201", "211", "221", "231", "241",
]

class CombinationKey:
    # constants
    CONSTANTS_CALCULATED:bool = False
    MAX_VALUE:float
    COMBINATION_KEY_DATA:dict[str, dict[str, float]]

    def __init__(self) -> None:
        self.max_value = self.get_distance_max()
        self.combination_key_data = self.get_combination_key_data()

    # Keycode is 110.
    # first 0-2 is row bottom to top, second 0-4 is column left to right, third character 0-1 is swap layer
    def calc_key_distance(self, key1:str, key2:str) -> float:
        """Calculates the distance between two keys on the keyboard
        Undirectional (order of key1 and key2 does not matter)
        """
        distance:float = 0
        if key1 == key2:
            return 0
        
        key1_row = int(key1[0])
        key2_row = int(key2[0])
        key1_col = int(key1[1])
        key2_col = int(key2[1])

        # repeating fingers
        if key1[2] != key2[2]: # Using the switch key has a high distance
            distance += 2
        else:
            if key1_col == key2_col:
                # using the same finger
                distance += 2
            elif (key1_col == 3 and key2_col == 4) or (key1_col == 4 and key2_col == 3):
                # Using index twice on adjacent keys
                distance += 2

        # locational constraints

        # moving two rows is a lot
        # moving one row is a little
        # same row is no cost
        distance += abs(key1_row - key2_row)
        if key1_row != 1 or key2_row != 1:
            # prioritize the homerow
            distance += 1

        # long fingers = middle and index (2,3,4)
        # short fingers = pinkie and ring (0,1)

        # it is uncomfortable to have short fingers above long fingers
        if key1_col in [0,1] and key2_col in [2,3,4]\
        and key1_row > key2_row:
            distance += 2
        # same thing but switch the order
        elif key2_col in [0,1] and key1_col in [2,3,4]\
        and key2_row > key1_row:
            distance += 2
        return distance

    def get_distance_max(self) -> float:
        distances:list[float] = []
        for i, key1 in enumerate(key_list):
            for j, key2 in enumerate(key_list, i):
                distance = self.calc_key_distance(key1, key2)
                distances.append(distance)
        return max(distances)

    def normalize_distance(self, distance:float) -> float:
        return distance / self.max_value

    def get_combination_key_data(self) -> dict[str, dict[str, float]]:
        output:dict[str, dict[str, float]] = {}
        for i, key1 in enumerate(key_list):
            output[key1] = {}
            for j, key2 in enumerate(key_list, 0):
                # If you wanted to remove redundancies, iterate starting from i instead of 0
                distance = self.calc_key_distance(key1, key2)
                output[key1][key2] = self.normalize_distance(distance)
        return output
