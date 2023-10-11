import pygame, time, lorem, pyautogui, pandas, random, json
from tkinter import messagebox
from text import Text
import pygame.freetype
from login import AuthenticateUser
from gamestages import * 
from enemy import Enemy
from maincharacter import MainCharacter
pygame.init()

# Login = AuthenticateUser(database_manager=DatabaseManager)
# Login.log_in_user()
# Login.root.mainloop()

# USERNAME = Login.username

pygame.init()
FPS = 20
HEIGHT = 800
WIDTH = 1100


CLASSROOM=pygame.transform.scale(pygame.image.load("C:/Users/fungu/Desktop/Typinggame/images/classroom.png"), (WIDTH, HEIGHT -50 ))

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock() 

FONT = pygame.freetype.Font(None, 30)
FONT.origin = True

def find_connection_nodes(current_node): 
    with open("./database/graph.json") as file: 
        graph = json.loads(file.read())
    all_nodes = [node for node in graph[f"{current_node}"]]
    df = pandas.read_csv("./database/positions.csv")
    positions = []
    for node in all_nodes: 
        seat_x_y = df.loc[int(node)]
        positions.append((seat_x_y.x, seat_x_y.y))
    return positions

def make_new_text_sprites(text_group, positions): 
    text_group.empty()
    for node in positions: 
        text_group.add(Text(node[0], node[1]))
    return text_group

wraith = Enemy(0, 400)
all_texts = pygame.sprite.Group()
df = pandas.read_csv("database\positions.csv") 
user_location = (random.randint(0, df.shape[0]-1))
user_connecting_nodes = find_connection_nodes(user_location)
x, y = df.iloc[user_location][1:3]
user = MainCharacter(x, y)
sprites = pygame.sprite.Group()
sprites.add(wraith)
sprites.add(user)
text_sprites = pygame.sprite.Group()
text_sprites = make_new_text_sprites(text_sprites, user_connecting_nodes)

# print(random.randint(df.shape[0]))
# for x_pos, y_pos in zip(df['x'], df['y']): 
#     text_thing = Text(x_pos, y_pos)
#     all_texts.add(text_thing)



class MainGame(): 
    def __init__(self, text_objects) -> None:
        self.clock = pygame.time.Clock()
        self.text_objects = text_objects
        self.text_object = None

    def register_key(self, event):
        counter = 0
        print(event)
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
                    self.is_complete = True
            else: 
                self.text_object.characters_reset()
                self.text_object.next_key = 0
                self.text_object = None
            
        # else:
        #     if event.unicode == self.characters_unicode[self.next_key]: 
        #         self.characters_completed[self.next_key] = True
        #         self.next_key += 1
        #     elif event.unicode != '': 
        #         self.characters_completed[self.next_key] = False
        #         self.next_key += 1

    def reset_text_objects(self): 
        pass

    def main_loop(self, screen, game_entities): 
        while True:
            self.clock.tick(FPS)
            # if text_object.is_complete: 
            #     return 'summary'
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                elif event.type == pygame.KEYDOWN: 
                    self.register_key(event)
            
            screen.fill('black')
            screen.blit(CLASSROOM, (0, 50))
            game_entities.update()
            game_entities.draw(screen)
            self.text_objects.update()
            self.text_objects.draw(screen)
            pygame.display.update()

summarymenu = SummaryMenu(FONT, WIDTH, HEIGHT, FPS)

scene = 'menu'
maingame = MainGame(text_sprites)

startmenu = StartMenu(FONT, FPS)
# summarymenu = SummaryMenu()



while True: 
    if scene == 'menu': 
        scene = startmenu.main_loop(WIN)
    elif scene == "game":
        # TEXT.reset()
        # TEXT.start_time = time.time()
        scene = maingame.main_loop(WIN, sprites)
    elif scene == "summary": 
        # wpm = TEXT.calculating_wpm()
        # errors = TEXT.calculate_errors()
        summarymenu.get_stats(wpm=100, errors=100)
        scene = summarymenu.main_loop(WIN)


# threading for event process and mainloop? 
# pickle in python