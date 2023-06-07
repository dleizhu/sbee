import math
import random
import pygame

# hexagon
HEX_SIZE = 50
HEX_HEIGHT = HEX_SIZE * 2
HEX_WIDTH = (3 ** 0.5 / 2) * HEX_HEIGHT
HEX_MARGIN = 10

# letter
BLACK = (0, 0, 0)
pygame.font.init()
FONT = pygame.font.SysFont("arial", 24)

class Hexagon:

    def __init__(self, x, y, color, letter):
        self.x = x
        self.y = y
        self.color = color
        self.letter = letter
    
    def set_letter(self, letter):
        self.letter = letter

    def draw(self, window):
        pygame.draw.polygon(window, self.color, self.get_vertices())

        text = FONT.render(self.letter, True, BLACK)
        text_rect = text.get_rect(center=(self.x, self.y))
        window.blit(text, text_rect)
    
    def get_vertices(self):
        vertices = []
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)
            vertex_x = self.x + HEX_SIZE * math.cos(angle_rad)
            vertex_y = self.y + HEX_SIZE * math.sin(angle_rad)
            vertices.append((vertex_x, vertex_y))
        return vertices

    @staticmethod
    def shuffle(surrounding_hexagons, surrounding_letters):
        random.shuffle(surrounding_letters)
        for i in range(len(surrounding_hexagons)):
            hex = surrounding_hexagons[i]
            hex.set_letter(surrounding_letters[i])
        return surrounding_hexagons
    
class CenterHexagon(Hexagon):

    def __init__(self, x, y, color, letter):
        super().__init__(x, y, color, letter)
    
    def draw(self, window):
        super().draw(window)
