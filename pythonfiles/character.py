import pygame
from pygame.sprite import _Group

class MainCharacter(pygame.sprite.Sprite): 
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)
        