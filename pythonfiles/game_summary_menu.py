# import pygame 
# from pygame import freetype
from button import Button
from menu import Menu

HEIGHT = 965
WIDTH = 1285


class GameSummaryMenu(Menu):
    def __init__(self, score): 
        Menu.__init__(self)
        self.button_dict["TypingGame"] = Button("Play Again", (WIDTH/2), (HEIGHT)/4)
        self.button_dict["StartMenu"] = Button("Main Menu", (WIDTH/2), (HEIGHT)/2)
        self.title_array.append(Button(f"Score : {score}", (WIDTH/2), (HEIGHT*3)/4))
    

# FONT = freetype.Font(".\\images\\scary_font.ttf", 50)

# class GameSummaryMenu():
#     def __init__(self, score):
#         self.score = score
#         self.menu_image, self.menu_rect = FONT.render("MENU", "blue")
#         self.menu_rect.center = (WIDTH / 2, HEIGHT * 0.25)
#         self.score_image, self.score_rect = FONT.render(f"Score: {self.score}", "blue")
#         self.score_rect.center = (WIDTH / 2, HEIGHT * 0.75)

#     def main_loop(self, screen, background, clock):
#         """main pygame loop, shows game score, and option to return to main menu"""
#         while True:
#             clock.tick(60)
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     if self.menu_rect.collidepoint(event.pos):
#                         return "StartMenu"

#             screen.fill("black")
#             screen.blit(background, (0, 0))
#             screen.blit(self.menu_image, self.menu_rect)
#             screen.blit(self.score_image, self.score_rect)
#             pygame.display.update()
