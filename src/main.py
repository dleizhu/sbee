from puzzle import Puzzle
from state import State
from datetime import datetime

def main():
    print("\nEnter the date of the sbee to solve!")
    print("Date (MM/DD/YY): ", end = "")
    puzzle_date_str = input()
    puzzle_date = datetime.strptime(puzzle_date_str, "%m/%d/%y")
    first_date_str = "05/09/18"
    first_date = datetime.strptime(first_date_str, "%m/%d/%y")
    puzzle_num = (puzzle_date - first_date).days + 1
    puzzle = Puzzle(puzzle_num)
    state = State(puzzle)
    state.run_game()
    
if __name__ == "__main__":
    main()