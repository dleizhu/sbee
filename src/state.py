from puzzle import Puzzle
class State:
    levels = ["Beginner", "Good Start", "Moving Up", "Good", "Solid", "Nice",
              "Great", "Amazing", "Genius"]
    def __init__(self, puzzle=Puzzle()):
        self.puzzle = puzzle
        self.score = 0
        self.words_used = []
        self.level = "Beginner"
    
    def get_puzzle(self):
        return self.puzzle