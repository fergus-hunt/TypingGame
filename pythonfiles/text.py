import requests, lorem, pygame, time, pandas, random, string
import pygame.freetype
pygame.init()

FONT = pygame.freetype.Font(None, 50)
FONT.origin = True 

API_TOKEN = "***REMOVED***"
URL = f"https://quotes.rest/qod.json?api_key={API_TOKEN}"


class Text(pygame.sprite.Sprite): 
    """renders new text, takes user key presses, analyses data"""
    def __init__(self, x, y, node) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.text= self.generate_text()
        self.rect = FONT.get_rect(self.text)
        self.metrics = FONT.get_metrics(self.text)
        self.next_key = 0
        self.characters_unicode = [character for character in self.text]
        self.characters_completed = ["Na" for index in range(len(self.characters_unicode))]
        self.image = pygame.Surface(self.rect.size)
        self.image.set_colorkey((255, 0, 255))
        self.node = node
        self.baseline = self.rect.y
        self.rect.center = (x, y)


    def update(self): 
        self.rendering_text()

    def characters_reset(self): 
        for index in range(len(self.characters_completed)):
            self.characters_completed[index] = "Na"

    def generate_text(self): 
        text = ""
        for i in range(2):
            num = random.randint(0, 25) 
            text += string.ascii_lowercase[num]
        return text
        
    def rendering_text(self):
        x_val = 0
        self.image.fill((255, 0, 255))
        #coudl make quicker here. 
        for index, metric in zip(range(len(self.characters_unicode)), self.metrics):      
            character = self.characters_unicode[index] 
            if self.characters_completed[index] == "Na":
                FONT.render_to(self.image, (x_val, self.baseline), character, 'white')
                x_val += metric[4]
            elif self.characters_completed[index]: 
                FONT.render_to(self.image, (x_val, self.baseline), character, "green")
                x_val += metric[4]
            else:
                FONT.render_to(self.image, (x_val, self.baseline),character, "red")
                x_val += metric[4]

