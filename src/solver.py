from functools import cmp_to_key

from src.inputs import input_result, input_word, proceed
from src.letters import LETTERS, find_positions
from src.scoring import word_score


class WordSolver:
    def __init__(self, length: int, first_letter: str):
        self.length = length

        self.word = "*" * self.length
        self.possible_words = []

        self.letters_info = {
            letter: {
                "present": 0,
                "positioned_at": [],
                "not_positioned_at": [],
                "number": -1,
            }
            for letter in LETTERS
        }

        self.letters_info[first_letter] = {
            "present": 1,
            "positioned_at": [0],
            "not_positioned_at": [],
            "number": -1,
        }

        self.turn = 0

        with open("assets/dico.txt") as dico:
            for line in dico:
                if line[0] == first_letter and len(line) == self.length + 1:
                    self.possible_words.append(line[:-1])

        self.filter_possible_words()

    def contains_absent_letter(self, word):
        absent_letters = [
            letter
            for letter, info in self.letters_info.items()
            if info["present"] == -1
        ]
        return any([letter in word for letter in absent_letters])

    def contains_all_present_letters(self, word):
        present_letters = [
            letter for letter, info in self.letters_info.items() if info["present"] == 1
        ]
        return all([letter in word for letter in present_letters])

    def contains_placed_letters(self, word):
        positioned_letters = [
            letter
            for letter in LETTERS
            if len(self.letters_info[letter]["positioned_at"]) > 0
        ]
        for letter in positioned_letters:
            if not set(self.letters_info[letter]["positioned_at"]) <= set(
                find_positions(word, letter)
            ):
                return False
        return True

    def contains_letters_at_wrong_position(self, word):
        for index, letter in enumerate(word):
            if index in self.letters_info[letter]["not_positioned_at"]:
                return True
        return False

    def contains_correct_number_of_letter(self, word):
        quantified_letters = [
            letter for letter in LETTERS if self.letters_info[letter]["number"] != -1
        ]
        for letter in quantified_letters:
            if len(find_positions(word, letter)) != self.letters_info[letter]["number"]:
                return False
        return True

    def filter_possible_words(self):
        self.possible_words = [
            word
            for word in self.possible_words
            if self.contains_all_present_letters(word)
            and not self.contains_absent_letter(word)
            and self.contains_placed_letters(word)
            and not self.contains_letters_at_wrong_position(word)
            and self.contains_correct_number_of_letter(word)
        ]
        self.possible_words = sorted(
            self.possible_words,
            key=cmp_to_key(
                lambda x, y: word_score(y, self.turn) - word_score(x, self.turn)
            ),
        )

    def get_best_words(self):
        score = word_score(self.possible_words[0], self.turn)
        i = 1
        while (
            i < len(self.possible_words)
            and word_score(self.possible_words[i], self.turn) == score
        ):
            i += 1
        return self.possible_words[:i]

    def process_trial(self, word, result):

        # process exact number of letters if possible
        letters = list(set(word))

        for letter in letters:
            indexes = find_positions(word, letter)
            if len(indexes) > 1 and result[indexes[-1]] == "0":
                self.letters_info[letter]["number"] = len(
                    [
                        1
                        for index, score in enumerate(result)
                        if index in indexes and score != 0
                    ]
                )

        for index in range(self.length):
            letter = word[index]
            score = int(result[index])
            info = self.letters_info[letter]

            if score == 0 and info["present"] == 0:
                self.letters_info[letter]["present"] = -1
            elif score == 0 and info["present"] == 1:
                self.letters_info[letter]["not_positioned_at"].append(index)
            elif score == 1:
                self.letters_info[letter]["present"] = 1
                self.letters_info[letter]["not_positioned_at"].append(index)
            elif score == 2:
                self.letters_info[letter]["present"] = 1
                self.letters_info[letter]["positioned_at"].append(index)

            self.letters_info[letter]["positioned_at"] = sorted(
                list(set(self.letters_info[letter]["positioned_at"]))
            )
            self.letters_info[letter]["not_positioned_at"] = sorted(
                list(set(self.letters_info[letter]["not_positioned_at"]))
            )

    def pick_word(self):
        if len(self.possible_words) == 0:
            print("Aucun mot trouvé...")
            return True
        elif len(self.possible_words) == 1:
            print("Le mot est : ", self.possible_words[0])
            return True

        best_words = self.get_best_words()

        if len(best_words) > 1:
            print("Les meilleurs mots à jouer sont :")
            print("\n".join(best_words), "\n")
            played_word = input_word(best_words, self.length)

        elif len(best_words) == 1:
            print("Le meilleur mot à jouer est : ", best_words[0])
            played_word = (
                input_word([], self.length)
                if not proceed("Voulez-vous jouer ce mot ?")
                else best_words[0]
            )

        print(
            "\n",
            "0 = pas présent\n",
            "1 = présent mais pas à la bonne place\n",
            "2 = à la bonne place\n",
        )

        result = input_result(self.length)

        self.process_trial(played_word, result)

        self.filter_possible_words()
        print()
        l = len(self.possible_words)
        pluriel = "s" if l > 1 else ""
        print(f"Encore {l} mot{pluriel} possible{pluriel}.")

        if l <= 10:
            print("Mots possibles : ", ", ".join(self.possible_words))
        print()

        self.turn += 1
        return False
