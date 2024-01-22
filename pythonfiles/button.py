import pygame 
from pygame import freetype 

pygame.init()
freetype.init()

# FONT = freetype.Font(".\\images\\scary_font.ttf", 50)

class MenuFeature: 
    def __init__(self, text, x_pos, y_pos, feature_control): # Class constructor 
        self.surface, self.rect  = feature_control.font_dynamic.render(text, feature_control.colour) # Enable feature to be displayed on screen 
        
        self.rect.center = (x_pos, y_pos) # Placing button in correct position. 

    def update(self, screen): # places feature ontop of background image. 
        pygame.draw.rect(screen, 'black', self.rect)
        screen.blit(self.surface, self.rect)


