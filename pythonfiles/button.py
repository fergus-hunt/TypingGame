import pygame 
from pygame import freetype 

pygame.init()
freetype.init()

# FONT = freetype.Font(".\\images\\scary_font.ttf", 50)

class Button:
    def __init__(self, text, x_pos, y_pos, feature_control):
        self.surface, self.rect  = feature_control.font_dynamic.render(text, feature_control.colour)
        
        self.rect.center = (x_pos, y_pos)

    def update(self, screen):
        pygame.draw.rect(screen, 'black', self.rect)
        screen.blit(self.surface, self.rect)


