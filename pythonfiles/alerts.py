import pygame 

from pygame import freetype 

FONT = freetype.Font(None, 100)
HEIGHT = 965
WIDTH = 1285

class Alert(): 
    def __init__(self):
        self.rect = FONT.get_rect("ROUND 0")
        self.image = pygame.Surface(self.rect.size)
        self.rect.center = (WIDTH/2, HEIGHT/5)
        self.count = 0

    def refresh(self): 
        if self.count > 10: 
            self.count = -1
            self.rect.center = (2000, 0)
        elif self.count >= 0: 
            self.count += 1

                

    def new_round(self, round): 
        text = f"ROUND {round}"
        self.image, self.rect = FONT.render(text,"blue")
        # self.image = pygame.Surface(self.rect.size) 
        self.rect.center = (WIDTH/2, HEIGHT/5)
        # FONT.render_to(self.image, (0, 0), text, 'blue')