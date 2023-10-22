import requests, lorem, pygame, time, pandas, random
import pygame.freetype
pygame.init()

FONT = pygame.freetype.Font(None, 35)
FONT.origin = True 

class TypeTestText(): 
    """renders new text, takes user key presses, analyses data"""
    def __init__(self) -> None:
        self.text= self.get_text()
        self.next_key = 0
        self.is_complete = False
        self.characters_unicode = [character for character in self.text]
        self.characters_completed = ['Na' for index in range(len(self.characters_unicode))]
        self.rect = FONT.get_rect(self.text)
        self.metrics = FONT.get_metrics(self.text)

    def get_text(self): 
        pd = pandas.read_csv('database\data.csv')
        text_index = random.randint(0, len(pd)-1)
        text = pd.loc[text_index]
        return text.passage

    def reset(self):
        self.text= self.get_text()
        self.next_key = 0
        self.is_complete = False
        self.characters_unicode = [character for character in self.text]
        self.characters_completed = ['Na' for index in range(len(self.characters_unicode))]
        self.rect = FONT.get_rect(self.text)
        self.metrics = FONT.get_metrics(self.text)
    
    def register_key(self, event):
        if self.next_key == len(self.characters_completed):
            self.is_complete = True
        else: 
            if event.key == pygame.K_BACKSPACE: 
                self.next_key -= 1
                self.characters_completed[self.next_key] = 'Na'
            elif event.unicode == self.characters_unicode[self.next_key]: 
                self.characters_completed[self.next_key] = True
                self.next_key += 1
            elif event.unicode != '': 
                self.characters_completed[self.next_key] = False
                self.next_key += 1
        

    def rendering_text(self):
        x_val = 0
        baseline = self.rect.y 
        text_surface = pygame.Surface(self.rect.size)
        completed = -550
        #coudl make quicker here. 
        for index, metric in zip(range(len(self.characters_unicode)), self.metrics):      
            character = self.characters_unicode[index] 
            if self.characters_completed[index] == "Na": 
                FONT.render_to(text_surface,(x_val, baseline), character, 'white')
                x_val += metric[4]
            elif self.characters_completed[index]: 
                FONT.render_to(text_surface, (x_val, baseline), character, "green")
                x_val += metric[4]
                completed += metric[4]
            elif not self.characters_completed[index]: 
                FONT.render_to(text_surface, (x_val, baseline),character, "red")
                x_val += metric[4]
                completed += metric[4]
        self.rect.x = 0-completed

        self.surface= text_surface

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
