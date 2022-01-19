from statistics import mean

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

LETTER_SCORES = {letter: 0 for letter in LETTERS}

with open("assets/dico.txt") as dico:
    for line in dico:
        for letter in line[:-1]:
            LETTER_SCORES[letter] += 1

_mean = mean(LETTER_SCORES.values())

LETTER_SCORES = {key.upper(): s / _mean for key, s in LETTER_SCORES.items()}


LETTER_FREQUENCY_WEIGHT = 1
LETTER_DIVERSITY_WEIGHT = 3


def find_positions(word, letter_to_find):
    return [index for index, letter in enumerate(word) if letter == letter_to_find]
