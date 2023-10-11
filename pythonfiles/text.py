import requests, lorem, pygame, time, pandas, random, string
import pygame.freetype
pygame.init()

FONT = pygame.freetype.Font(None, 35)
FONT.origin = True 

API_TOKEN = "TfYf279t3YTCMftnoaNsg23Zbi13H5xblBHvu4yw"
URL = f"https://quotes.rest/qod.json?api_key={API_TOKEN}"


class Text(pygame.sprite.Sprite): 
    """renders new text, takes user key presses, analyses data"""
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.text= self.generate_text()
        self.rect = FONT.get_rect(self.text)
        self.metrics = FONT.get_metrics(self.text)
        self.next_key = 0
        self.is_complete = False
        self.characters_unicode = [character for character in self.text]
        self.characters_completed = ["Na" for index in range(len(self.characters_unicode))]
        self.image = pygame.Surface(self.rect.size)
        self.image.set_colorkey((255, 0, 255))
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
        # def get_text(self): 
        # pd = pandas.read_csv('database\data.csv')
        # text_index = random.randint(0, len(pd)-1)
        # text = pd.loc[text_index]
        # text = "jdfgalkafd;ajlsfsdf"
        # return text

    # def reset(self):
    #     self.text= self.get_text()
    #     self.next_key = 0
    #     self.is_complete = False
    #     self.characters_unicode = [character for character in self.text]
    #     self.characters_completed = ['Na' for index in range(len(self.characters_unicode))]
    #     self.rect = FONT.get_rect(self.text)
    #     self.metrics = FONT.get_metrics(self.text)
    
    # def register_key(self, event):
    #     if self.next_key == len(self.characters_completed):
    #         self.is_complete = True
    #     else: 
    #         if event.key == pygame.K_BACKSPACE: 
    #             self.next_key -= 1
    #             self.characters_completed[self.next_key] = "Na"
    #         elif event.unicode == self.characters_unicode[self.next_key]: 
    #             self.characters_completed[self.next_key] = True
    #             self.next_key += 1
    #         elif event.unicode != '': 
    #             self.characters_completed[self.next_key] = False
    #             self.next_key += 1
        
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


    def calculating_wpm(self): 
        total_word = len(self.text.split())
        total_time = (self.end_time - self.start_time) / 60
        return round(total_word / (total_time), 2)

    def calculate_errors(self): 
        sum = 0
        for i in self.characters_completed: 
            if i == False:
                sum += 1
        return sum
