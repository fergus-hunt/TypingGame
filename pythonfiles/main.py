import pygame, time, lorem, pyautogui, pandas, random, json
from tkinter import messagebox
from text import Text
from pygame import freetype
from login import AuthenticateUser
from gamestages import * 
from alerts import Alert
from databasemanager import DatabaseManager
pygame.init()

DataManager = DatabaseManager()

# Login = AuthenticateUser(database_manager=DatabaseManager)
# Login.log_in_user()
# Login.root.mainloop()
# USERNAME = Login.username

USERNAME = "Fergus"

pygame.init()
# FPS = 20
HEIGHT = 965
WIDTH = 1285

STOPPED_MOVING = (pygame.USEREVENT + 1)
NEXT_ANIMATION = (pygame.USEREVENT + 2)
GAME_OVER = (pygame.USEREVENT + 3)
CLASSROOM=pygame.image.load("images\\backgrounds\\classroom4.png")
MENUBACKGROUND = pygame.transform.scale(pygame.image.load("images\\backgrounds\\haunted_house.jpeg"), (WIDTH, HEIGHT))
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

# get a new font. 

while True: 
    if scene == 'StartMenu': 
        scene = startmenu.main_loop(WIN, MENUBACKGROUND)
    elif scene == "TypingGame":
        typinggame =  TypingGame(graph, STOPPED_MOVING, NEXT_ANIMATION, GAME_OVER)
        scene, score = typinggame.main_loop(WIN, game_alert, CLASSROOM)
        DataManager.upload_game_score(USERNAME, score)
    elif scene == "TypingTest": 
        typingtest = TypingTest()
        scene, words_per_minute, errors = typingtest.main_loop(WIN, MENUBACKGROUND)
        DataManager.upload_test_score(USERNAME, words_per_minute, errors)
    elif scene == "TestSummary": 
        # return wpm, errors and statistics 
        testsummarymenu.get_stats(words_per_minute, errors)
        scene = testsummarymenu.main_loop(WIN, MENUBACKGROUND)
    elif scene == "GameSummary": 
        # return score, record high score. 
        game_summary = GameSummaryMenu(score=typinggame.scoreboard.score)
        scene = game_summary.main_loop(WIN, MENUBACKGROUND)

