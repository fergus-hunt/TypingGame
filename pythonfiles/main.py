import json, pygame
from pygame import freetype

from database_manager import *
from result_viewer import ResultViewer
from menu import Menu
from button import Button
from user_manager import UserManager
from typing_test import TypingTest
from typing_game import TypingGame
import threading

pygame.init()
freetype.init()



# Login = UserManager()
# Login.log_in_user()
# Login.root.mainloop()
# USERNAME = Login.username

USERNAME = "Fergus"

pygame.init()
HEIGHT = 965
WIDTH = 1285
FONT = freetype.Font(".\\images\\scary_font.ttf", 30)
FONT.origin = True
MainThread = threading.current_thread()
# MainThread.start()

CLASSROOM = pygame.image.load(".\\images\\backgrounds\\classroom4.png")
MENUBACKGROUND = pygame.transform.scale(pygame.image.load(".\\images\\backgrounds\\haunted_house.jpeg"), (WIDTH, HEIGHT))
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


# all_texts = pygame.sprite.Group(

with open("./database/graph.json") as file:
    graph = json.loads(file.read())

scene = 'StartMenu'
def make_result_thread(columns, results, thread):
    results = ResultViewer(columns, results)
    results.mainloop()
    # thread.join()
    if thread.is_alive(): 
        thread.join()
    
# get a new font.
CLOCK = pygame.time.Clock()

while True:
    if scene == 'StartMenu':
        start_menu = Menu()
        start_menu.add_button("TypingGame", Button("Play Game", WIDTH/2, HEIGHT * 0.25))
        start_menu.add_button("TypingTest", Button( "Take Test", WIDTH / 2, HEIGHT / 2))
        start_menu.add_button("ResultViewerTest", Button("View Test Stats", WIDTH*2/3, 0.75 * HEIGHT))
        start_menu.add_button("ResultViewerGame", Button("View Game Stats", WIDTH / 3, 0.75 * HEIGHT))
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
        # test_summary = TestSummaryMenu(words_per_minute, errors)
        test_summary = Menu()
        test_summary.add_title(Button(f"WPM : {words_per_minute}", WIDTH / 2, (HEIGHT/2)))
        test_summary.add_title(Button(f"ERRORS : {errors}", WIDTH / 2, HEIGHT/4))
        test_summary.add_button("StartMenu", Button("Main Menu", WIDTH *2/3, 0.75 * HEIGHT))
        test_summary.add_button("TypingTest", Button("Play Again", WIDTH / 3, 0.75 * HEIGHT))
        scene = test_summary.main_loop(WIN, MENUBACKGROUND, CLOCK)
    elif scene == "GameSummary":
        # return score, record high score. 
        # game_summary = GameSummaryMenu(score=typing_game.scoreboard.score)
        game_summary = Menu()
        game_summary.add_title(Button(f"Score : {score}", WIDTH / 2, (HEIGHT*0.75)))
        game_summary.add_button("StartMenu", Button(f"Main Menu", WIDTH / 2, HEIGHT/2))
        game_summary.add_button("TypingGame", Button("Play again", WIDTH / 2, 0.25 * HEIGHT))
        scene = game_summary.main_loop(WIN, MENUBACKGROUND, CLOCK)
    elif scene == "ResultViewerTest":
        test_scores = get_user_test_scores(USERNAME)
        scene = "StartMenu"
        result_thread = threading.Thread()
        result_thread = threading.Thread(target=make_result_thread, kwargs={"columns": ("username", "wpm", "errors", "Date"), "results":test_scores, "thread":result_thread})
        result_thread.start()
    elif scene == "ResultViewerGame":
        game_scores = get_user_game_scores(USERNAME)
        scene = "StartMenu"
        result_thread = threading.Thread()
        result_thread = threading.Thread(target=make_result_thread, kwargs={"columns": ("username", "score", "Date"), "results":game_scores, "thread":result_thread})
        result_thread.start()

        # show_results(("username", "score", "Date"),game_scores)
        # results = ResultViewer(("username", "score", "Date"),game_scores)