import pygame, sys, json, pprint

class Enemy(pygame.sprite.Sprite): 
    def __init__(self, graph): 
        pygame.sprite.Sprite.__init__(self)
        
        self.df = graph
        self.current_node = "0"
        self.next_node = "1"
        self.path = []
        self.next_positions = []


        
        self.movement_speed = 20
        self.animations = []
        self.get_animations("right")
        self.animation_index = 0
        self.image = self.animations[self.animation_index]
        self.rect =self.image.get_rect()
        self.rect.center = (self.df['positions'][f"{self.current_node}"])

    def get_animations(self, direction): 

        path = f"./images/enemy-skeleton/skeleton-{direction}/"
        for i in range(12): 
            if i >= 10: 
                image = pygame.transform.scale(pygame.image.load(f"{path}tile0{i}.png"), (192, 192))
            else:
                image = pygame.transform.scale(pygame.image.load(f"{path}tile00{i}.png"), (192, 192))
            self.animations.append(image)
        
    def update(self): 
        
            if len(self.next_positions) == 0: 
                self.animations = []
                self.current_node = self.path[-1]
                self.next_node = self.path[-2]
                del self.path[-1]
                self.enemymovements()
            else: 
                self.animation_index += 1
                if self.animation_index >= len(self.animations): 
                    self.animation_index = 0
                self.image = self.animations[self.animation_index]
                self.rect.center = self.next_positions[0] # moving the enemy foward 
                del self.next_positions[0]

    def enemymovements(self): # splits up the movement from current node to next node
        current_position = self.df['positions'][f"{self.current_node}"]
        next_position = self.df['positions'][f"{self.next_node}"]
        x_denoms = (next_position[0] - current_position[0])/self.movement_speed
        y_denoms = (next_position[1] - current_position[1])/self.movement_speed

        if (abs(x_denoms)) > abs(y_denoms): 
            if x_denoms < 0: 
                self.get_animations("left")
            else: 
                self.get_animations("right")
        else: 
            if y_denoms < 0:
                self.get_animations("right")
            else: 
                self.get_animations("left")

        for i in range(1, self.movement_speed+1): 
            next_pos = (round((i * x_denoms) + current_position[0], 2), round((i * y_denoms) + current_position[1], 2))
            self.next_positions.append(next_pos)
        
   