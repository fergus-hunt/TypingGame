import pygame, time, lorem, pyautogui, pandas, random, json
from tkinter import messagebox
from text import Text
import pygame.freetype
from login import AuthenticateUser
from gamestages import * 
from enemy import Enemy
from maincharacter import MainCharacter
from scoreboard import ScoreBoard
pygame.init()

# Login = AuthenticateUser(database_manager=DatabaseManager)
# Login.log_in_user()
# Login.root.mainloop()
# USERNAME = Login.username

pygame.init()
FPS = 20
HEIGHT = 965
WIDTH = 1285

STOPPED_MOVING = (pygame.USEREVENT + 1)
NEXT_ANIMATION = (pygame.USEREVENT + 2)
GAME_OVER = (pygame.USEREVENT + 3)
CLASSROOM=pygame.image.load("images\classroom4.png")

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock() 

FONT = pygame.freetype.Font(None, 30)
FONT.origin = True


# all_texts = pygame.sprite.Group()
sprites = pygame.sprite.Group()

with open("./database/graph.json") as file: 
    graph = json.loads(file.read())
user = MainCharacter(17, 547, 602, STOPPED_MOVING, graph)
sprites.add(user)
user_score = ScoreBoard(WIDTH/2, 0)
sprites.add(user_score)
wraith = Enemy(100, 100, graph, GAME_OVER)
sprites.add(wraith)
textgame= MainGame(user, wraith, user_score, graph,  STOPPED_MOVING, NEXT_ANIMATION, GAME_OVER)

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
