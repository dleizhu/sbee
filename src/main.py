from puzzle import Puzzle
from state import State

def main():
    # print("Enter the puzzle number, or 0 for today's sbee!\n")
    # puzzle_num = int(input())
    # puzzle = Puzzle(puzzle_num)
    # puzzle.print()
    state = State()
    state.get_puzzle().print()
    

if __name__ == "__main__":
    main()