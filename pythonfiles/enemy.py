import pygame
from game_entity import GameEntity


class Enemy(GameEntity):
    def __init__(self): 
        GameEntity.__init__(self, f"./images/enemy-skeleton/skeleton", "1", (177,504), 20)
        self.path = []
        self.stopped_moving = True

    def movement_steps(self, next_position):
        # del self.path[-1]
        # self.current_node = self.next_node
        # self.next_node = self.path[-1]
        """calculates the user next steps based on there current node and their next one"""
        # self.current_node = self.next_node
        x_steps = (next_position[0] - self.rect.center[0]) / self.movement_speed
        y_steps = (next_position[1] - self.rect.center[1]) / self.movement_speed
        if (abs(x_steps)) > abs(y_steps):
            if x_steps < 0:
                self.get_animations("left")
            else:
                self.get_animations("right")
        else:
            if y_steps < 0:
                self.get_animations("left")
            else:
                self.get_animations("right")
        for i in range(1, self.movement_speed + 1):
            next_pos = ((i * x_steps) + self.rect.center[0], (i * y_steps) + self.rect.center[1])
            self.next_positions.append(next_pos)

