# from pygame import freetype
# import pygame
from button import Button
from menu import Menu

HEIGHT = 965
WIDTH = 1285

class MainMenu(Menu):
    def __init__(self): 
        Menu.__init__(self)
        self.button_dict["TypingGame"] = (Button("Play Game", WIDTH/2, HEIGHT * 0.25))
        self.button_dict["TypingTest"]=Button( "Take Test", WIDTH / 2, HEIGHT / 2)
        self.button_dict["ResultViewer"]=(Button("View Stats", WIDTH / 2, 0.75 * HEIGHT))



# pygame.init()
# freetype.init()


# class MainMenu:
#     def __init__(self) -> None:
#         self.button_dict = {}
#         self.button_dict["TypingGame"] = (Button("Play Game", WIDTH/2, HEIGHT * 0.25))
#         self.button_dict["TypingTest"]=Button( "Take Test", WIDTH / 2, HEIGHT / 2)
#         self.button_dict["ResultViewer"]=(Button("View Stats", WIDTH / 2, 0.75 * HEIGHT))
#         # self.play_surface, self.play_button = FONT.render("Play Game", 'blue')
#         # self.stats_surface, self.stats_button = FONT.render("View Stats", 'blue')
#         # self.test_surface, self.test_button = FONT.render("Take Test", "blue")

#     def main_loop(self, screen, background, clock):
#         """Main pygame loop, shows buttons to play game, take the test and view user statistics"""
#         while True:
#             clock.tick(60)
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     for button in self.button_dict:
#                         if self.button_dict[button].rect.collidepoint(event.pos):
#                             return button
#                     # elif self.button_dict[1].rect.collidepoint(event.pos):
#                     #     return "TypingTest"
#                     # elif self.button_dict[2].rect.collidepoint(event.pos):
#                     #     database_manager = DatabaseManager()
#                     #     userresult = database_manager.get_user_scores()
#                     #     results = ResultViewer(userresult)

#             screen.fill('black')
#             screen.blit(background, (0, 0))
#             for button in self.button_dict.values(): 
#                 button.update(screen)
#             # screen.blit(self.play_surface, self.play_button)
#             # screen.blit(self.test_surface, self.test_button)
#             # screen.blit(self.stats_surface, self.stats_button)
#             pygame.display.update()

