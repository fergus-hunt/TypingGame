import pygame 

from pygame import freetype 

FONT = freetype.Font(None, 100)


class Alert(pygame.sprite.Sprite): 
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.rect.Rect(0, 2000, 0, 0)
        self.image = pygame.Surface(self.rect.size)
        self.is_alert = False
        self.count = 0

    def update(self): 
        if self.is_alert: 
            if self.count > 10: 
                self.count = 0
                self.is_alert = False
            else: 
                self.count += 1
        else: 
            self.rect = pygame.rect.Rect(0, 2000, 0, 0)
            self.image = pygame.Surface(self.rect.size)

    def new_round(self, round): 
        self.is_alert = True
        text = f"ROUND {round}"
        self.rect = FONT.get_rect(text)
        self.image = pygame.Surface(self.rect.size)
        FONT.render_to(self.image, (0, 0), text, 'blue')