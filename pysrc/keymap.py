# # taken directly from research paper
single_key_distribution:list[float] = [
    3.73, 3.73, 3.93, 3.15, 1.76,
    5.15, 5.25, 5.35, 5.25, 4.05,
    3.32, 4.12, 4.22, 3.82, 3.15,

    3.73, 3.73, 3.93, 3.15, 1.76,
    5.15, 5.25, 5.35, 5.25, 4.05,
    3.32, 4.12, 4.22, 3.82, 3.15,
]

# normalize distribution and prioritize the default layer
single_key_distribution = [
    (x+0.5) if i < 15 else x 
    for i, x in enumerate(single_key_distribution)]
single_key_distribution_max = max(single_key_distribution)
single_key_distribution = [
    x / single_key_distribution_max
    for x in single_key_distribution]
# print(single_key_distribution)

single_key_distribution = [
    0.7230769230769232, 0.7230769230769232, 0.7572649572649572, 0.6239316239316239, 0.3863247863247863,
    0.9658119658119659, 0.982905982905983, 1.0, 0.982905982905983, 0.7777777777777778,
    0.652991452991453, 0.7897435897435898, 0.8068376068376069, 0.7384615384615385, 0.6239316239316239,
    
    0.6376068376068377, 0.6376068376068377, 0.6717948717948719, 0.5384615384615384, 0.3008547008547009,
    0.8803418803418804, 0.8974358974358975, 0.9145299145299145, 0.8974358974358975, 0.6923076923076923,
    0.5675213675213675, 0.7042735042735043, 0.7213675213675214, 0.652991452991453, 0.5384615384615384]

    
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
    """Produces a matrix that represents the complexity between two keys. Normalized value (0-1) where 1 is preferrable.
    Example Table:
    data = {
        KeyA:{
            KeyA:None,
            KeyB:0.1,
            KeyC:0.2,
        },
        KeyB:{
            KeyA:0.1,
            KeyB:None,
            KeyC:0.3,
        },
        KeyC:{
            KeyA:0.2,
            KeyB:0.3,
            KeyC:None,
        }
    }
    The combination of the same keys is always None.
    Note order does not matter. data[KeyA][KeyB] == data[KeyB][KeyA]

    KeyCodes are represented by a three digit string (000).
    - first digit row (0-2): 0 is bottom row, 2 is top row
    - second digit column (0-4): 0 is left (pinkie), 4 and 5 are on the right (index)
    - third column layer (0-1): Which layer of letters. Pressing space switches layers
    """
    def __init__(self) -> None:
        self._combination_key_distances = self.get_combination_key_distances()
        self.max_distance = max(
            [max(
                [distance for distance in val.values() if distance is not None]
            ) for val in self._combination_key_distances.values()]
        )
        # normalize values and flip range (0-1 becomes 1-0)
        self.combination_key_data:dict[str, dict[str, float|None]] = dict(\
            [(key1, \
                dict([(key2, None if value is None else 1 - (float(value) / self.max_distance))\
                for key2, value in subdict.items()])\
            ) for key1, subdict in self._combination_key_distances.items()]\
        )

    # costs of different key actions
    # switching layers is very costly
    SWITCH_KEY = 3
    # using the same finger
    SAME_FINGER = 2
    # pressing adjacent keys with the index finger
    ADJACENT_INDEX_FINGER = 3
    # prioritize the homerow
    HOME_ROW_PRIORITY = 1
    # jumping just one row
    CHANGE_ONE_ROW = 1
    # jumps of two rows
    CHANGE_TWO_ROWS = 3
    # deprioritize having short fingers above long fingers because it is uncomfortable
    SHORT_FINGER_ABOVE_LONG_FINGER = 2
    # I don't like combinations of my fingers on the bottom and middle row
    # because of staggered keyboard
    BOTTOM_MIDDLE_ROW_COMBINATION = 2
    
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

        if key1[2] != key2[2]: # Using the switch key has a high distance
            distance += self.SWITCH_KEY
        else:
            if key1_col == key2_col:
                # using the same finger
                distance += self.SAME_FINGER
            elif (key1_col == 3 and key2_col == 4) or (key1_col == 4 and key2_col == 3):
                # Using index finger twice on adjacent keys
                distance += self.ADJACENT_INDEX_FINGER

        # locational constraints

        # moving two rows is a lot
        # moving one row is a little
        # same row is no cost
        if key1_row != 1 or key2_row != 1:
            # prioritize the homerow
            distance += self.HOME_ROW_PRIORITY
        if abs(key1_row - key2_row) == 1:
            distance += self.CHANGE_ONE_ROW
        elif abs(key1_row - key2_row) == 2: # I really don't want to jump 2 rows
            distance += self.CHANGE_TWO_ROWS

        # long fingers = middle and index (2,3,4)
        # short fingers = pinkie and ring (0,1)

        # it is uncomfortable to have short fingers above long fingers
        if key1_col in [0,1] and key2_col in [2,3,4]\
        and key1_row > key2_row:
            distance += self.SHORT_FINGER_ABOVE_LONG_FINGER
        # same thing but switch the order
        elif key2_col in [0,1] and key1_col in [2,3,4]\
        and key2_row > key1_row:
            distance += self.SHORT_FINGER_ABOVE_LONG_FINGER

        # I don't like combinations of my fingers on the bottom and middle row
        # because of staggered keyboard
        if key1_row == 0 and key2_row == 1 and key2_col - key1_col == 1:
            distance += self.BOTTOM_MIDDLE_ROW_COMBINATION
        elif key2_row == 0 and key1_row == 1 and key1_col - key2_col == 1:
            distance += self.BOTTOM_MIDDLE_ROW_COMBINATION

        return distance

    def get_distance_max(self) -> float:
        distances:list[float] = []
        for i, key1 in enumerate(key_list):
            for j, key2 in enumerate(key_list, i):
                distance = self.calc_key_distance(key1, key2)
                distances.append(distance)
        return max(distances)

    def get_combination_key_distances(self) -> dict[str, dict[str, float|None]]:
        output:dict[str, dict[str, float|None]] = dict([(key, {}) for key in key_list])
        for i, key1 in enumerate(key_list):
            for j, key2 in enumerate(key_list, i):
                if key1 == key2:
                    output[key1][key2] = None
                    continue
                # If you wanted to remove redundancies, iterate starting from i instead of 0
                distance = self.calc_key_distance(key1, key2)
                output[key1][key2] = distance
                output[key2][key1] = distance
        return output
    