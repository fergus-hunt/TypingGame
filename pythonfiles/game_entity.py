import pygame, path, os


class GameEntity(pygame.sprite.Sprite): # inheriting from pygame sprite 
    """used for on screen, moving objects"""
    def __init__(self, image_path, current_node, starting_coordinates, movement):
        """Initializing attributes that determine behaviour""" 
        pygame.sprite.Sprite.__init__(self)
        self.current_node = current_node
        self.image_path = path.Path(image_path) 
        self.image = pygame.transform.scale(
            pygame.image.load(
                f"{image_path}-left/" + (os.listdir(f"{image_path}-left/")[0])
                ),(80, 80)
            ) # starting image
        self.rect = self.image.get_rect()
        self.rect.center = starting_coordinates
        self.movement_speed = movement 
        self.stopped_moving = False
        self.animations = [] # queue for images to show animation 
        self.next_positions = []  # Using stack for positioning 
        self.animation_index = 0 # stack pointer 

    def update(self):
        """Updates the character to the new position"""
        if len(self.next_positions) == 0 and len(self.animations) > 0: # no  more positions 
            self.image = self.animations[0]  
            self.animations = []
            self.stopped_moving = True 

        elif len(self.next_positions) > 0 and len(self.animations) > 0:
            self.animation_index += 1
            if self.animation_index >= len(self.animations):
                self.animation_index = 0
            self.image = self.animations[self.animation_index] # dequeing from circular for next animation
            self.rect.center = self.next_positions[0] # popping from stack, nextp position
            del self.next_positions[0]

    def get_animations(self, direction):
        """When entity begins moving in another direction, the correct animations are fetched and loaded 
        into a queue"""
        newPath = path.Path(f"{self.image_path}-{direction}/") # changing direction 
        for image in os.listdir(newPath):  # loadin the images into array to show moving animation
            pygameImage = pygame.transform.scale(pygame.image.load(f"{newPath}{image}"), (80, 80))
            self.animations.append(pygameImage)
