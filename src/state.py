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
    
    def get_score(self):
        return self.score
    
    def get_words_used(self):
        return self.words_used
    
    def get_level(self):
        return self.level
    
    def inc_score(self, points):
        self.score += points
    
    def use_word(self, word):
        self.words_used.append(word)

    def update_level(self):
        # TODO
        return
    
    def try_word(self, word):
        if word in self.words_used:
            print(f"Already got {word} :)")
        elif word in self.puzzle.get_word_points():
            points = self.puzzle.get_word_points()[word]
            if self.puzzle.is_pangram(word):
                print("***Pangram!***")
            print(f"+{points}")
            self.inc_score(points)
            self.use_word(word)
            self.update_level()
        else:
            print(f"{word} isn't right :(")
    
    def run_game(self):
        print("\nStarting game!\n")
        puzzle = self.get_puzzle()
        letters = puzzle.get_letters()
        while True:
            print(f"\nScore: {self.get_score()}   Level: {self.get_level()}")
            if self.get_words_used():
                print("Words used: ", end = "")
                print(self.get_words_used())
            for letter in letters:
                print(letter, end=" ")
            print()
            
            print("Try a word:")
            word_try = input()
            if (word_try == 'q'):
                print(f"Final score: {self.get_score()}")
                break
            else:
                self.try_word(word_try.upper())