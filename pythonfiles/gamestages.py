import pygame 

class SummaryMenu(): 
    def __init__(self, FONT, WIDTH, HEIGHT, FPS) -> None:
        self.clock = pygame.time.Clock()
        self.font = FONT
        self.width = WIDTH
        self.height = HEIGHT
        self.fps = FPS
        
    def get_stats(self, wpm, errors): 
        self.wpm = wpm
        self.errors = errors

    def main_loop(self, screen): 
        while True: 
            self.clock.tick(self.fps)
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    pygame.quit() 
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_SPACE: 
                        return 'game'

            screen.fill('black')
            self.font.render_to(screen, (self.width/2, self.height/2 + 50), str(self.wpm), 'blue')
            self.font.render_to(screen, (self.width/2, self.height/2), str(self.errors), 'red')
            pygame.display.update()


class StartMenu(): 
    def __init__(self, FONT, FPS) -> None:        
        self.clock = pygame.time.Clock()
        self.fps = FPS
        self.font = FONT

    def main_loop(self, screen): 
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        counter = 5
        run = True
        while run: 
            self.clock.tick(self.fps)
            if counter < 0: 
                return 'game'
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT : 
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.unicode == 'p': 
                    return 'game'
                if event.type == pygame.USEREVENT:
                    counter -= 1
            
            screen.fill('black')
            self.font.render_to(screen, ((screen.get_width()/2),(screen.get_height()/2) ), str(counter), "red")
            pygame.display.update()

            

# class MainGame(): 
#     def __init__(self, FPS ) -> None:
#         self.clock = pygame.time.Clock()

#     def main_loop(self, screen, text_object, student_entities): 
#         while True:
#             self.clock.tick(FPS)
#             if pygame.sprite.collide_rect(wraith, teacher):
#                 wraith.current_animation = "attacking"
#                 teacher.current_animation = "dying"
#                 print(pygame.sprite.collide_rect(wraith, teacher))
#             if text_object.is_complete: 
#                 return 'summary'
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit() 
#                 elif event.type == pygame.KEYDOWN: 
#                     text_object.register_key(event)
            

#             text_surf = text_object.rendering_text()
#             screen.fill("black")
#             screen.blit(CLASSROOM, (0, 50))
#             screen.blit(text_surf, text_object.rect)
#             student_entities.update()
#             student_entities.draw(screen)
#             pygame.display.update()