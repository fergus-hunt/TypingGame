import pygame, sys, time
from game_text import GameText
from pygame import freetype
from enemy import Enemy
from main_character import MainCharacter
from scoreboard import ScoreBoard

pygame.init()
freetype.init()     

# global window size constants 
HEIGHT = 965
WIDTH = 1285


class TypingGame:
    def __init__(self, graph, feature_control) -> None:
        self.game_sprites = pygame.sprite.Group()
        # storing graph of checkpoints and useability features 
        self.feature_control =feature_control
        self.df = graph

        # initialize moving game entiteis 
        self.character = MainCharacter()
        self.enemy = Enemy()
        self.scoreboard = ScoreBoard(feature_control)

        # adding entities to group
        self.game_sprites.add(self.character)
        self.game_sprites.add(self.enemy)
        self.game_sprites.add(self.scoreboard)

        # initializing text surrounding user 
        self.text_object = None
        self.text_sprites = pygame.sprite.Group()
        self.make_new_text_sprites()

        # self.music = pygame.mixer.Sound("images/game_music.mp3")

    def alert(self, screen):
        """shows the current round within pygame screen"""
        if self.scoreboard.score % 100 == 0:
            # Makes big screen for limited frames that shows current found 
            alert_image, alert_rect = self.feature_control.font_dynamic.render(f"Round {self.scoreboard.score}", self.feature_control.colour)
            alert_rect.center = (WIDTH / 2, HEIGHT / 5)
            screen.blit(alert_image, alert_rect)

    def calculate_enemy_path(self):
        """Dijkstra's algorithm to find the shortest path enemy can take towards user"""
        if self.enemy.current_node != self.character.current_node: # ensure game isn't over 
            visited = {}
            unvisited = {}
            # making an array of unvisited nodes 
            for node in self.df['distances'].keys():
                unvisited[node] = [sys.maxsize, None]


            current_node = self.enemy.current_node
            unvisited[f"{current_node}"] = [0, None]

            # iterating through all nodes 
            while len(unvisited) > 0:
                current_node = f"{min(unvisited, key=unvisited.get)}" # finding shortest node to enemy 
                neighbours = self.df['distances'][f"{current_node}"] # storing the distances of surrounding checkpoints
                for node in neighbours:
                    if node in unvisited.keys():
                        cost = unvisited[current_node][0] + neighbours[node] # saving distance between adjacent nodes 
                        if cost < unvisited[node][0]: # storing the distance in unvisited list 
                            unvisited[node] = [cost, current_node]

                visited[current_node] = unvisited[current_node] # putting checked node in visited list 
                del unvisited[current_node] # deleting node from unvisited list 

            node = visited[str(self.character.current_node)] # marking the destination node 
            temporary_node = node[1] 
            if not temporary_node:  # The game will be over 
                return "GameSummary", self.scoreboard.score
            
            path = [self.character.current_node, node[1]] # array sequentially storing shortest path for enemy 
            while str(temporary_node)!= str(self.enemy.current_node) and self.enemy.current_node != self.character.current_node:
                
                path.append(visited[str(temporary_node)][1])
                temporary_node = visited[temporary_node][1] 

            del path[-1] # deleting enemy current node 
            self.enemy.path = path # setting enemy attribute as new shortest path 

    def register_key(self, event):
        """Registers the key presses for user against the surrounding text objects"""
        if self.text_object is None: # there is no progress on any surrounding texts 
            counter = 0
            while counter < (len(self.text_sprites.sprites())):
                current_object = self.text_sprites.sprites()[counter]

                # checking if key event is same as any neighbouring first characters 
                if event.unicode == current_object.characters_unicode[0]: 
                    self.text_object = current_object
                    self.text_object.characters_completed[0] = True
                    self.text_object.next_key += 1 # storing progress as attribute 
                    counter = 5 # stopping iteration
                counter += 1
        else:
            # is input the second character of text object
            if event.unicode == self.text_object.characters_unicode[self.text_object.next_key]:
                # marking second character as completed 
                self.text_object.characters_completed[self.text_object.next_key] = True
                self.text_object.next_key += 1
                if self.text_object.next_key == len(self.text_object.characters_completed): # is text completed
                    # setting the character next node to the completed text 
                    self.character.movement_steps(self.text_object.current_node, self.text_object.rect.center)
                    self.character.is_moving = True 
            else: # character is wrong, text object is reset 
                self.text_object.characters_reset()
                self.text_object.next_key = 0
                self.text_object = None

    def make_new_text_sprites(self):
        """Makes new text sprites when user has arrived at new checkpoint"""
        self.text_object = None
        # finding all surrounding checkpoints to user position 
        positions = [(self.df['positions'][node][0], self.df['positions'][node][1], node) for node in
                     self.df['distances'][f"{self.character.current_node}"]]
        self.text_sprites.empty() # removing all surrounding text 
        # making new text objects
        for position in positions: 
            self.text_sprites.add(GameText(position[0], position[1], position[2], self.feature_control))

    def main_loop(self, screen, background, clock): 
        """Main pygame loop where the user plays the game, updates screen and register events """

        self.calculate_enemy_path() # using dijkstras algorithm to find enemy path 
        self.enemy.movement_steps(self.df["positions"][f"{self.enemy.current_node}"])
        self.feature_control.music.play() # play game music 
        entity_update_rate = 0
        # main loop 
        while True:
            clock.tick(60)
            entity_update_rate += clock.get_time() # updating the time elapsed

            # iterating through user events between frames  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # register user keypress 
                elif event.type == pygame.KEYDOWN and len(self.character.next_positions) == 0:
                    self.feature_control.keysound.play()
                    self.register_key(event)
            # character has reached new checkpoint 
            if self.character.stopped_moving:
                self.character.stopped_moving = False
                self.enemy.user_node = self.character.current_node # updating the new nodes 
                self.calculate_enemy_path() # calculating new enemy shortest path 
                self.make_new_text_sprites() # reinitializing neighbouring text 
                self.scoreboard.update_scoreboard() # adding to scoreboard 

            # enemy has reached new checkpoint
            if self.enemy.stopped_moving:  
                self.enemy.stopped_moving = False
                self.enemy.current_node = self.enemy.path[-1]
                del self.enemy.path[-1] # updating enemy current node 
                # making new movement direction for enemy 
                self.enemy.movement_steps(self.df["positions"][f"{self.enemy.current_node}"]) 

            # enemy node = characater node so game is over 
            if self.enemy.current_node == self.character.current_node:
                return "GameSummary", self.scoreboard.score

            # if new round the enemy movement speed is incremented 
            elif self.scoreboard.score % 100 == 0: 
                self.enemy.movement_speed = int(20 - self.scoreboard.score / 100)

            # updating entities if elapsed time has passed 
            if entity_update_rate > 200:
                self.game_sprites.update()
                entity_update_rate = 0 # resetting time counter 

            screen.fill('black')
            screen.blit(background, (0, 50))

            # drawing all sprites on screen 
            self.game_sprites.draw(screen)
            self.text_sprites.update()
            self.text_sprites.draw(screen)
            self.alert(screen)
            # updating the display 
            pygame.display.update()