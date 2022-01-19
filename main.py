from src.inputs import input_first_letter, input_length
from src.solver import WordSolver


def solve():
    length = input_length()
    first_letter = input_first_letter()

    solver = WordSolver(length, first_letter)

    print("\n", "#" * 30, "\n")

    solved = False
    while not solved:
        solved = solver.pick_word()


if __name__ == "__main__":
    solve()
