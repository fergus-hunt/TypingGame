import pygame, sys, time
from game_text import GameText
from pygame import freetype
from enemy import Enemy
from main_character import MainCharacter
from scoreboard import ScoreBoard

pygame.init()
freetype.init()     

FONT = freetype.Font(".\\images\\scary_font.ttf", 50)
HEIGHT = 965
WIDTH = 1285


class TypingGame:
    def __init__(self, graph) -> None:
        self.game_sprites = pygame.sprite.Group()
        self.df = graph

        self.character = MainCharacter()
        self.enemy = Enemy()
        self.scoreboard = ScoreBoard()

        self.game_sprites.add(self.character)
        self.game_sprites.add(self.enemy)
        self.game_sprites.add(self.scoreboard)

        self.text_object = None
        self.text_sprites = pygame.sprite.Group()
        self.make_new_text_sprites()

        # self.music = pygame.mixer.Sound("images/game_music.mp3")
        self.key_noise = pygame.mixer.Sound('./images/typewriter.wav')

    def alert(self, screen):
        """shows the current round within pygame screen"""
        if self.scoreboard.score % 100 == 0:
            alert_image, alert_rect = FONT.render(f"Round {self.scoreboard.score}")
            alert_rect.center = (WIDTH / 2, HEIGHT / 5)
            screen.blit(alert_image, alert_rect)

    def calculate_enemy_path(self):
        """Dijkstra's algorithm to find the shortest path enemy can take towards user"""
        if self.enemy.current_node != self.character.current_node:
            visited = {}
            unvisited = {}
            for node in self.df['distances'].keys():
                unvisited[node] = [sys.maxsize, None]

            current_node = self.enemy.current_node
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

            node = visited[str(self.character.current_node)]
            temporary_node = node[1]
            if not temporary_node: 
                return "GameSummary", self.scoreboard.score
            
            path = [self.character.current_node, node[1]]
            while str(temporary_node)!= str(self.enemy.current_node) and self.enemy.current_node != self.character.current_node:
                
                path.append(visited[str(temporary_node)][1])
                temporary_node = visited[temporary_node][1]

            # print(f"Enemy path: {path}")
            # print(f"Current node : {self.enemy.current_node}")
            # print(f"Next node : {self.enemy.next_node}")
            del path[-1]
            self.enemy.path = path

    def register_key(self, event):
        """Registers the key presses for user against the surrounding text objects"""
        if self.text_object is None:
            counter = 0
            while counter < (len(self.text_sprites.sprites())):
                current_object = self.text_sprites.sprites()[counter]
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
                    self.character.movement_steps(self.text_object.current_node, self.text_object.rect.center)
                    self.character.is_moving = True
            else:
                self.text_object.characters_reset()
                self.text_object.next_key = 0
                self.text_object = None

    def make_new_text_sprites(self):
        """Makes new text sprites when user has arrived at new checkpoint"""
        self.text_object = None
        positions = [(self.df['positions'][node][0], self.df['positions'][node][1], node) for node in
                     self.df['distances'][f"{self.character.current_node}"]]
        self.text_sprites.empty()
        for position in positions:
            self.text_sprites.add(GameText(position[0], position[1], position[2]))

    def main_loop(self, screen, background, clock):
        """Main pygame loop where the user plays the game"""
        self.calculate_enemy_path()
        self.enemy.movement_steps(self.df["positions"][f"{self.enemy.current_node}"])
        # self.music.play()
        entity_update_rate = 0
        while True:
            clock.tick(60)
            entity_update_rate += clock.get_time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.KEYDOWN and len(self.character.next_positions) == 0:
                    self.key_noise.play()
                    self.register_key(event)

            if self.character.stopped_moving:
                self.character.stopped_moving = False
                self.enemy.user_node = self.character.current_node
                self.calculate_enemy_path()
                self.make_new_text_sprites()
                self.scoreboard.update_scoreboard()

            if self.enemy.stopped_moving:
                self.enemy.stopped_moving = False
                self.enemy.current_node = self.enemy.path[-1]
                del self.enemy.path[-1]
                self.enemy.movement_steps(self.df["positions"][f"{self.enemy.current_node}"])
                print(f"path = {self.enemy.path}")
                print(f"Current node : {self.enemy.current_node}")


            if self.enemy.current_node == self.character.current_node:
                # self.music.stop()
                return "GameSummary", self.scoreboard.score

            elif self.scoreboard.score % 100 == 0:
                self.enemy.movement_speed = int(20 - self.scoreboard.score / 100)

            if entity_update_rate > 200:
                self.game_sprites.update()
                entity_update_rate = 0

            screen.fill('black')
            screen.blit(background, (0, 50))
            self.game_sprites.draw(screen)
            self.text_sprites.update()
            self.text_sprites.draw(screen)
            self.alert(screen)
            pygame.display.update()