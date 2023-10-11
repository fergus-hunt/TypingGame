import pygame, pandas

pygame.init() 

class Student(pygame.sprite.Sprite):
     
    def __init__(self, image, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image), (50, 50))
        self.rect =self.image.get_rect()
        self.rect.center = (x, y)

    