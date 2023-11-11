import pygame, pandas, json, numpy, time, sys
from text import Text
from pygame import freetype 
from enemy import Enemy
from maincharacter import MainCharacter
from scoreboard import ScoreBoard
from result_viewer import ResultViewer
from typetesttext import TypeTestText
from databasemanager import DatabaseManager

FONT = freetype.Font(None, 50)
HEIGHT = 965
WIDTH = 1285

class TestSummaryMenu(): 
        
    def get_stats(self, wpm, errors): 
        self.wpm = wpm
        self.errors = errors
        self.wpm_image, self.wpm_rect = FONT.render("WORDS PER MINUTE : " + str(self.wpm), 'blue')
        self.wpm_rect.center = (WIDTH/2, (HEIGHT*2)/3)
        self.error_image, self.error_rect = FONT.render("ERRORS : " + str(self.errors), 'red')
        self.error_rect.center = (WIDTH/2, HEIGHT/3)

    def main_loop(self, screen, background): 
        clock = pygame.time.Clock()
        while True: 
            clock.tick()
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    pygame.quit() 
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_SPACE: 
                        return 'StartMenu'

            screen.fill('black')
            screen.blit(background, (0, 0))
            screen.blit(self.error_image, self.error_rect)
            screen.blit(self.wpm_image, self.wpm_rect)
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
        self.play_surface, self.play_button = FONT.render("Play Game", 'blue')
        self.stats_surface, self.stats_button = FONT.render("View Stats", 'blue')
        self.test_surface, self.test_button = FONT.render("Take Test", "blue")
        self.play_button.center = (WIDTH/2, HEIGHT*0.25)
        self.test_button.center = (WIDTH/2, HEIGHT/2)
        self.stats_button.center = (WIDTH/2, 0.75*HEIGHT)

    def main_loop(self, screen, background, clock): 
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
                    elif self.stats_button.collidepoint(event.pos):
                        tempmanager = DatabaseManager()
                        userresult=tempmanager.get_user_scores()
                        results = ResultViewer(userresult)
            
            screen.fill('black')
            screen.blit(background, (0, 0))
            screen.blit(self.play_surface, self.play_button)
            screen.blit(self.test_surface, self.test_button)
            screen.blit(self.stats_surface, self.stats_button)
            pygame.display.update()

class TypingGame(): 
    def __init__(self, graph) -> None:
        self.df = graph

        self.character = MainCharacter()
        self.enemy = Enemy(graph)
        self.scoreboard = ScoreBoard()
        self.make_game_sprites()
        
        self.text_object = None
        self.text_objects = pygame.sprite.Group()
        self.make_new_text_sprites()

        # self.music = pygame.mixer.Sound("images/game_music.mp3")
        self.key_noise = pygame.mixer.Sound('images/typewriter.wav')

    def make_game_sprites(self): 
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.character)
        self.sprites.add(self.enemy)
        self.sprites.add(self.scoreboard)

    def alert(self, screen):
        if self.scoreboard.score % 100 == 0:
            alert_image, alert_rect = FONT.render(f"Round {self.scoreboard.score}")
            alert_rect.center = (WIDTH/2, HEIGHT/5)
            screen.blit(alert_image, alert_rect)



    def calculate_enemy_path(self):
        if self.enemy.current_node != self.character.node:
            visited = {}
            unvisited = {}
            for node in self.df['distances'].keys(): 
                unvisited[node] = [sys.maxsize, None]

            current_node = self.enemy.next_node
            unvisited[f"{current_node}"] = [0, None]
            
            while len(unvisited) > 0: 
                
                current_node = f"{min(unvisited, key=unvisited.get)}"
                neighbours = self.df['distances'][f"{current_node}"]
                for node in neighbours: 
                    if node in unvisited.keys(): 
                        cost = unvisited[current_node][0] + neighbours[node]
                        if cost < unvisited[node][0]: 
                            unvisited[node] = [cost, current_node]
                
                visited[current_node] = unvisited[current_node]
                del unvisited[current_node]

            node = visited[str(self.character.node)]
            temporary_node = node[1]

            path = [self.character.node, node[1]]
            while temporary_node != self.enemy.next_node and self.enemy.current_node != self.character.node:

                previous_node = visited[temporary_node][1]
                path.append(previous_node)
                temporary_node = visited[temporary_node][1]

            print(f"Enemy path: {path}")
            print(f"Cureent node : {self.enemy.current_node}")
            print(f"Next node : {self.enemy.next_node}")
            self.enemy.path = path


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
                    self.character.movement_steps(self.text_object.node,self.text_object.rect.center)
                    self.character.is_moving = True
            else: 
                self.text_object.characters_reset()
                self.text_object.next_key = 0
                self.text_object = None
            
    def make_new_text_sprites(self): 
        self.text_object = None
        positions = [(self.df['positions'][node][0], self.df['positions'][node][1], node) for node in self.df['distances'][f"{self.character.node}"]]
        self.text_objects.empty()
        for position in positions: 
            self.text_objects.add(Text(position[0],position[1], position[2]))


    def main_loop(self, screen,  background, clock): 
        self.calculate_enemy_path()
        
        # self.music.play()
        tick_interval = 0

        while True:
            clock.tick(60)
            tick_interval += clock.get_time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    
                elif event.type == pygame.KEYDOWN and len(self.character.next_positions) == 0: 
                    self.key_noise.play()
                    self.register_key(event)

            if self.character.stopped_moving:
                self.character.stopped_moving = False
                self.enemy.user_node = self.character.node
                self.calculate_enemy_path()
                self.make_new_text_sprites()
                self.scoreboard.update_scoreboard()
                    
            if pygame.sprite.collide_rect(self.enemy, self.character):
                # self.music.stop()
                return "GameSummary", self.scoreboard.score
            
            elif self.scoreboard.score %100 == 0: 
                self.enemy.movement_speed = int(20 - self.scoreboard.score/100)            

            if tick_interval > 200:
                self.sprites.update()
                tick_interval = 0


            screen.fill('black')
            screen.blit(background, (0, 50))
            self.sprites.draw(screen)
            self.text_objects.update()
            self.text_objects.draw(screen)
            self.alert(screen)
            pygame.display.update()

class TypingTest(): 
    def __init__(self): 
        self.text_object = TypeTestText()


    def main_loop(self, screen, background): 
        clock = pygame.time.Clock()
        start_time = time.time()
        while True:
            clock.tick(60)
            if self.text_object.is_complete: 
                end_time = time.time()
                words_per_minute = self.text_object.calculating_wpm(start_time, end_time)
                errors = self.text_object.calculate_errors()
                return 'TestSummary', words_per_minute, errors
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
