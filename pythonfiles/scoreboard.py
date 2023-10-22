import pygame

from pygame import freetype
pygame.init()

FONT = freetype.Font(None, 50)
HEIGHT = 965
WIDTH = 1285
 


class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)
        self.score = 000 
        self.score_increment = 10
        self.image, self.rect = FONT.render(str(self.score), "blue")
        self.rect.center = (WIDTH/2, 25)

    def update(self): 
        # self.render_text()
        pass 

    def update_score(self): 
        self.score += self.score_increment
        self.image, self.rect = FONT.render(str(self.score), "blue")
        self.rect.center = (WIDTH/2, 25)


    # def render_text(self): 
    #     # metrics = FONT.get_metrics(str(self.score))
