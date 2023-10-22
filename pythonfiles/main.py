import pygame, time, lorem, pyautogui, pandas, random, json
from tkinter import messagebox
from text import Text
from pygame import freetype
from login import AuthenticateUser
from gamestages import * 

from alerts import Alert
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

FONT = freetype.Font(None, 30)
FONT.origin = True




# all_texts = pygame.sprite.Group()

with open("./database/graph.json") as file: 
    graph = json.loads(file.read())

sprites = pygame.sprite.Group()
game_alert = Alert()

summarymenu = SummaryMenu(FONT, WIDTH, HEIGHT, FPS)

scene = 'menu'

startmenu = StartMenu(FPS)

while True: 
    if scene == 'menu': 
        scene = startmenu.main_loop(WIN)
    if scene == "game":
        textgame =  MainGame(graph, STOPPED_MOVING, NEXT_ANIMATION, GAME_OVER)
        scene = textgame.main_loop(WIN, game_alert, CLASSROOM)
    elif scene == "summary": 
        summarymenu.get_stats(wpm=100, errors=100)
        scene = summarymenu.main_loop(WIN)
