import pygame
import json
from text import Text

pygame.init()
class MainCharacter(pygame.sprite.Sprite): 
    def __init__(self,node, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("./images/student-images/Pink_Monster.png"), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.node = node
        self.is_moving = False
        self.next_positions = []  # implementing a stack

    def reposition(self, node, position): 
        self.node = node 
        self.rect.center = position

    def update(self): 
        if self.is_moving: 
            if len(self.next_positions) == 0: 
                self.is_moving = False
            else: 
                self.rect.center = self.next_positions[0]
                del self.next_positions[0]
        
        

