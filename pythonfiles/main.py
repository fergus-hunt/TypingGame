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
    print(all_nodes)
    for node in all_nodes: 
        seat_x_y = df.loc[int(node)]
        positions.append((seat_x_y.x, seat_x_y.y))
    return positions

def make_new_text_sprites(text_group, positions): 
    text_group.empty()
    for node in positions: 
        text_group.add(Text(node[0], node[1]))
    return text_group

class Teacher(pygame.sprite.Sprite): 
    def __init__(self, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.current_animation = "idle"
        self.idle_images = self.get_images("images/idle-teacher", 4)
        self.dying_images = self.get_images("images/teacher-death", 8)
        self.animations = {
            "dying":self.dying_images,
            "idle":self.idle_images, 
        }
        self.image = self.animations[self.current_animation][0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def get_images(self, path, size):
        image_list = [] 
        for i in range(size): 
            if i < 10: 
                image_path = f"{path}/tile00{i}.png"
            else: 
                image_path = f"{path}/tile0{i}.png"
            image = pygame.transform.scale(pygame.image.load(image_path), (100, 100))
            image_list.append(image)
        return image_list
    
    def update(self): 
        self.image = self.animations[self.current_animation][self.frame]
        self.frame += 1
        if self.frame >= len(self.animations[self.current_animation]): 
            if self.current_animation == "dying": 
                self.kill()
            self.frame= 0

teacher = Teacher(600, 350)
wraith = Enemy(0, 400)
all_texts = pygame.sprite.Group()
df = pandas.read_csv("database\positions.csv") 
user_location = (random.randint(0, df.shape[0]-1))
user_connecting_nodes = find_connection_nodes(user_location)
x, y = df.iloc[user_location][1:3]
user = MainCharacter(x, y)
sprites = pygame.sprite.Group()
sprites.add(wraith)
sprites.add(teacher)
sprites.add(user)
text_sprites = pygame.sprite.Group()
text_sprites = make_new_text_sprites(text_sprites, user_connecting_nodes)

# print(random.randint(df.shape[0]))
# for x_pos, y_pos in zip(df['x'], df['y']): 
#     text_thing = Text(x_pos, y_pos)
#     all_texts.add(text_thing)



class MainGame(): 
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()

    def main_loop(self, screen, text_objects, student_entities): 
        while True:
            self.clock.tick(FPS)
            if pygame.sprite.collide_rect(wraith, teacher):
                wraith.current_animation = "attacking"
                teacher.current_animation = "dying"
                print(pygame.sprite.collide_rect(wraith, teacher))
            # if text_object.is_complete: 
            #     return 'summary'
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                elif event.type == pygame.KEYDOWN: 
                    for sprite in text_objects.spritedict.keys(): 
                        sprite.register_key(event)
            
            screen.fill('black')
            screen.blit(CLASSROOM, (0, 50))
            student_entities.update()
            student_entities.draw(screen)
            text_sprites.update()
            text_sprites.draw(screen)
            pygame.display.update()

summarymenu = SummaryMenu(FONT, WIDTH, HEIGHT, FPS)

scene = 'menu'
maingame = MainGame()

startmenu = StartMenu(FONT, FPS)
# summarymenu = SummaryMenu()



while True: 
    if scene == 'menu': 
        scene = startmenu.main_loop(WIN)
    elif scene == "game":
        # TEXT.reset()
        # TEXT.start_time = time.time()
        scene = maingame.main_loop(WIN, all_texts, sprites)
    elif scene == "summary": 
        # wpm = TEXT.calculating_wpm()
        # errors = TEXT.calculate_errors()
        summarymenu.get_stats(wpm=100, errors=100)
        scene = summarymenu.main_loop(WIN)


# threading for event process and mainloop? 
# pickle in python