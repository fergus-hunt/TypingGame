import json

from databasemanager import DatabaseManager
from gamestages import *

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

CLASSROOM = pygame.image.load("..\\images\\backgrounds\\classroom4.png")
MENUBACKGROUND = pygame.transform.scale(pygame.image.load("..\\images\\backgrounds\\haunted_house.jpeg"), (WIDTH, HEIGHT))
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FONT = freetype.Font(None, 30)
FONT.origin = True

# all_texts = pygame.sprite.Group()

with open("../database/graph.json") as file:
    graph = json.loads(file.read())

scene = 'StartMenu'

# get a new font. 
clock = pygame.time.Clock()

while True:
    if scene == 'StartMenu':
        startmenu = StartMenu()
        scene = startmenu.main_loop(WIN, MENUBACKGROUND, clock)
    elif scene == "TypingGame":
        typinggame = TypingGame(graph)
        scene, score = typinggame.main_loop(WIN, CLASSROOM, clock)
        DataManager.upload_game_score(USERNAME, score)
    elif scene == "TypingTest":
        typingtest = TypingTest()
        scene, words_per_minute, errors = typingtest.main_loop(WIN, MENUBACKGROUND, clock)
        DataManager.upload_test_score(USERNAME, words_per_minute, errors)
    elif scene == "TestSummary":
        # return wpm, errors and statistics 
        testsummarymenu = TestSummaryMenu(words_per_minute, errors)
        scene = testsummarymenu.main_loop(WIN, MENUBACKGROUND, clock)
    elif scene == "GameSummary":
        # return score, record high score. 
        game_summary = GameSummaryMenu(score=typinggame.scoreboard.score)
        scene = game_summary.main_loop(WIN, MENUBACKGROUND, clock)
