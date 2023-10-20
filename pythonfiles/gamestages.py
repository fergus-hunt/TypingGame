import pygame, pandas, json, numpy
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
    def __init__(self, player, enemy, scoreboard,alert,   graph,  character_moving, next_animation, game_over) -> None:
        self.STOP_MOVING = character_moving
        self.NEXT_ANIMATION = next_animation
        self.GAME_OVER = game_over
        self.fps = 60
        self.df = graph

        self.scoreboard = scoreboard
        self.character = player
        self.enemy = enemy
        self.alert = alert

        
        self.text_object = None
        self.clock = pygame.time.Clock()
        self.text_objects = pygame.sprite.Group()
        self.make_new_text_sprites()

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

    def main_loop(self, screen, game_entities, background): 

        pygame.time.set_timer(self.NEXT_ANIMATION, 200)
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                elif event.type == pygame.KEYDOWN: 
                    self.register_key(event)

                # if event.type == self.GAME_OVER: 
                #     return "menu"
                
                if event.type == self.NEXT_ANIMATION: 
                    game_entities.update()
                    # if self.enemy.user_found: 
                    #     pygame.quit()

                if event.type == self.STOP_MOVING: 
                    self.enemy.user_node = self.character.node
                    self.make_new_text_sprites()
                    self.scoreboard.update_score()
            


                if self.scoreboard.score %100 == 0: 
                    # self.enemy.movement_speed = self.enemy.movement_speed - 2
                    self.alert.new_round(self.scoreboard.score / 100)


            screen.fill('black')
            screen.blit(background, (0, 50))
            game_entities.draw(screen)
            self.text_objects.update()
            self.text_objects.draw(screen)
            pygame.display.update()