import pygame, path, os


class GameEntity(pygame.sprite.Sprite): 
    def __init__(self, image_path, current_node, starting_coordinates, movement): 
        pygame.sprite.Sprite.__init__(self)
        self.current_node = current_node
        self.image_path = path.Path(image_path)
        self.image = pygame.transform.scale(pygame.image.load(f"{image_path}-left/" + (os.listdir(f"{image_path}-left/")[0])),(80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = starting_coordinates
        self.movement_speed = movement
        self.stopped_moving = False
        self.animations = []
        self.next_positions = []  # implementing a stack
        self.animation_index = 0

    def update(self):
        """Updates the character to the new position"""
        if len(self.next_positions) == 0 and len(self.animations) > 0:
            # self.is_moving = False
            self.image = self.animations[0]
            self.animations = []
            self.stopped_moving = True

        elif len(self.next_positions) > 0 and len(self.animations) > 0:
            self.animation_index += 1
            if self.animation_index >= len(self.animations):
                self.animation_index = 0
            self.image = self.animations[self.animation_index]
            self.rect.center = self.next_positions[0]
            del self.next_positions[0]

    def get_animations(self, direction):
        newPath = path.Path(f"{self.image_path}-{direction}/")
        print(newPath)
        for image in os.listdir(newPath):  # could make this better for enemies (inheritance?)
            pygameImage = pygame.transform.scale(pygame.image.load(f"{newPath}{image}"), (80, 80))
            self.animations.append(pygameImage)
