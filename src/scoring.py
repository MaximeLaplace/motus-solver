from src.letters import LETTER_SCORES

LETTER_FREQUENCY_WEIGHT = 1
LETTER_DIVERSITY_WEIGHT = 3


def word_score(word: str) -> int:
    letter_frequency_score = sum([LETTER_SCORES[letter] for letter in word])
    letter_diversity_score = len(list(set(word)))

    return (
        LETTER_FREQUENCY_WEIGHT * letter_frequency_score
        + (LETTER_DIVERSITY_WEIGHT) * letter_diversity_score
    )
