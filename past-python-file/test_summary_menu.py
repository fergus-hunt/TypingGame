import pygame
from pygame import freetype
from button import Button
from menu import Menu


pygame.init()
freetype.init()

FONT = freetype.Font(".\\images\\scary_font.ttf", 50)
HEIGHT = 965
WIDTH = 1285

class TestSummaryMenu(Menu):
    def __init__(self, wpm, errors):
        Menu.__init__(self)
        self.button_dict["TypingTest"] = Button("Play Again", WIDTH/2, (HEIGHT)/4)
        self.title_array.append(Button(f"WPM : {wpm}", WIDTH / 2, (HEIGHT/2)))
        self.title_array.append(Button(f"ERRORS : {errors}", WIDTH / 2, (HEIGHT*3)/4))

        

# class TestSummaryMenu():
#     """class to show the post text menu screen"""

#     def __init__(self, wpm, errors):
#         self.wpm = wpm
#         self.errors = errors
#         self.wpm_rect.center = (WIDTH / 2, (HEIGHT * 2) / 3)
#         self.error_image, self.error_rect = FONT.render("ERRORS : " + str(self.errors), 'red')
#         self.error_rect.center = (WIDTH / 2, HEIGHT / 3)

#     def main_loop(self, screen, background, clock):
#         """The main pygame loop, shows user WPM, errors and option to return to main menu"""
#         while True:
#             clock.tick(60)
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_SPACE:
#                         return 'StartMenu'

#             screen.fill('black')
#             screen.blit(background, (0, 0))
#             screen.blit(self.error_image, self.error_rect)
#             screen.blit(self.wpm_image, self.wpm_rect)
#             pygame.display.update()





