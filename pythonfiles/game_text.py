import pygame
import pygame.freetype
import random
import string

pygame.init()

class GameText(pygame.sprite.Sprite): # inheriting from pygame sprite 
    """renders new text, takes user key presses, analyses data"""
    def __init__(self, x, y, node, feature_control) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.feature_control = feature_control
        # initializing text from API 
        self.get_text()
        # loading user specific features 
        self.rect = self.feature_control.font_static.get_rect(self.text) 
        self.metrics = self.feature_control.font_static.get_metrics(self.text)

        self.next_key = 0
        # linked array to determine whether character's have been pressed 
        self.characters_unicode = [character for character in self.text]
        self.characters_completed = ["Na" for index in range(len(self.characters_unicode))]
        self.image = pygame.Surface(self.rect.size)
        self.image.set_colorkey((255, 0, 255))
        self.current_node = node
        self.baseline = self.rect.y
        self.rect.center = (x, y)

    def update(self): # Updating text 
        self.rendering_text()

    def characters_reset(self): 
        """Resets the text if the user got letter wrong"""
        for index in range(len(self.characters_completed)):
            self.characters_completed[index] = "Na"

    def get_text(self):
        """Generate the new text for object"""
        self.text = ""
        for i in range(2):
            # making random character 
            num = random.randint(0, 25)
            self.text += string.ascii_lowercase[num]

    def rendering_text(self): 
        """Renders the new text, and changes colour based on whether it's status"""
        x_val = 0
        self.image.fill((255, 0, 255))
        # could make quicker here.
        for index, metric in zip(range(len(self.characters_unicode)), self.metrics):
            character = self.characters_unicode[index]
            # rendering the correct colour based on user input. 
            if self.characters_completed[index] == "Na":
                self.feature_control.font_static.render_to(self.image, (x_val, self.baseline), character, self.feature_control.colour)
                x_val += metric[4]
            elif self.characters_completed[index]:
                self.feature_control.font_static.render_to(self.image, (x_val, self.baseline), character, "green")
                x_val += metric[4]

