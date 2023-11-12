import pygame
from pygame import freetype

pygame.init()
freetype.init()

FONT = freetype.Font(None, 50)
HEIGHT = 965
WIDTH = 1285

class TestSummaryMenu():
    """class to show the post text menu screen"""

    def __init__(self, wpm, errors):
        self.wpm = wpm
        self.errors = errors
        self.wpm_image, self.wpm_rect = FONT.render("WORDS PER MINUTE : " + str(self.wpm), 'blue')
        self.wpm_rect.center = (WIDTH / 2, (HEIGHT * 2) / 3)
        self.error_image, self.error_rect = FONT.render("ERRORS : " + str(self.errors), 'red')
        self.error_rect.center = (WIDTH / 2, HEIGHT / 3)

    def main_loop(self, screen, background, clock):
        """The main pygame loop, shows user WPM, errors and option to return to main menu"""
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return 'StartMenu'

            screen.fill('black')
            screen.blit(background, (0, 0))
            screen.blit(self.error_image, self.error_rect)
            screen.blit(self.wpm_image, self.wpm_rect)
            pygame.display.update()





