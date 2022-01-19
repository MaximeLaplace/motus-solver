from src.letters import LETTERS


def _enter_word() -> str:
    word = input("Quel mot choisissez-vous ? ").upper()
    return word


def _enter_result() -> str:
    result = input("Quel est le résultat ? ").upper()
    return result


def _enter_first_letter() -> str:
    letter = input("Première lettre : ")
    return letter


def _enter_length() -> str:
    length = input("Longueur du mot : ")
    return length


def input_word(allowed_words: list[str], length: int) -> str:
    word = _enter_word()

    while len(word) != length or word not in allowed_words and len(allowed_words) != 0:
        if len(word) == 0:
            word = _enter_word()
        if len(word) != length:
            print("Le mot n'est pas de la bonne longueur.")
            word = _enter_word()
        elif word not in allowed_words:
            print("\nLe mot n'est pas dans la liste des meilleurs mots.")
            if proceed("Voulez-vous le choisir quand même ?"):
                return word
            word = _enter_word()

    return word


def input_result(length: int) -> list[int]:
    result = _enter_result()

    while len(result) != length or any([char not in "012" for char in result]):
        if len(result) == 0:
            result = _enter_result()
        if any([char not in "012" for char in result]):
            print("N'utilisez que des 0, des 1 ou des 2 pour exprimer le résultat.")
            result = _enter_result()
        elif len(result) != length:
            print("Ce n'est pas de la bonne longueur.")
            result = _enter_result()

    return [int(s) for s in result]


def input_first_letter() -> str:
    letter = _enter_first_letter()

    while len(letter) != 1 or letter not in LETTERS:
        if len(letter) == 0:
            letter = _enter_first_letter()
        elif len(letter) > 1:
            print("Veuillez n'entrer qu'une seule lettre.")
            letter = _enter_first_letter()
        elif letter not in LETTERS:
            print("Lettre invalide.")
            letter = _enter_first_letter()

    return letter


def input_length() -> int:
    length = _enter_length()
    allowed_lengths = ["5", "6", "7", "8", "9", "10"]

    while len(length) == 0 or len(length) > 2 or length not in allowed_lengths:
        if len(length) == 0:
            length = _enter_length()
        elif length not in allowed_lengths:
            print(
                f'Longueur de mot invalide. Longueurs supportées : {", ".join(allowed_lengths)}'
            )
            length = _enter_length()

    return int(length)


def proceed(message: str):
    user_proceed = input(message.strip() + " (y/n) ").upper()
    return user_proceed == "Y"
