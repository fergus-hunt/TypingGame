import pygame

from pygame import freetype
pygame.init()

FONT = freetype.Font(None, 50)
# FONT.origin = True  

class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = x, y
        self.score = 000 
        self.score_increment = 10
        self.rect = FONT.get_rect(str(self.score))
        self.image = pygame.Surface(size = self.rect.size)
        self.rect.x, self.rect.y = x, y
        

    def update(self): 
        self.render_text()
        pass 

    def update_score(self): 
        self.score += self.score_increment

    def render_text(self): 
        # metrics = FONT.get_metrics(str(self.score))
        self.rect = FONT.get_rect(str(self.score))
        self.image = pygame.Surface(size = self.rect.size)
        self.rect.x, self.rect.y = self.x, self.y
        FONT.render_to(self.image, (0, 0), str(self.score), "blue")

