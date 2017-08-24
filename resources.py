import pygame

pygame.font.init()

colours = {"white":pygame.Color(255,255,255),
        "black":pygame.Color(0,0,0),
        "red":pygame.Color(244,67,54),
        "blue":pygame.Color(33,150,243),
        "primary":pygame.Color(76,175,80),
        "accent":pygame.Color(245,0,87)}

font = "assets/fonts/alterebro-pixel-font.ttf"
fonts = {"small": pygame.font.Font(font, 45),
        "normal": pygame.font.Font(font, 55),
        "large": pygame.font.Font(font, 75),
        "heading": pygame.font.Font(font, 95)}
