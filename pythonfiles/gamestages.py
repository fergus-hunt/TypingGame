import pygame, pandas, json, time
from text import Text

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

            
class MainGame(): 
    def __init__(self, player, fps, dataframe, graph, enemy) -> None:
        self.fps = fps
        self.df = dataframe
        self.graph = graph
        self.character = player
        self.enemy = enemy
        
        self.text_object = None
        self.clock = pygame.time.Clock()
        self.text_objects = pygame.sprite.Group()
        self.make_new_text_sprites()
        self.character_move = pygame.USEREVENT + 1

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
                    self.find_denominations()
                    self.make_new_text_sprites()
                    self.character.is_moving = True
            else: 
                self.text_object.characters_reset()
                self.text_object.next_key = 0
                self.text_object = None
            

    def find_denominations(self): 
        self.character.node = self.text_object.node
        print(f"Text position: {self.text_object.rect.center}")
        print("Character position: " + str(self.character.rect.center))
        next_character_position = self.df[f"{self.character.node}"]
        print(f"Next character position: {next_character_position}")
        time.sleep(10)
        x_denoms = (next_character_position[0] - self.character.rect.x)/6
        y_denoms = (next_character_position[1] - self.character.rect.y)/6
        for i in range(0, 7): 
            next_pos = (i * x_denoms + self.character.rect.x, i * y_denoms + self.character.rect.y)
            self.character.next_positions.append(next_pos)


        
        
    def make_new_text_sprites(self): 
        self.text_object = None
        positions = self.df[f"{self.character.node}"]
        positions = [(self.df[node][0], self.df[node][1], node) for node in self.graph[f"{self.character.node}"]]
        self.text_objects.empty()
        for position in positions: 
            self.text_objects.add(Text(position[0],position[1], position[2]))


    def main_loop(self, screen, game_entities, background, enemy): 

        pygame.time.set_timer(self.character_move, 2000)
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == self.character_move: 
                    self.character.update()
                if event.type == pygame.QUIT:
                    pygame.quit() 

                elif event.type == pygame.KEYDOWN: 
                    self.register_key(event)
            
            screen.fill('black')
            screen.blit(background, (0, 50))
            enemy.find_user(self.character.node)
            game_entities.update()
            game_entities.draw(screen)
            self.text_objects.update()
            self.text_objects.draw(screen)
            pygame.display.update()