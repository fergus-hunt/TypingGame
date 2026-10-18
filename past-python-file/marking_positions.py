import pygame

FPS = 60
HEIGHT = 800
WIDTH = 1100


# class thing(pygame.sprite.Sprite): 
#     def __init__(self, height, width): 
#         super().__init__() 

#         self.image = pygame.transform.scale(pygame.image.load("images/teacher.jpeg"), (width,height))
#         self.rect = pygame.rect.Rect(0, 0, width, height)
        # pygame.draw.rect(self.image,'black', self.rect) 

# object.rect.x = 200
# object.rect.y = 200
# object = thing(100, 100)
# all_sprites_list = pygame.sprite.Group() 
# all_sprites_list.add(object)
  
# fire_golem = pygame.transform.scale(pygame.image.load("images/fire_golem_clear.png"), (100, 100))
CLASSROOM=pygame.transform.scale(pygame.image.load("secondentiremap.png"), (WIDTH, HEIGHT -50 ))
# fire_golem = pygame.sprite.Sprite()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock() 
student_positions = []
counter = -1
while True: 
    CLOCK.tick(FPS)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            with open("position.txt", 'w') as file: 
                students = "\n".join(student_positions)
                file.write(students)
            pygame.quit() 
    
        if event.type == pygame.MOUSEBUTTONDOWN: 
            counter += 1
            if counter == 0: 
                student_positions.append("seat,x,y")
            (mouseX, mouseY) = pygame.mouse.get_pos()
            student_positions.append((f"{counter},{mouseX},{mouseY}"))
    WIN.fill('black')
    WIN.blit(CLASSROOM, (0, 50))
    pygame.display.update()


# fire_golem = pygame.transform.scale(pygame.image.load("images/fire_golem_clear.png"), (100, 100))
# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# CLOCK = pygame.time.Clock() 
# student_positions = []
# counter = -1
# while True: 
#     CLOCK.tick(FPS)
#     for event in pygame.event.get(): 
#         if event.type == pygame.QUIT: 
#             with open("position.txt", 'w') as file: 
#                 students = "\n".join(student_positions)
#                 file.write(students)
#             pygame.quit() 
#         if event.type == pygame.MOUSEBUTTONDOWN: 
#             counter += 1
#             if counter == 0: 
#                 student_positions.append("seat,x,y")
#             (mouseX, mouseY) = pygame.mouse.get_pos()
#             student_positions.append((f"{counter},{mouseX},{mouseY}"))
#     WIN.fill('black')
#     WIN.blit(CLASSROOM, (0, 50))
#     pygame.display.update()