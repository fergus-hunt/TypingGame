import pygame
from game_entity import GameEntity

pygame.init()




class MainCharacter(GameEntity):
    """Class to represent the user character"""

    def __init__(self):
        GameEntity.__init__(self, "./images/blue-devout/devouted", 17, (653, 749), 6)
        

    
    def movement_steps(self, next_node, next_position):
        """calculates the user next steps based on there current node and their next one"""
        self.current_node = next_node
        x_steps = (next_position[0] - self.rect.center[0]) / self.movement_speed
        y_steps = (next_position[1] - self.rect.center[1]) / self.movement_speed
        if (abs(x_steps)) > abs(y_steps):
            if x_steps < 0:
                self.get_animations("left")
            else:
                self.get_animations("right")
        else:
            if y_steps < 0:
                self.get_animations("back")
            else:
                self.get_animations("forward")
        for i in range(1, self.movement_speed + 1):
            next_pos = ((i * x_steps) + self.rect.center[0], (i * y_steps) + self.rect.center[1])
            self.next_positions.append(next_pos)