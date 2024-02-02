import pandas, json, numpy
import pygame

SEAT_WIDTH = 7

def get_distances(positions): 
    df = positions
    dict = {}
    for row in df.keys(): 
        seat_number = int(row)
        if seat_number % SEAT_WIDTH == 0 or seat_number == 0: 
            if seat_number == 21: 
                neighbours = [22, 14]
            elif  seat_number == 0: 
                neighbours = [1, SEAT_WIDTH]
            else: 
                neighbours = [seat_number + 1, seat_number - SEAT_WIDTH, seat_number + SEAT_WIDTH]

        elif seat_number % SEAT_WIDTH == 6: 
            if seat_number == 6: 
                neighbours = [seat_number - 1, seat_number + SEAT_WIDTH]
            elif seat_number == 27:
                neighbours = [seat_number -1, seat_number-SEAT_WIDTH]
            else: 
                neighbours = [seat_number - 1, seat_number + SEAT_WIDTH, seat_number - SEAT_WIDTH]
            
        elif seat_number >20: 
            neighbours = [seat_number + 1, seat_number -1 , seat_number - SEAT_WIDTH]
        elif seat_number < SEAT_WIDTH: 
            neighbours = [seat_number + 1, seat_number -1, seat_number + SEAT_WIDTH]
        else: 
            neighbours = [seat_number + 1, seat_number -1, seat_number + SEAT_WIDTH, seat_number - SEAT_WIDTH]
        print("Neightbours: ", neighbours)
        connections = {}
        for person in neighbours:
            
            tuuple = df[(person)]
            print(tuuple)
            x = tuuple[0] - df[row][0]
            y = tuuple[1] - df[row][1]
            print(x, y)
            hypot = (x*x + y*y)
            distance = (numpy.sqrt(hypot))
            connections[person] = distance

        dict[f"{seat_number}"] = connections
    json_whole = {"positions": positions, "distances": dict}
    json_hwat = json.dumps(json_whole)
    with open("temporary.json", "w") as file: 
        file.write(json_hwat)

FPS = 60
HEIGHT = 965
WIDTH = 1282


all_positions = {}

  
CLASSROOM=(pygame.image.load("./images/classroom4.png"))
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock() 


counter = -1
while True: 
    CLOCK.tick(FPS)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            file = pandas.DataFrame((all_positions))
            jsonstuff = json.dumps(all_positions)
            print(jsonstuff)
            get_distances(all_positions)
            pygame.quit() 
    
        if event.type == pygame.MOUSEBUTTONDOWN: 
            counter += 1
            (mouseX, mouseY) = pygame.mouse.get_pos()
            all_positions[counter] = [mouseX, mouseY]
    WIN.fill('black')
    WIN.blit(CLASSROOM, (0, 50))
    pygame.display.update()

















