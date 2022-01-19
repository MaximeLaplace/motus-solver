from src.console_utils import clear_console
from src.inputs import input_first_letter, input_length
from src.solver import WordSolver

if __name__ == "__main__":
    clear_console()

    length = input_length()
    first_letter = input_first_letter()

    WordSolver(length, first_letter).solve()
