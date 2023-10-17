import pygame

from pygame import freetype
pygame.init()

FONT = freetype.Font(None, 50)
FONT.origin = True  

class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self, x, y): 
        pygame.sprite.Sprite().__init__()
        self.score = 0 
        self.image = pygame.transform.scale(pygame.image.load("SCOREBOARD IMAGE"), (200, 100))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self): 
        pass 

    def render_text(self): 
        # metrics = FONT.get_metrics(str(self.score))
        baseline = self.rect.y
        FONT.render_to(self.image, (0, baseline), str(self.score), "blue")

