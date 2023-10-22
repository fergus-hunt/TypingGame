import pygame 

from pygame import freetype 

FONT = freetype.Font(None, 100)
FONT.origin = True


class Alert(): 
    def __init__(self):
        self.rect = FONT.get_rect("ROUND 0")
        self.baseline = self.rect.y
        self.image = pygame.Surface(self.rect.size)
        self.rect.center = (500, 400)
        self.count = 0

    def refresh(self): 
        if self.count > 10: 
            self.count = -1
            self.rect.center = (2000, 0)
        elif self.count >= 0: 
            self.count += 1

                

    def new_round(self, round): 
        text = f"ROUND {round}"
        self.rect = FONT.get_rect(text)
        self.image = pygame.Surface(self.rect.size)
        self.baseline = self.rect.y
        self.rect.center = (500, 400)
        FONT.render_to(self.image, (0, self.baseline), text, 'blue')