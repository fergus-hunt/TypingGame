import pygame, json
from pygame import freetype


class FeatureControl:  
    """Contains the user features"""
    def __init__(self): # User specific settings  
        self.keysound = None
        self.font_static = None
        self.font_dynamic = None
        self.colour = None
        self.music = None
        
        
        
        
        self.reset()

    def reset(self): 
        """Load the settings from JSON file and changing attributes"""
        with open(".\\database\\user_settings.json", "r") as file: 
            ALL_SETTINGS= json.loads(file.read()) #Creating dictionary for user settings 

        # initializing attributes to the user specific settings
        self.keysound = pygame.mixer.Sound(ALL_SETTINGS["Keysound"])
        self.font_static = freetype.Font(ALL_SETTINGS["Font"], 50)
        self.font_static.origin = True
        self.font_dynamic = freetype.Font(ALL_SETTINGS["Font"], 75)
        self.colour = ALL_SETTINGS["Colour"]
        self.music = pygame.mixer.Sound(ALL_SETTINGS["Music"])
        
