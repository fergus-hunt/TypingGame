import pandas, json, time, numpy
import pygame



def get_distances(): 
    with open("positions.json", "r") as file: 
        df = json.loads(file.read())
    print(df)
    dict = {}
    for row in df.keys(): 
        seat_number = int(row)
        if seat_number % 7 == 0 or seat_number == 0: 
            if seat_number == 21: 
                neighbours = [22, 14]
            elif  seat_number == 0: 
                neighbours = [1, 7]
            else: 
                neighbours = [seat_number + 1, seat_number - 7, seat_number + 7]

        elif seat_number % 7 == 6: 
            if seat_number == 6: 
                neighbours = [seat_number - 1, seat_number + 7]
            elif seat_number == 27:
                neighbours = [seat_number -1, seat_number-7]
            else: 
                neighbours = [seat_number - 1, seat_number + 7, seat_number - 7]
            
        elif seat_number >20: 
            neighbours = [seat_number + 1, seat_number -1 , seat_number - 7]
        else: 
            neighbours = [seat_number + 1, seat_number -1, seat_number + 7, seat_number - 7]

        connections = {}
        for person in neighbours:
            
            tuuple = df[str(person)]
            print(tuuple)
            x = tuuple[0]
            y = tuuple[1]
            print(x, y)
            hypot = (x*x + y*y)
            distance = (numpy.sqrt(hypot))
            connections[f"{seat_number}"] = hypot

        dict[f"{seat_number}"] = connections
        print(dict)

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
            with open("positions.json", "w") as newfile: 
                newfile.write(jsonstuff)
            # time.sleep(5)
            get_distances()
            pygame.quit() 
    
        if event.type == pygame.MOUSEBUTTONDOWN: 
            counter += 1
            (mouseX, mouseY) = pygame.mouse.get_pos()
            all_positions[counter] = [mouseX, mouseY]
    WIN.fill('black')
    WIN.blit(CLASSROOM, (0, 50))
    pygame.display.update()

















