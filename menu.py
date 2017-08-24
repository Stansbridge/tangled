import pygame
import time
import webbrowser

from enum import Enum

import client
from controls import InputHandler

name_character_min_limit = 1
name_character_max_limit = 10
move_timeout = 0.2
colour_primary = (76,175,80)
colour_accent = (245,0,87)

class Menu():
    def __init__(self, pygame_screen, title, options, offset, parent):
        self.pygame_screen = pygame_screen
        self.title = title
        self.options = options
        self.offset = offset
        self.parent = parent
        
        self.option_selected = self.get_option_by_pos(0)
        self.logo = pygame.transform.scale(pygame.image.load("assets/images/logo.jpg"), (700, 200))
        self.font_path = client.font
        self.fonts = {
            "small": pygame.font.Font(client.font, 45),
            "normal": pygame.font.Font(client.font, 55),
            "large": pygame.font.Font(client.font, 75),
            "heading": pygame.font.Font(client.font, 95),
        }
    
    def render_text(self, font, text, pos = (0, 0), colour = (0,0,0)):
        rendered_text_surface = font.render(text, False, colour)
        self.pygame_screen.blit(rendered_text_surface, pos)
    
    def render_options(self):
        font = self.fonts["large"]
        for index, option in self.options.items():
            colour = (0,0,0)
            if index == self.option_selected:
                index = "> {0}".format(index)
                colour = colour_accent
            self.render_text(font, index, (option["pos"] + self.offset[0], option["pos"] * 55 + self.offset[1]), colour)
    
    def render(self):
        self.render_text(self.fonts["heading"], self.title, (self.offset[0] - 320, 120), (0,0,0,138))
        self.pygame_screen.blit(self.logo,(self.offset[0] - 320, 220))
        self.render_text(self.fonts["small"], self.options[self.option_selected]["desc"], (self.offset[0] - 50, 375), colour_primary)
        self.render_options()
    
    def get_option_by_pos(self, pos):
        for option in self.options:
            if self.options[option]["pos"] == pos:
                return option
    
    def update(self, inputHandler):
        if not inputHandler.inputsTimeout["up"] == move_timeout:
            inputHandler.setTimeout("up", move_timeout)
            inputHandler.setTimeout("down", move_timeout)
        if inputHandler.checkPress("up"):
            self.option_selected = self.get_option_by_pos((self.options[self.option_selected]["pos"] - 1) % len(self.options))
        elif inputHandler.checkPress("down"):
            self.option_selected = self.get_option_by_pos((self.options[self.option_selected]["pos"] + 1) % len(self.options))
        elif inputHandler.checkPress("enter"):
            return self.options[self.option_selected]["action"]
        elif inputHandler.checkPress("back"):
            if self.parent:
                return self.parent
        self.render()
