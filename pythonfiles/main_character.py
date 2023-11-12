import pygame

pygame.init()



class MainCharacter(pygame.sprite.Sprite):
    """Class to represent the user character"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.current_node = "17"


        self.image = pygame.transform.scale(pygame.image.load("./images/blue-devout/devouted-back/tile000.png"),
                                            (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (653, 749)

        self.animations = []
        self.next_positions = []  # implementing a stack
        self.animation_index = 0
        self.stopped_moving = False

    def update(self):
        """Updates the character to the new position"""
        if len(self.next_positions) == 0 and len(self.animations) > 0:
            # self.is_moving = False
            self.image = self.animations[0]
            self.animations = []
            self.stopped_moving = True

        elif len(self.next_positions) > 0 and len(self.animations) > 0:
            self.rect.center = self.next_positions[0]
            self.animation_index += 1
            if self.animation_index >= len(self.animations):
                self.animation_index = 0
            self.image = self.animations[self.animation_index]
            del self.next_positions[0]

    def movement_steps(self, next_node, next_position):
        """calculates the user next steps based on there current node and their next one"""
        self.current_node = next_node
        x_steps = (next_position[0] - self.rect.center[0]) / 6
        y_steps = (next_position[1] - self.rect.center[1]) / 6
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
        for i in range(1, 7):
            next_pos = ((i * x_steps) + self.rect.center[0], (i * y_steps) + self.rect.center[1])
            self.next_positions.append(next_pos)

    def get_animations(self, direction):
        path = f"./images/blue-devout/devouted-{direction}/"
        for i in range(3):  # could make this better for enemies (inheritance?)
            image = pygame.transform.scale(pygame.image.load(f"{path}tile00{i}.png"), (80, 80))
            self.animations.append(image)
