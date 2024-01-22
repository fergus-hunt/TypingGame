from pygame import freetype 
import pygame 
from button import MenuFeature

pygame.init()

class Menu:
    def __init__(self) -> None:
        self.button_dict = {} # Buttons that will be interactive on menu 
        self.title_array = [] # On screen text that will show information 
    
    def add_button(self, command, button): # Add different buttons for different purposes. 
        self.button_dict[command] = button 

    def add_title(self, title): # add different titles to display information
        self.title_array.append(title) # Adding title 
    
    def main_loop(self, screen, background, clock): # What makes menu interactive
        """Main pygame loop, shows buttons to play game, take the test and view user statistics"""
        while True:
            clock.tick(60)
            for event in pygame.event.get(): # Iterating through all events 
                if event.type == pygame.QUIT: # registering quit event
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN: # checking for any event that would classify as button being pressed
                    for command in self.button_dict: # iterating through the buttons 
                        if self.button_dict[command].rect.collidepoint(event.pos): # checking if mouse button was within button borders. 
                            return command # changing the game state 

            screen.fill('black') # covering up previous frame actions. 
            screen.blit(background, (0, 0)) # loading background
            for button in self.button_dict.values(): 
                button.update(screen) # rendering all buttons on new screen 
            
            for title in self.title_array: # rending all information on screen 
                title.update(screen)
            pygame.display.update() # updating new screen 



