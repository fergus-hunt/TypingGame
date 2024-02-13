import json, pygame
from tkinter import messagebox
from pygame import freetype

from database_manager import *
from result_viewer import ResultViewer



from menu import Menu # adding menu functionality

from menu_feature import MenuFeature
from user_manager import UserManager
from typing_test import TypingTest
from typing_game import TypingGame
from feature_control import FeatureControl
import threading
from settings import Settings
freetype.init()



# Login = UserManager()
# Login.log_in_user()
# Login.root.mainloop()
# USERNAME = Login.username

USERNAME = "Fergus"

pygame.init() # initialising pygame modules 
HEIGHT = 965 # global constant for all pygame windows 
WIDTH = 1285 # global constant for all pygame windows 
CLASSROOM = pygame.image.load(".\\images\\backgrounds\\classroom4.png") # Constnat background 
MENUBACKGROUND = pygame.transform.scale(pygame.image.load(".\\images\\backgrounds\\haunted_house.jpeg"), (WIDTH, HEIGHT)) # constant background 
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Constant window for all pygame stages 
SCENE = 'StartMenu' # Current game state, dictates what window will be shown. 
CLOCK = pygame.time.Clock() # Global constant


# FONT = freetype.Font(".\\images\\scary_font.ttf", 30)
# FONT.origin = True
MainThread = threading.current_thread() # making the thread for pygame windows. 
# MainThread.start()
# all_texts = pygame.sprite.Group(


with open("./database/graph.json") as file: # Variable stores the distance and connections between all nodes / checkpoints
    graph = json.loads(file.read())

FEATURE_CONTROL = FeatureControl() # class that read/writes to and frame settings_options, controls user-specific features. 
# def make_result_thread(columns, results, thread):
#     results = ResultViewer(columns, results, FEATURE_CONTROL)
#     results.mainloop()
#     # thread.join()
#     if thread.is_alive(): 
#         thread.join()
    
# get a new font.

    


while True: # Main game loop, this is how different game stages are reached, moving between menu's 
    
    # message = f"Game Stage is : {SCENE}" # testing strategy 
    # messagebox.showinfo(title="Testing", message=message) # This shows the curretn game stage, ensures SCENE is changing correctly

    # SCENE = "StartMenu"
    if SCENE == 'StartMenu':
        start_menu = Menu()
        start_menu.add_button("TypingGame", MenuFeature("Play Game", WIDTH/2, HEIGHT * 0.25, FEATURE_CONTROL)) # Button to play game 
        start_menu.add_button("TypingTest", MenuFeature( "Take Test", WIDTH *1/3, HEIGHT / 2, FEATURE_CONTROL)) # button to take test 
        start_menu.add_button("ResultViewerTest", MenuFeature("View Test Stats", WIDTH*2/3, 0.75 * HEIGHT, FEATURE_CONTROL)) # button to view test results 
        start_menu.add_button("ResultViewerGame", MenuFeature("View Game Stats", WIDTH / 3, 0.75 * HEIGHT, FEATURE_CONTROL))# button to view game results 
        start_menu.add_button("ChangeSettings", MenuFeature("ChangeSettings", WIDTH *2/3, 0.5 * HEIGHT, FEATURE_CONTROL))# button to change game features. 
        SCENE = start_menu.main_loop(WIN, MENUBACKGROUND, CLOCK)
        
        
        
    elif SCENE == "TypingGame":
        typing_game = TypingGame(graph, FEATURE_CONTROL)
        SCENE, score = typing_game.main_loop(WIN, CLASSROOM, CLOCK)
        upload_game_score(USERNAME, score)
    elif SCENE == "TypingTest":
        typing_test = TypingTest(FEATURE_CONTROL)
        SCENE, words_per_minute, errors = typing_test.main_loop(WIN, MENUBACKGROUND, CLOCK)
        upload_test_score(USERNAME, words_per_minute, errors)
    elif SCENE == "TestSummary":
        # return wpm, errors and statistics 
        # test_summary = TestSummaryMenu(words_per_minute, errors)
        test_summary = Menu()
        test_summary.add_title(MenuFeature(f"WPM : {words_per_minute}", WIDTH / 2, (HEIGHT/2), FEATURE_CONTROL))
        test_summary.add_title(MenuFeature(f"ERRORS : {errors}", WIDTH / 2, HEIGHT/4, FEATURE_CONTROL))
        test_summary.add_button("StartMenu", MenuFeature("Main Menu", WIDTH *2/3, 0.75 * HEIGHT, FEATURE_CONTROL))
        test_summary.add_button("TypingTest", MenuFeature("Play Again", WIDTH / 3, 0.75 * HEIGHT, FEATURE_CONTROL))
        SCENE = test_summary.main_loop(WIN, MENUBACKGROUND, CLOCK)
    elif SCENE == "GameSummary":
        # return score, record high score. 
        # game_summary = GameSummaryMenu(score=typing_game.scoreboard.score)
        game_summary = Menu()
        game_summary.add_title(MenuFeature(f"Score : {score}", WIDTH / 2, (HEIGHT*0.75), FEATURE_CONTROL))
        game_summary.add_button("StartMenu", MenuFeature(f"Main Menu", WIDTH / 2, HEIGHT/2, FEATURE_CONTROL))
        game_summary.add_button("TypingGame", MenuFeature("Play again", WIDTH / 2, 0.25 * HEIGHT, FEATURE_CONTROL))
        SCENE = game_summary.main_loop(WIN, MENUBACKGROUND, CLOCK)#
        
    # showing test results 
    elif SCENE == "ResultViewerTest":
        SCENE = "StartMenu" # when tkinter window quits start menu is loaded
        columns = ("username", "wpm", "errors", "Date") # columns within database 
        test_scores = get_user_test_scores(USERNAME) # getting results from database 
        results = ResultViewer(columns, test_scores, FEATURE_CONTROL)
        results.mainloop()
        
    # showing game results 
    elif SCENE == "ResultViewerGame":
        SCENE = "StartMenu" # when tkinter window quits start menu is loaded
        columns = ("username", "Score", "Date") # Columns within database 
        game_scores = get_user_game_scores(USERNAME) # getting results from database 
        results = ResultViewer(columns, game_scores, FEATURE_CONTROL)
        results.mainloop() 
        
    elif SCENE == "ChangeSettings":
        SCENE = "StartMenu"
        example = Settings()
        example.mainloop()
        example.destroy()

        FEATURE_CONTROL.reset()

