import pygame, pandas, json, numpy
from text import Text
from pygame import freetype 
from enemy import Enemy
from maincharacter import MainCharacter
from scoreboard import ScoreBoard
from typetesttext import TypeTestText

FONT = freetype.Font(None, 50)
HEIGHT = 965
WIDTH = 1285

class TestSummaryMenu(): 
        
    def get_stats(self, wpm, errors): 
        self.wpm = wpm
        self.errors = errors

    def main_loop(self, screen, background): 
        clock = pygame.time.Clock()
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
            # FONT.render_to(screen, (WIDTH/2, HEIGHT/2 + 50), str(self.wpm), 'blue')
            # FONT.render_to(screen, (WIDTH/2, HEIGHT/2), str(self.errors), 'red')
            pygame.display.update()

class GameSummaryMenu(): 
    def __init__(self, score):
        self.score = score
        self.menu_image, self.menu_rect = FONT.render("MENU", "blue")
        self.menu_rect.center = (WIDTH/2, HEIGHT*0.25)
        self.score_image, self.score_rect = FONT.render(f"Score: {self.score}", "blue")
        self.score_rect.center = (WIDTH/2, HEIGHT*0.75)

    def main_loop(self, screen, background): 
        clock = pygame.time.Clock() 
        while True: 
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





class StartMenu(): 
    def __init__(self) -> None:        
        # self.play_button = FONT.get_rect("Play Game")
        # self.stats_button = FONT.get_rect("View Stats")
        self.play_surface, self.play_button = FONT.render("Play Game", 'blue')
        self.stats_surface, self.stats_button = FONT.render("View Stats", 'blue')
        self.test_surface, self.test_button = FONT.render("Take Test", "blue")
        self.play_button.center = (WIDTH/2, HEIGHT*0.25)
        self.test_button.center = (WIDTH/2, HEIGHT/2)
        self.stats_button.center = (WIDTH/2, 0.75*HEIGHT)

    def main_loop(self, screen, background): 
        clock = pygame.time.Clock()
        while True: 
            clock.tick(60)
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT : 
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    print(event.pos)
                    if self.play_button.collidepoint(event.pos): 
                        return "TypingGame"
                    elif self.test_button.collidepoint(event.pos): 
                        return "TypingTest"
            
            screen.fill('black')
            screen.blit(background, (0, 0))
            screen.blit(self.play_surface, self.play_button)
            screen.blit(self.test_surface, self.test_button)
            pygame.display.update()







class TypingGame(): 
    def __init__(self, graph, character_moving, next_animation, game_over) -> None:
        self.STOP_MOVING = character_moving
        self.NEXT_ANIMATION = next_animation
        self.GAME_OVER = game_over
        self.df = graph

        self.character = MainCharacter(character_moving, graph)
        self.enemy = Enemy(graph, game_over)
        self.scoreboard = ScoreBoard()
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
                elif event.type == pygame.KEYDOWN and not self.character.is_moving: 
                    self.register_key(event)

                if event.type == self.GAME_OVER: 
                    return "GameSummary"
                
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

class TypingTest(): 
    def __init__(self): 
        self.text_object = TypeTestText()


    def main_loop(self, screen, background): 
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            if self.text_object.is_complete: 
                return 'TestSummary'
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                elif event.type == pygame.KEYDOWN: 
                    self.text_object.register_key(event)
            self.text_object.rendering_text()
            screen.fill("black") 
            screen.blit(background, (0, 0))
            screen.blit(self.text_object.surface, self.text_object.rect)
            pygame.display.update()