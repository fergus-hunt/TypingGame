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
# FPS = 20
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

game_alert = Alert()

testsummarymenu = TestSummaryMenu()
startmenu = StartMenu()

scene = 'StartMenu'


while True: 
    if scene == 'StartMenu': 
        scene = startmenu.main_loop(WIN)
    elif scene == "TypingGame":
        typinggame =  TypingGame(graph, STOPPED_MOVING, NEXT_ANIMATION, GAME_OVER)
        scene = typinggame.main_loop(WIN, game_alert, CLASSROOM)
    elif scene == "TypingTest": 
        typingtest = TypingTest()
        scene =typingtest.main_loop(WIN)
    elif scene == "TestSummary": 
        testsummarymenu.get_stats(wpm=100, errors=100)
        scene = testsummarymenu.main_loop(WIN)
    elif scene == "GameSummary": 
        game_summary = GameSummaryMenu(score=typinggame.scoreboard.score)
        scene = game_summary.main_loop(WIN)

