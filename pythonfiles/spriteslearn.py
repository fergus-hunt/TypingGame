import pygame 

pygame.init() 
FPS = 10
HEIGHT = 800
WIDTH = 1100


class Wraith(pygame.sprite.Sprite): 
    def __init__(self, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.image_collection = []
        self.image_collection.append(pygame.transform.scale(pygame.image.load("images/organised/teacher.png"), (50, 50)))
        self.image_index = 0
        self.rect =self.image.get_rect()
        self.rect.center = (x, y)

    def update(self): 
        self.rect.move_ip(0, 1)
        
        # self.filling_image.blit(self.)

    def get_idle_images


square = Square( 500, 300)
squares = pygame.sprite.Group()
squares.add(square)



screen = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock() 

while True: 
    CLOCK.tick(FPS)
    screen.fill('black')

    squares.update()
    squares.draw(screen) 
    
    print(squares)
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit() 
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            pos = pygame.mouse.get_pos()
            square = Square( pos[0], pos[1])
            squares.add(square)
    
    pygame.display.update()