from puzzle import Puzzle
from state import State
from hexagon import Hexagon, CenterHexagon, HEX_SIZE, HEX_HEIGHT, HEX_WIDTH, HEX_MARGIN
from button import Button
from datetime import datetime
import argparse
import pygame
import math
import sys

pygame.init()

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREY = (50, 50, 50)
LIGHT_GREY = (200, 200, 200)
YELLOW = (255, 255, 0)

# window
WIDTH = 800
HEIGHT = 600
WINDOW = None
FPS = 60

# font
FONT = pygame.font.SysFont("calibri", 32)

def main():
    parser = argparse.ArgumentParser(description='Sbee')
    parser.add_argument('-c', '--commandline', action='store_true', help='Run the command-line version of the game')

    args = parser.parse_args()

    if args.commandline:
        # Run the command-line version of the game
        command_line_version()
    else:
        graphical_version()

def get_puzzle_num_from_date_string(date_str):
    puzzle_date = datetime.strptime(date_str, "%m/%d/%y")
    first_date_str = "05/09/18"
    first_date = datetime.strptime(first_date_str, "%m/%d/%y")
    return (puzzle_date - first_date).days + 1

def command_line_version():
    """Command-line version"""
    print("\nEnter the date of the sbee to solve!")
    print("Date (MM/DD/YY): ", end = "")
    puzzle_date_str = input()
    puzzle_num = get_puzzle_num_from_date_string(puzzle_date_str)
    puzzle = Puzzle(puzzle_num)
    state = State(puzzle)
    state.run_game()

def delete_last_letter(word):
    print("deleting")
    if len(word[0]) > 0:
        word[0] = word[0][:-1]
        print(f"word is now {word[0]}")

def graphical_version():
    global WINDOW
    
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("sbee")
    
    # Initialize game state
    date_str = startup_screen()
    puzzle_num = get_puzzle_num_from_date_string(date_str)
    puzzle = Puzzle(puzzle_num)
    state = State(puzzle)

    # Initialize letters
    letters = puzzle.get_letters()
    hexagons = []
    center_hexagon = CenterHexagon(WIDTH // 2, HEIGHT // 2, YELLOW, letters[0])
    hexagons.append(center_hexagon)
    for i in range(6):
        angle_deg = 60 * i + 30 
        angle_rad = math.radians(angle_deg)
        hex_x = center_hexagon.x + (2 * HEX_SIZE + HEX_MARGIN) * math.cos(angle_rad)
        hex_y = center_hexagon.y + (2 * HEX_SIZE + HEX_MARGIN) * math.sin(angle_rad)
        hexagons.append(Hexagon(hex_x, hex_y, LIGHT_GREY, letters[i + 1]))
    
    # Initialize shuffle button
    shuffle_width = 120
    shuffle_height = 40
    shuffle_x = WIDTH // 2 - shuffle_width - 8
    shuffle_y = HEIGHT - 60
    shuffle_button = Button(shuffle_x, shuffle_y, shuffle_width, shuffle_height,
                            "shuffle", YELLOW, LIGHT_GREY, FONT, BLACK, Hexagon.shuffle)

    # Initialize delete button
    delete_width = 120
    delete_height = 40
    delete_x = WIDTH // 2 + 8
    delete_y = HEIGHT - 60
    delete_button = Button(delete_x, delete_y, delete_width, delete_height,
                        "delete", LIGHT_GREY, LIGHT_GREY, FONT, BLACK, delete_last_letter)


    # Initialize word attempt
    word = ""
    word_box = pygame.Rect(0, 0, WIDTH, 100)
    word_font = pygame.font.SysFont("calibri", 32)

    # Initialize feedback variables
    feedback_text = ""
    feedback_timer = 0

    # Main game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        WINDOW.fill(DARK_GREY)
        score = state.get_score()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for hexagon in hexagons:
                    if pygame.Rect(hexagon.get_x() - HEX_SIZE, hexagon.get_y() - HEX_SIZE,
                                   HEX_WIDTH, HEX_HEIGHT).collidepoint(mouse_pos):
                        print("hex clicked")
                        word += hexagon.get_letter()
                shuffle_button.handle_event(event, hexagons[1:], letters[1:])
                word_container = [word]
                delete_button.handle_event(event, word_container)
                word = word_container[0]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    word = word[:-1] # delete last character
                elif event.key == pygame.K_RETURN:
                    try_score, is_pangram = state.try_word(word)
                    # Display feedback text
                    feedback_text = ""
                    if try_score == 0:
                        feedback_text = f"Already got {word} :)"
                    elif try_score > 0:
                        feedback_text = f"+{try_score}!"
                        if is_pangram:
                            feedback_text = f"***Pangram! +{try_score}!***"
                    elif try_score < 0:
                        feedback_text = f"{word} isn't correct :("

                    feedback_timer = FPS  # 1 seconds
                    word = ""
                    score = state.get_score()
                    print(state.get_score())
                else:
                    word += event.unicode.upper() # Add pressed key to word attempt
        
        # Draw word
        word_surface = word_font.render(word, True, WHITE)
        word_rect = word_surface.get_rect(center=(WIDTH // 2, word_box.y + word_box.height // 2))
        pygame.draw.rect(WINDOW, DARK_GREY, word_box)
        WINDOW.blit(word_surface, word_rect)

        # Draw hexagons
        for hexagon in hexagons:
            hexagon.draw(WINDOW)

        # Draw shuffle button
        shuffle_button.draw(WINDOW)

        # Draw delete button
        delete_button.draw(WINDOW)

        # Draw feedback text
        if feedback_timer > 0:
            feedback_surface = FONT.render(feedback_text, True, WHITE)
            feedback_rect = feedback_surface.get_rect(topright=(WIDTH - 10, 10))
            WINDOW.blit(feedback_surface, feedback_rect)
            feedback_timer -= 1
        
        # Draw score
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(topleft=(10, 10))
        WINDOW.blit(score_text, score_rect)
        
        pygame.display.flip()

    pygame.quit()
                

def startup_screen():
    text = ""
    input_box_width = max(200, FONT.size(text)[0] + 10)
    input_box_height = 40
    input_box = pygame.Rect((WIDTH - input_box_width) // 2, 250, input_box_width, input_box_height)
    active = False

    # game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if text:
                            print("Date entered: " + text)
                            return text
                            running = False
                        
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        
        # Clear screen
        WINDOW.fill(WHITE)

        # Render text
        text_surface = FONT.render("Enter the date of the sbee to solve!", True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 200))
        WINDOW.blit(text_surface, text_rect)

        # Render input box
        pygame.draw.rect(WINDOW, BLACK, input_box, 2)
        input_text = FONT.render(text, True, BLACK)
        WINDOW.blit(input_text, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()

    
if __name__ == "__main__":
    main()