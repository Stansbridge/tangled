import pygame
import time
import webbrowser

from enum import Enum

import client
from controls import InputHandler
from resources import *

move_timeout = 0.2

class Menu():
    def __init__(self, pygame_screen, title, options, offset, parent):
        self.pygame_screen = pygame_screen
        self.title = title
        self.options = options
        self.offset = offset
        self.parent = parent
        
        self.option_selected = self.get_option_by_pos(0)
        self.logo = pygame.transform.scale(pygame.image.load("assets/images/logo.jpg"), (700, 200))
    
    def option_add(self, option, desc, action, pos):
        self.options[option] = {"desc":desc, "action":action, "pos":pos}
    
    def render_text(self, font, text, pos = (0, 0), colour = colours["black"]):
        rendered_text_surface = font.render(text, False, colour)
        self.pygame_screen.blit(rendered_text_surface, pos)
    
    def render_options(self):
        for index, option in self.options.items():
            colour = colours["black"]
            if index == self.option_selected:
                index = "> {0}".format(index)
                colour = colours["accent"]
            self.render_text(fonts["large"], index, (option["pos"] + self.offset[0], option["pos"] * 55 + self.offset[1]), colour)
    
    def render(self):
        self.render_text(fonts["heading"], self.title, (self.offset[0] - 320, 120), colours["black"])
        self.pygame_screen.blit(self.logo,(self.offset[0] - 320, 220))
        self.render_text(fonts["small"], self.options[self.option_selected]["desc"], (self.offset[0] - 50, 375), colours["primary"])
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

class MenuInput():
    def __init__(self, pygame_screen, title, desc, offset, parent, limit, default, action):
        self.pygame_screen = pygame_screen
        self.title = title
        self.desc = desc
        self.offset = offset
        self.parent = parent
        self.limit = limit
        self.action = action
        
        self.ticker = 0.0
        self.char_name = default
        self.logo = pygame.transform.scale(pygame.image.load("assets/images/logo.jpg"), (700, 200))
    
    def option_add(self, option, desc, action, pos):
        self.options[option] = {"desc":desc, "action":action, "pos":pos}
    
    def render_text(self, font, text, pos = (0, 0), colour = colours["black"]):
        rendered_text_surface = font.render(text, False, colour)
        self.pygame_screen.blit(rendered_text_surface, pos)
    
    def render(self):
        self.ticker += 2
        self.ticker %= 100
        self.render_text(fonts["heading"], self.title, (self.offset[0] - 320, 120), colours["black"])
        self.pygame_screen.blit(self.logo,(self.offset[0] - 320, 220))
        #self.render_text(fonts["large"], self.desc, (self.offset[0] - 125, self.offset[1]))
        if self.ticker > 25 and len(self.char_name) < self.limit[1]:
            self.render_text(fonts["large"], self.desc + self.char_name + '_', (self.offset[0], self.offset[1]))
        else:
            self.render_text(fonts["large"], self.desc + self.char_name, (self.offset[0], self.offset[1]))
    
    def get_option_by_pos(self, pos):
        for option in self.options:
            if self.options[option]["pos"] == pos:
                return option
    
    def update(self, inputHandler, event):
        if event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_BACKSPACE:
                self.char_name = self.char_name[:-1]
            elif event.key < 123 and event.key != 13 and len(self.char_name) < self.limit[1]:
                self.char_name += chr(event.key)
        if not any(pygame.key.get_pressed()[key] and not key == 13 for key in range(0,124)):
            if inputHandler.checkPress("enter") and len(self.char_name) > self.limit[0]:
                return self.action
            elif inputHandler.checkPress("back"):
                if self.parent:
                    return self.parent
        #self.render()