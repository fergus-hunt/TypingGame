import pygame, time
from test_text import TestText

pygame.init()

class TypingTest:
    def __init__(self):
        self.text_object = TestText()

    def main_loop(self, screen, background, clock):
        """main python loop which allows user to play game"""
        start_time = time.time()
        while True:
            clock.tick(60)
            if self.text_object.is_complete:
                end_time = time.time()
                wpm = self.text_object.calculating_wpm(start_time, end_time)
                errors = self.text_object.calculate_errors()
                return 'TestSummary', wpm, errors
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    self.text_object.noise.play()
                    self.text_object.register_key(event)
            self.text_object.rendering_text()
            screen.fill("black")
            screen.blit(background, (0, 0))
            screen.blit(self.text_object.surface, self.text_object.rect)
            pygame.display.update()
