import pygame, sys, json, pprint

class Enemy(pygame.sprite.Sprite): 
    def __init__(self, x, y, positions, graph): 
        pygame.sprite.Sprite.__init__(self)
        self.current_animation = "idle" # idle
        self.frame = 0
        self.graph = graph
        self.df = positions
        self.current_node = "0"
        self.attacking_images = self.get_images("images/undead-executioner-attack", 13)
        self.idle_images = self.get_images("images/undead-executioner-idle", 4)
        self.animations = {
            "attacking": self.attacking_images, 
            "idle": self.idle_images
        }
        self.image = self.animations[self.current_animation][0]
        self.rect =self.image.get_rect()
        self.rect.center = (self.df[f"{self.current_node}"])
        self.next_positions = {"0":[]}
        self.path = []


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
        if len(self.path) > 1 and len(self.next_positions) > 1: 
                
            if len(self.next_positions[(self.current_node)]) == 0: 
                del self.path[-1]
                del self.next_positions[str(self.current_node)]
                self.current_node = self.path[-1]

            self.rect.center = self.next_positions[self.current_node][0]
            del self.next_positions[self.current_node][0]
        # print(f"PATH: {self.path}")
        # print(f"POSITIONS: {self.next_positions}")
        # next_coordinates = self.df[self.next_node]
        # self.rect.center = (next_coordinates[0], next_coordinates[1])
        # self.current_node = self.next_node

    def find_denominations(self): 
        for index in range(len(self.path)-1, 0, -1): 
            current = self.path[index]
            next = self.path[index-1]
            current_position = self.df[f"{current}"]
            next_position = self.df[f"{next}"]
            x_denoms = (next_position[0] - current_position[0])/18
            y_denoms = (next_position[1] - current_position[1])/18
            temp_list = []
            for i in range(1, 13): 
                next_pos = ((i * x_denoms) + current_position[0], (i * y_denoms) + current_position[1])
                temp_list.append(next_pos)
                self.next_positions.setdefault(f"{current}", temp_list)

    def find_user(self, user_node):
        visited = {}
        unvisited = {}
        for node in self.graph.keys(): 
            unvisited[node] = [sys.maxsize, None]

        if len(self.next_positions[f"{self.current_node}"]) != 0: 
            next_node = self.path[-2]
            unvisited[f"{next_node}"] = [0, None]
        else: 
            unvisited[f"{self.current_node}"] = [0, None]

        while len(unvisited) > 0: 
            
            current_node = f"{min(unvisited, key=unvisited.get)}"
            neighbours = self.graph[f"{current_node}"]
            for node in neighbours: 
                if node in unvisited.keys(): 
                    cost = unvisited[current_node][0] + neighbours[node]
                    if cost < unvisited[node][0]: 
                        unvisited[node] = [cost, current_node]
            
            visited[current_node] = unvisited[current_node]
            del unvisited[current_node]

        node = visited[str(user_node)]
        temporary_node = node[1]
        path = [node[1]]
            
        while temporary_node != self.current_node:

            previous_node = visited[temporary_node][1]
            path.append(previous_node)
            temporary_node = visited[temporary_node][1]

        self.path = path
        self.find_denominations()
