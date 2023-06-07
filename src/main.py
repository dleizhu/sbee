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
    shuffle_button = Button(WIDTH // 2 - shuffle_width // 2, HEIGHT - 60, shuffle_width, shuffle_height,
                            "shuffle", YELLOW, LIGHT_GREY, FONT, BLACK, lambda: Hexagon.shuffle(hexagons[1:], letters[1:]))
    
    running = True
    while running:
        WINDOW.fill(DARK_GREY)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for hexagon in hexagons:
                    if pygame.Rect(hexagon.x - HEX_SIZE, hexagon.y - HEX_SIZE,
                                   HEX_WIDTH, HEX_HEIGHT).collidepoint(mouse_pos):
                        print("hex clicked") # TODO: fill word box
                    shuffle_button.handle_event(event)
            elif event.type == pygame.KEYDOWN:
                # TODO: allow typing
                continue
        
        for hexagon in hexagons:
            hexagon.draw(WINDOW)
        shuffle_button.draw(WINDOW)
        
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