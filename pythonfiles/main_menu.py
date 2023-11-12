from pygame import freetype
import pygame
from database_manager import DatabaseManager
from result_viewer import ResultViewer

pygame.init()
freetype.init()

FONT = freetype.Font(None, 50)
HEIGHT = 965
WIDTH = 1285

class MainMenu:
    def __init__(self) -> None:
        self.play_surface, self.play_button = FONT.render("Play Game", 'blue')
        self.stats_surface, self.stats_button = FONT.render("View Stats", 'blue')
        self.test_surface, self.test_button = FONT.render("Take Test", "blue")
        self.play_button.center = (WIDTH / 2, HEIGHT * 0.25)
        self.test_button.center = (WIDTH / 2, HEIGHT / 2)
        self.stats_button.center = (WIDTH / 2, 0.75 * HEIGHT)

    def main_loop(self, screen, background, clock):
        """Main pygame loop, shows buttons to play game, take the test and view user statistics"""
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.pos)
                    if self.play_button.collidepoint(event.pos):
                        return "TypingGame"
                    elif self.test_button.collidepoint(event.pos):
                        return "TypingTest"
                    elif self.stats_button.collidepoint(event.pos):
                        database_manager = DatabaseManager()
                        userresult = database_manager.get_user_scores()
                        results = ResultViewer(userresult)

            screen.fill('black')
            screen.blit(background, (0, 0))
            screen.blit(self.play_surface, self.play_button)
            screen.blit(self.test_surface, self.test_button)
            screen.blit(self.stats_surface, self.stats_button)
            pygame.display.update()

