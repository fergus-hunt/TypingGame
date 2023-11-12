import json, pygame
from pygame import freetype

from database_manager import DatabaseManager
from test_summary_menu import TestSummaryMenu
from game_summary_menu import GameSummaryMenu
from main_menu import MainMenu
from typing_test import TypingTest
from typing_game import TypingGame

pygame.init()
freetype.init()

data_manager = DatabaseManager()

# Login = AuthenticateUser(database_manager=DatabaseManager)
# Login.log_in_user()
# Login.root.mainloop()
# USERNAME = Login.username

USERNAME = "Fergus"

pygame.init()
# FPS = 20
HEIGHT = 965
WIDTH = 1285
FONT = freetype.Font(None, 30)
FONT.origin = True

CLASSROOM = pygame.image.load(".\\images\\backgrounds\\classroom4.png")
MENUBACKGROUND = pygame.transform.scale(pygame.image.load(".\\images\\backgrounds\\haunted_house.jpeg"), (WIDTH, HEIGHT))
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


# all_texts = pygame.sprite.Group()

with open("./database/graph.json") as file:
    graph = json.loads(file.read())

scene = 'StartMenu'

# get a new font. 
clock = pygame.time.Clock()

while True:
    if scene == 'StartMenu':
        start_menu = MainMenu()
        scene = start_menu.main_loop(WIN, MENUBACKGROUND, clock)
    elif scene == "TypingGame":
        typing_game = TypingGame(graph)
        scene, score = typing_game.main_loop(WIN, CLASSROOM, clock)
        data_manager.upload_game_score(USERNAME, score)
    elif scene == "TypingTest":
        typing_test = TypingTest()
        scene, words_per_minute, errors = typing_test.main_loop(WIN, MENUBACKGROUND, clock)
        data_manager.upload_test_score(USERNAME, words_per_minute, errors)
    elif scene == "TestSummary":
        # return wpm, errors and statistics 
        test_summary = TestSummaryMenu(words_per_minute, errors)
        scene = test_summary.main_loop(WIN, MENUBACKGROUND, clock)
    elif scene == "GameSummary":
        # return score, record high score. 
        game_summary = GameSummaryMenu(score=typing_game.scoreboard.score)
        scene = game_summary.main_loop(WIN, MENUBACKGROUND, clock)
