import pygame 
from pygame import freetype 

pygame.init()
freetype.init()

FONT = freetype.Font(".\\images\\scary_font.ttf", 30)

class Button:
    def __init__(self, text, x_pos, y_pos):
        self.surface, self.rect  = FONT.render(text, "green")
        self.rect.center = (x_pos, y_pos)

    def update(self, screen):
        screen.blit(self.surface, self.rect)


