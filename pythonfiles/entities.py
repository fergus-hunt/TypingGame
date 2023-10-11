import pygame, pandas

pygame.init() 

class Student(pygame.sprite.Sprite):
     
    def __init__(self, image, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image), (50, 50))
        self.rect =self.image.get_rect()
        self.rect.center = (x, y)


class Teacher(pygame.sprite.Sprite): 
    def __init__(self, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.current_animation = "idle"
        self.idle_images = self.get_images("images/idle-teacher", 4)
        self.dying_images = self.get_images("images/teacher-death", 8)
        self.animations = {
            "dying":self.dying_images,
            "idle":self.idle_images, 
        }
        self.image = self.animations[self.current_animation][0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def get_images(self, path, size):
        image_list = [] 
        for i in range(size): 
            if i < 10: 
                image_path = f"{path}/tile00{i}.png"
            else: 
                image_path = f"{path}/tile0{i}.png"
            image = pygame.transform.scale(pygame.image.load(image_path), (100, 100))
            image_list.append(image)
        return image_list
    
    def update(self): 
        self.image = self.animations[self.current_animation][self.frame]
        self.frame += 1
        if self.frame >= len(self.animations[self.current_animation]): 
            if self.current_animation == "dying": 
                self.kill()
            self.frame= 0
