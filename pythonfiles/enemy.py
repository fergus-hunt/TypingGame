import pygame, sys, json, pprint

class Enemy(pygame.sprite.Sprite): 
    def __init__(self, graph, game_over_event): 
        pygame.sprite.Sprite.__init__(self)
        self.GAME_OVER = game_over_event
        
        self.df = graph
        self.current_node = "0"
        self.user_found = False
        self.user_node = "12"


        # self.frame = 0
        self.current_animation = "idle" # animation status
        self.attacking_images = self.get_images("images/undead-executioner-attack", 13)
        self.idle_images = self.get_images("images/undead-executioner-idle", 4)
        self.animations = {
            "attacking": self.attacking_images, 
            "idle": self.idle_images
        }
        
        self.movement_speed = 20

        self.image = self.animations[self.current_animation][0]
        self.rect =self.image.get_rect()
        self.rect.center = (self.df['positions'][f"{self.current_node}"])

        self.path = self.find_user_path()
        self.next_positions = self.calculate_enemy_movement()
        


    def get_images(self, path, size):
        image_list = [] 
        for i in range(size): 
            if i < 10: 
                image_path = f"{path}/tile00{i}.png"
            else: 
                image_path = f"{path}/tile0{i}.png"
            image = pygame.transform.scale(pygame.image.load(image_path), (150, 150))
            image_list.append(image)
        return image_list
        
    def update(self): 
        # self.image = self.animations[self.current_animation][self.frame]
        # self.frame += 1
        # if self.frame >= len(self.animations[self.current_animation]): 
        #     self.frame= 0
        #     self.current_animation = "idle"
        if self.current_node != self.user_node and not self.user_found: 
            if len(self.next_positions) == 0: 
                self.current_node = self.path[-2] # current enemy node
                self.path = self.find_user_path()
                self.next_positions = self.calculate_enemy_movement()
            else: 
                print(self.next_positions)
                self.rect.center = self.next_positions[0] # moving the enemy foward 
                del self.next_positions[0]
        else: 
            self.user_found = True # seeing whether user has been caught
            pygame.event.post(pygame.event.Event(self.GAME_OVER, myevent="bastard"))

    def calculate_enemy_movement(self): # splits up the movement from current node to next node
        current = self.current_node 
        next = self.path[-2]
        current_position = self.df['positions'][f"{current}"]
        next_position = self.df['positions'][f"{next}"]
        x_denoms = (next_position[0] - current_position[0])/self.movement_speed
        y_denoms = (next_position[1] - current_position[1])/self.movement_speed
        print(f"XDenoms: {x_denoms}\tYDENOMS: {y_denoms}")#
        temp_list = []
        for i in range(1, self.movement_speed+1): 
            next_pos = (round((i * x_denoms) + current_position[0], 2), round((i * y_denoms) + current_position[1], 2))

            temp_list.append(next_pos)
        return temp_list


    def find_user_path(self): # find the best path 
        visited = {}
        unvisited = {}
        print(self.df)
        for node in self.df['distances'].keys(): 
            unvisited[node] = [sys.maxsize, None]

        unvisited[f"{self.current_node}"] = [0, None]
        
        while len(unvisited) > 0: 
            
            current_node = f"{min(unvisited, key=unvisited.get)}"
            neighbours = self.df['distances'][f"{current_node}"]
            for node in neighbours: 
                if node in unvisited.keys(): 
                    cost = unvisited[current_node][0] + neighbours[node]
                    if cost < unvisited[node][0]: 
                        unvisited[node] = [cost, current_node]
            
            visited[current_node] = unvisited[current_node]
            del unvisited[current_node]

        node = visited[str(self.user_node)]
        temporary_node = node[1]
        # print(f"NODE: {node}\nLIST: {visited}")
        # print(f"TEMPORARY NODE: {temporary_node}")
        # print("MY NODE: ", self.current_node)

        path = [self.user_node, node[1]]
        while temporary_node != self.current_node and self.current_node != self.user_node:

            previous_node = visited[temporary_node][1]
            path.append(previous_node)
            temporary_node = visited[temporary_node][1]

        print(f"PATH: {path}\tCURRENT NODE: {self.current_node}")
        return path
