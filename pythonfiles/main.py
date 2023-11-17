import json, pygame
from pygame import freetype

from database_manager import *
from result_viewer import ResultViewer
from menu import Menu
from button import Button
from user_manager import UserManager
from test_summary_menu import TestSummaryMenu
from game_summary_menu import GameSummaryMenu
from main_menu import MainMenu
from typing_test import TypingTest
from typing_game import TypingGame

pygame.init()
freetype.init()



# Login = UserManager(database_manager=DatabaseManager)
# Login.log_in_user()
# Login.root.mainloop()
# USERNAME = Login.username

USERNAME = "Fergus"

pygame.init()
HEIGHT = 965
WIDTH = 1285
FONT = freetype.Font(".\\images\\scary_font.ttf", 30)
FONT.origin = True

CLASSROOM = pygame.image.load(".\\images\\backgrounds\\classroom4.png")
MENUBACKGROUND = pygame.transform.scale(pygame.image.load(".\\images\\backgrounds\\haunted_house.jpeg"), (WIDTH, HEIGHT))
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


# all_texts = pygame.sprite.Group()

with open("./database/graph.json") as file:
    graph = json.loads(file.read())

scene = 'StartMenu'

# get a new font.
CLOCK = pygame.time.Clock()

while True:
    if scene == 'StartMenu':
        start_menu = Menu()
        start_menu.add_button("TypingGame", Button("Play Game", WIDTH/2, HEIGHT * 0.25))
        start_menu.add_button("TypingTest", Button( "Take Test", WIDTH / 2, HEIGHT / 2))
        start_menu.add_button("ResultViewer", Button("View Stats", WIDTH / 2, 0.75 * HEIGHT))
        
        scene = start_menu.main_loop(WIN, MENUBACKGROUND, CLOCK)
    elif scene == "TypingGame":
        typing_game = TypingGame(graph)
        scene, score = typing_game.main_loop(WIN, CLASSROOM, CLOCK)
        upload_game_score(USERNAME, score)
    elif scene == "TypingTest":
        typing_test = TypingTest()
        scene, words_per_minute, errors = typing_test.main_loop(WIN, MENUBACKGROUND, CLOCK)
        upload_test_score(USERNAME, words_per_minute, errors)
    elif scene == "TestSummary":
        # return wpm, errors and statistics 
        test_summary = TestSummaryMenu(words_per_minute, errors)
        scene = test_summary.main_loop(WIN, MENUBACKGROUND, CLOCK)
    elif scene == "GameSummary":
        # return score, record high score. 
        game_summary = GameSummaryMenu(score=typing_game.scoreboard.score)
        scene = game_summary.main_loop(WIN, MENUBACKGROUND, CLOCK)
    elif scene == "ResultViewer":
        userresult = get_user_game_scores(USERNAME)
        results = ResultViewer(userresult)
        scene = "StartMenu"
