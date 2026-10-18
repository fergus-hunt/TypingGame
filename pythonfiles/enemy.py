
from game_entity import GameEntity


class Enemy(GameEntity): # Inheriting from game entity 
    def __init__(self): 
        GameEntity.__init__(self, f"./images/enemy-skeleton/skeleton", "0", (177,504), 20)
        self.path = [] # Array of nodes 
        self.stopped_moving = True # is moving

    def movement_steps(self, next_position):
        """calculates the next steps based on there current node and their next one in the path"""
        x_steps = (next_position[0] - self.rect.center[0]) / self.movement_speed # X positions between current and next node 
        y_steps = (next_position[1] - self.rect.center[1]) / self.movement_speed # # X positions between current and next node 
        if (abs(x_steps)) > abs(y_steps): # determining the direction of travel
            if x_steps < 0:
                self.get_animations("left") 
            else:
                self.get_animations("right")
        else:
            if y_steps < 0:
                self.get_animations("left")
            else:
                self.get_animations("right")
        for i in range(1, self.movement_speed + 1): # adding the x and y positions to path
            next_pos = ((i * x_steps) + self.rect.center[0], (i * y_steps) + self.rect.center[1])
            self.next_positions.append(next_pos)

