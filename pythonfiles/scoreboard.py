import pygame
from pygame import freetype

pygame.init()
freetype.init()

# FONT = freetype.Font(".\\images\\scary_font.ttf", 50)
HEIGHT = 965
WIDTH = 1285


class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self, feature_control):
        pygame.sprite.Sprite.__init__(self)
        self.feature_control = feature_control
        self.score = 000
        self.score_increment = 10
        self.image, self.rect = self.feature_control.font_dynamic.render(f"SCORE : {self.score}", self.feature_control.colour)
        self.rect.center = (WIDTH / 2, 25)

    def update_scoreboard(self):
        """updates the user's score and keeps track."""
        self.score += self.score_increment
        self.image, self.rect = self.feature_control.font_dynamic.render(f"SCORE : {self.score}", self.feature_control.colour)
        self.rect.center = (WIDTH / 2, 25)
