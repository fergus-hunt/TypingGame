import pygame 
from pygame import freetype

pygame.init()
freetype.init()

FONT = freetype.Font(None, 50)
HEIGHT = 965
WIDTH = 1285

class GameSummaryMenu():
    def __init__(self, score):
        self.score = score
        self.menu_image, self.menu_rect = FONT.render("MENU", "blue")
        self.menu_rect.center = (WIDTH / 2, HEIGHT * 0.25)
        self.score_image, self.score_rect = FONT.render(f"Score: {self.score}", "blue")
        self.score_rect.center = (WIDTH / 2, HEIGHT * 0.75)

    def main_loop(self, screen, background, clock):
        """main pygame loop, shows game score, and option to return to main menu"""
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_rect.collidepoint(event.pos):
                        return "StartMenu"

            screen.fill("black")
            screen.blit(background, (0, 0))
            screen.blit(self.menu_image, self.menu_rect)
            screen.blit(self.score_image, self.score_rect)
            pygame.display.update()
