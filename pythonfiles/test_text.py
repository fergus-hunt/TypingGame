import pygame
import pygame.freetype
import requests
import time

pygame.init()
pygame.mixer.init()

# FONT = pygame.freetype.Font(".\\images\\scary_font.ttf", 50)
# FONT.origin = True
HEIGHT = 965
WIDTH = 1285

URL = f"https://api.quotable.io/quotes/random"


class TestText:
    """renders new text, takes user key presses, analyses data"""

    def __init__(self, feature_control) -> None:
        self.feature_control = feature_control
        # self.noise = pygame.mixer.Sound("images/typewriter.wav")
        self.text = self.get_text()
        self.next_key = 0
        self.is_complete = False
        self.characters_unicode = [character for character in self.text]
        self.characters_completed = ['Na' for index in range(len(self.characters_unicode))]
        self.rect = self.feature_control.font_static.get_rect(self.text)
        self.baseline = self.rect.y
        self.metrics = self.feature_control.font_static.get_metrics(self.text)
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def get_text(self):
        response = requests.get(URL)
        response.raise_for_status()
        self.feature_control.music.play()

        return response.json()[0]["content"]

    def reset(self):
        self.text = self.get_text()
        self.next_key = 0
        self.is_complete = False
        self.characters_unicode = [character for character in self.text]
        self.characters_completed = ['Na' for index in range(len(self.characters_unicode))]
        self.rect = self.feature_control.font_static.get_rect(self.text)
        self.metrics = self.feature_control.font_static.get_metrics(self.text)

    def register_key(self, event):
        self.feature_control.keysound.play()
        if self.next_key == len(self.characters_completed):
            self.end_time = time.time()
            self.feature_control.music.stop()
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
        text_surface = pygame.Surface(self.rect.size)
        completed = -550
        # coudl make quicker here.
        for index, metric in zip(range(len(self.characters_unicode)), self.metrics):
            character = self.characters_unicode[index]
            if not self.characters_completed[index]:
                self.feature_control.font_static.render_to(text_surface, (x_val, self.baseline), character, "red")
                x_val += metric[4]
                completed += metric[4]
            elif (not self.characters_completed[index-1] == "Na") and self.characters_completed[index] == "Na" and index != 0: 
                self.feature_control.font_static.render_to(text_surface, (x_val, self.baseline), character, "blue")
                x_val += metric[4] 
            elif self.characters_completed[index] == "Na":
                self.feature_control.font_static.render_to(text_surface, (x_val, self.baseline), character, 'white')
                x_val += metric[4]
            elif self.characters_completed[index]:
                self.feature_control.font_static.render_to(text_surface, (x_val, self.baseline), character, "green")
                x_val += metric[4]
                completed += metric[4]

        self.rect.x = 0 - completed
        self.surface = text_surface

    def calculating_wpm(self, start_time, end_time):
        total_word = len(self.text.split())
        total_time = (end_time - start_time) / 60
        return round(total_word / (total_time), 2)

    def calculate_errors(self):
        sum = 0
        for i in self.characters_completed:
            if not i:
                sum += 1
        return sum
