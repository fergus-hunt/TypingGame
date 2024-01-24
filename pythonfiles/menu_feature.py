import pygame 

pygame.init() # initialising pygame modules \\

# FONT = freetype.Font(".\\images\\scary_font.ttf", 50)

class MenuFeature: 
    def __init__(self, text, x_pos, y_pos, feature_control): # Class constructor
        """text= what's displayed on feature, (xpos, ypos) = centering position, feature control is class storing user features"""
        self.surface, self.rect  = feature_control.font_dynamic.render(text, feature_control.colour) # Enable feature to be displayed on screen 
        self.rect.center = (x_pos, y_pos) # Placing button in correct position. 

    def update(self, screen): # function to render each feature ontop of screen
        pygame.draw.rect(screen, 'black', self.rect) # positioning feature background
        screen.blit(self.surface, self.rect) # rendering feature text ontop of feature background


