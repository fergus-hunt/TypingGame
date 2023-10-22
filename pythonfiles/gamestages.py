import pygame, pandas, json, numpy
from text import Text
from pygame import freetype 
from enemy import Enemy
from maincharacter import MainCharacter
from scoreboard import ScoreBoard


FONT = freetype.Font(None, 50)

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
                        return 'menu'

            screen.fill('black')
            self.font.render_to(screen, (self.width/2, self.height/2 + 50), str(self.wpm), 'blue')
            self.font.render_to(screen, (self.width/2, self.height/2), str(self.errors), 'red')
            pygame.display.update()







class StartMenu(): 
    def __init__(self, FPS) -> None:        
        self.clock = pygame.time.Clock()
        self.fps = FPS
        # self.play_button = FONT.get_rect("Play Game")
        # self.stats_button = FONT.get_rect("View Stats")
        self.play_surface, self.play_button = FONT.render("Play Game", 'blue')
        self.stats_surface, self.stats_button = FONT.render("View Stats", 'blue')
        self.play_button.center = (200, 500)
        self.stats_button.center = (500, 500)

        

    def main_loop(self, screen): 
        while True: 
            self.clock.tick(self.fps)
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT : 
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    print(event.pos)
                    if self.play_button.collidepoint(event.pos): 
                        return "game"
                    elif self.stats_button.collidepoint(event.pos): 
                        return "summary"
            
            screen.fill('black')
            # self.render_text()
            screen.blit(self.play_surface, self.play_button)
            screen.blit(self.stats_surface, self.stats_button)
            pygame.display.update()







class MainGame(): 
    def __init__(self, graph, character_moving, next_animation, game_over) -> None:
        self.STOP_MOVING = character_moving
        self.NEXT_ANIMATION = next_animation
        self.GAME_OVER = game_over
        self.df = graph

        self.character = MainCharacter(character_moving, graph)
        self.enemy = Enemy(graph, game_over)
        self.scoreboard = ScoreBoard(500, 0)
        self.make_game_sprites()
        
        self.text_object = None
        self.text_objects = pygame.sprite.Group()
        self.make_new_text_sprites()

    def make_game_sprites(self): 
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.character)
        self.sprites.add(self.enemy)
        self.sprites.add(self.scoreboard)

    def register_key(self, event):
        if self.text_object == None: 
            counter = 0
            while counter < (len(self.text_objects.sprites())): 
                current_object = self.text_objects.sprites()[counter]
                if event.unicode == current_object.characters_unicode[0]: 
                    self.text_object = current_object
                    self.text_object.characters_completed[0] = True
                    self.text_object.next_key += 1
                    counter = 5
                counter += 1
        else: 
            if event.unicode == self.text_object.characters_unicode[self.text_object.next_key]:
                self.text_object.characters_completed[self.text_object.next_key] = True
                self.text_object.next_key += 1
                if self.text_object.next_key == len(self.text_object.characters_completed):
                    self.character.movement_steps(self.text_object.node)
                    self.character.is_moving = True
            else: 
                self.text_object.characters_reset()
                self.text_object.next_key = 0
                self.text_object = None
            
    def make_new_text_sprites(self): 
        self.text_object = None
        positions = self.df['positions'][f"{self.character.node}"]
        positions = [(self.df['positions'][node][0], self.df['positions'][node][1], node) for node in self.df['distances'][f"{self.character.node}"]]
        self.text_objects.empty()
        for position in positions: 
            self.text_objects.add(Text(position[0],position[1], position[2]))

    def main_loop(self, screen, alert, background): 
        pygame.time.set_timer(self.NEXT_ANIMATION, 200)
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                elif event.type == pygame.KEYDOWN: 
                    self.register_key(event)

                if event.type == self.GAME_OVER: 
                    return "summary"
                
                if event.type == self.NEXT_ANIMATION: 
                    self.sprites.update()

                if event.type == self.STOP_MOVING: 
                    self.enemy.user_node = self.character.node
                    self.make_new_text_sprites()
                    self.scoreboard.update_score()
            


                if self.scoreboard.score %100 == 0: 
                    self.enemy.movement_speed = int(20 - self.scoreboard.score/100)            
                    alert.new_round(self.scoreboard.score / 100)
                    alert.count = 0


            screen.fill('black')
            screen.blit(background, (0, 50))
            self.sprites.draw(screen)
            screen.blit(alert.image, alert.rect)
            alert.refresh()
            self.text_objects.update()
            self.text_objects.draw(screen)
            pygame.display.update()