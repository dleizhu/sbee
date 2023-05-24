from puzzle import Puzzle
from state import State

def main():
    print("\nEnter the puzzle number, or 0 for today's sbee!")
    puzzle_num = int(input())
    puzzle = Puzzle(puzzle_num)
    state = State(puzzle)
    state.run_game()
    
if __name__ == "__main__":
    main()