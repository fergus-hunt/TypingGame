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

STOPPED_MOVING = (pygame.USEREVENT + 1)
NEXT_ANIMATION = (pygame.USEREVENT + 2)
print(type(STOPPED_MOVING))

CLASSROOM=pygame.transform.scale(pygame.image.load("C:/Users/fungu/Desktop/Typinggame/images/classroom.png"), (WIDTH, HEIGHT -50 ))

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock() 

FONT = pygame.freetype.Font(None, 30)
FONT.origin = True


all_texts = pygame.sprite.Group()
user = MainCharacter(17, 547, 602, STOPPED_MOVING)
sprites = pygame.sprite.Group()
sprites.add(user)
# dataframe = pandas.read_csv("./database/positions.csv")
with open("./database/graph.json") as file: 
    graph = json.loads(file.read())
wraith = Enemy(100, 100, graph["positions"], graph["distances"])
sprites.add(wraith)
textgame = MainGame(user, 60, graph['positions'], graph['distances'], wraith, STOPPED_MOVING, NEXT_ANIMATION)

summarymenu = SummaryMenu(FONT, WIDTH, HEIGHT, FPS)

scene = 'menu'

startmenu = StartMenu(FONT, FPS)


while True: 
    if scene == 'menu': 
        scene = startmenu.main_loop(WIN)
    elif scene == "game":
        scene = textgame.main_loop(WIN, sprites, CLASSROOM)
    elif scene == "summary": 
        summarymenu.get_stats(wpm=100, errors=100)
        scene = summarymenu.main_loop(WIN)


# organise code so character repositions itself, 
# make the enemy dijkstras algorithm work 

