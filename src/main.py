from puzzle import Puzzle
from state import State
from datetime import datetime
import argparse
import pygame
import sys

pygame.init()

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# window
WIDTH = 800
HEIGHT = 600
WINDOW = None

# font
FONT = pygame.font.SysFont("arial", 32)

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

def graphical_version():
    global WINDOW
    
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("sbee")
    
    startup_screen()
    print("next screen") # TODO: remove
    
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
                            # TODO logic
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