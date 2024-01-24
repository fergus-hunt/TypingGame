import pygame, time
from test_text import TestText

pygame.init()

class TypingTest:
    def __init__(self, feature_control):
        self.text_object = TestText(feature_control)


    def main_loop(self, screen, background, clock):
        """main python loop which allows user to play game, register key presses and update screen """
        start_time = time.time()
        while True:
            clock.tick(60)
            # text is comleted 
            if self.text_object.is_complete:
                end_time = time.time()
                # calculating wpm and error count 
                wpm = self.text_object.calculating_wpm(start_time, end_time)
                errors = self.text_object.calculate_errors()
                # returns user statistics 
                return 'TestSummary', wpm, errors
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    self.text_object.register_key(event)
            # rendering text 
            self.text_object.rendering_text()
            
            screen.fill("black")
            screen.blit(background, (0, 0))
            screen.blit(self.text_object.surface, self.text_object.rect)
            # updating background 
            pygame.display.update()
