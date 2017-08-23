import pygame
import time

from enum import Enum

import client

name_character_min_limit = 1
name_character_max_limit = 10

class Screen():
    def __init__(self, pygame_screen):
        self.pygame_screen = pygame_screen
        self.font_path = client.font
        self.fonts = {
            'small': pygame.font.Font(client.font, 45),
            'normal': pygame.font.Font(client.font, 55),
            'large': pygame.font.Font(client.font, 75),
            'heading': pygame.font.Font(client.font, 95),
        }


class Menu(Screen):
    def __init__(self, title, options):
        self.title = title
        self.options = options
        self.option_selected = 0
    
    def render_text(self, font, text, pos = (0, 0), colour = (0, 0, 0)):
        rendered_text_surface = font.render(text, False, colour)
        self.pygame_screen.blit(rendered_text_surface, pos)
    
    def render(self):
        self.pygame_screen.blit(self.logo,(offset[0] - 320, 220))
        #DO THE THING
