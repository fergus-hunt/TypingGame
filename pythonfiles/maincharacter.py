import pygame
import json
from text import Text

pygame.init()
class MainCharacter(pygame.sprite.Sprite): 
    def __init__(self, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("./images/student-images/Pink_Monster.png"), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


