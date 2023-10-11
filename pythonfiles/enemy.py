import pygame, sys, json, pprint

class Enemy(pygame.sprite.Sprite): 
    def __init__(self, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.current_animation = "idle" # idle
        self.frame = 0
        self.current_node = "0"
        self.attacking_images = self.get_images("images/undead-executioner-attack", 13)
        self.idle_images = self.get_images("images/undead-executioner-idle", 4)
        self.animations = {
            "attacking": self.attacking_images, 
            "idle": self.idle_images
        }
        self.image = self.animations[self.current_animation][0]
        self.rect =self.image.get_rect()
        self.rect.center = (x, y)


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
        self.image = self.animations[self.current_animation][self.frame]
        self.frame += 1
        if self.frame >= len(self.animations[self.current_animation]): 
            self.frame= 0
            self.current_animation = "idle"
        self.rect.move_ip(1, 0)

    def find_user(self, graph, user_node): 
        visited = {}
        unvisited = {}
        for node in graph.keys(): 
            unvisited[node] = [sys.maxsize, None]

        unvisited[self.current_node] = [0 , None ]
        
        while len(unvisited) > 0: 
            
            current_node = f"{min(unvisited, key=unvisited.get)}"
            neighbours = graph[f"{current_node}"]
            for node in neighbours: 
                if node in unvisited.keys(): 
                    cost = unvisited[current_node][0] + neighbours[node]
                    if cost < unvisited[node][0]: 
                        unvisited[node] = [cost, current_node]
            
            visited[current_node] = unvisited[current_node]
            del unvisited[current_node]

        node = visited[str(user_node)]
            
        temporary_node = node
        path = node

        while temporary_node != self.current_node:

            previous_node = visited[temporary_node][1]
            path = previous_node + path
            temporary_node = visited[temporary_node][1]
        print(f"Path for {node} with cost {visited[node][0]}: ", end="")
        print(path)
        return visited
    


thing = Enemy(300, 300)
with open ("./database/graph.json") as file: 
    dict = json.loads(file.read())
end = thing.find_user(dict, 16)
# pprint.pprint(end)
