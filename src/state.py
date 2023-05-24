from puzzle import Puzzle
class State:
    
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
        percent = self.score / sum(self.puzzle.get_word_points().values())
        if percent >= 1:
            self.level = "Queen Bee"
        elif percent >= 0.7:
            self.level = "Genius"
        elif percent >= 0.5:
            self.level = "Amazing"
        elif percent >= 0.4:
            self.level = "Great"
        elif percent >= 0.25:
            self.level = "Nice"
        elif percent >= 0.15:
            self.level = "Solid"
        elif percent >= 0.08:
            self.level = "Good"
        elif percent >= 0.05:
            self.level = "Moving Up"
        elif percent >= 0.02:
            self.level = "Good Start"
    
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
            # if self.get_words_used():
            #     print("Words used: ", end = "")
            #     print(self.get_words_used())
            print("*"*30)
            for letter in letters:
                print(letter, end=" ")
            print()
            
            print("Try a word:")
            word_try = input()
            if (word_try == 'q'):
                print("*"*30)
                print(f"Final score: {self.score}     Final level: {self.level}\n\n")
                break
            else:
                self.try_word(word_try.upper())
            
            if self.level == "Queen Bee":
                print("You got all the words!")
                print("*"*30)
                print(f"Final score: {self.score}     Final level: {self.level}\n\n")
                break