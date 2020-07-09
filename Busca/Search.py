import random

from Node import Node


NOT_VISITED = 0
VISITED = 1
OBSTACLE = 2
FOOD = 3
VEHICLE = 4

COLORS = {
    NOT_VISITED: (255, 255, 255), # branco
    VISITED: (150, 0, 0), # vermelho escuro
    OBSTACLE: (0, 0, 0), # preto
    FOOD: (0, 0, 255), # azul
    VEHICLE: (255, 0, 0)} # vermelho


class Search:
    
    def __init__(self, rows=10, columns=15, obstacles=25, vehicle=1, food=1):
        self.rows = rows
        self.columns = columns
        self.obstacles = obstacles
        self.vehicle = vehicle
        self.food = food
        
        self.environment = self.create_new_environment()
        self.environment = self.add_to_environment(OBSTACLE, self.obstacles)
        self.environment = self.add_to_environment(FOOD, self.food)
        self.environment = self.add_to_environment(VEHICLE, self.vehicle)
        
        for row in self.environment:
            for node in row:
                print(node)

    def create_new_environment(self):
        environment = [[Node(row,column) for column in range(self.columns)] for row in range(self.rows)]
        
        for row in range(self.rows):
            for column in range(self.columns):
        
                node = environment[row][column]

                if(row == 0):
                    if(column == 0):
                        p6 = environment[row][column + 1]
                        p8 = environment[row + 1][column + 1]
                        p9 = environment[row + 1][column]
                        node.edges = [p6, p8, p9]
                    elif(column == self.columns - 1):
                        p4 = environment[row][column - 1]
                        p7 = environment[row + 1][column - 1]
                        p8 = environment[row + 1][column]
                        node.edges = [p4, p7, p8]
                    else:
                        p4 = environment[row][column - 1]
                        p6 = environment[row][column + 1]
                        p7 = environment[row + 1][column - 1]
                        p8 = environment[row + 1][column]
                        p9 = environment[row + 1][column + 1]
                        node.edges = [p4, p6, p7, p8, p9]

                elif(row == self.rows - 1):
                    if(column == 0):
                        p2 = environment[row - 1][column]
                        p3 = environment[row - 1][column + 1]
                        p6 = environment[row][column + 1]
                        node.edges = [p2, p3, p6]
                    elif(column == self.columns - 1):
                        p1 = environment[row - 1][column - 1]
                        p2 = environment[row - 1][column]
                        p4 = environment[row][column - 1]
                        node.edges = [p1, p2, p4]
                    else:
                        p1 = environment[row - 1][column - 1]
                        p2 = environment[row - 1][column]
                        p3 = environment[row - 1][column + 1]
                        p4 = environment[row][column - 1]
                        p6 = environment[row][column + 1]
                        node.edges = [p1, p2, p3, p4, p6]
                
                elif(column == 0):
                    p2 = environment[row - 1][column]
                    p3 = environment[row - 1][column + 1]
                    p6 = environment[row][column + 1]
                    p8 = environment[row + 1][column]
                    p9 = environment[row + 1][column + 1]
                    node.edges = [p2, p3, p6, p8, p9]
                
                elif(column == self.columns - 1):
                    p1 = environment[row - 1][column - 1]
                    p2 = environment[row - 1][column]
                    p4 = environment[row][column - 1]
                    p7 = environment[row + 1][column - 1]
                    p8 = environment[row + 1][column]
                    node.edges = [p1, p2, p4, p7, p8]
                
                else:
                    p1 = environment[row - 1][column - 1]
                    p2 = environment[row - 1][column]
                    p3 = environment[row - 1][column + 1]
                    p4 = environment[row][column - 1]
                    p6 = environment[row][column + 1]
                    p7 = environment[row + 1][column - 1]
                    p8 = environment[row + 1][column]
                    p9 = environment[row + 1][column + 1]
                    node.edges = [p1, p2, p3, p4, p6, p7, p8, p9]
        
        return environment

    def add_to_environment(self, type, amount):
        added = 0
        while(added < amount):
            x = random.randint(0, len(self.environment) - 1)
            y = random.randint(0, len(self.environment[0]) - 1)
            node = self.environment[x][y]
            is_not_visited = node.type == NOT_VISITED
            if(is_not_visited):
                node.type = type
                if(type == OBSTACLE):
                    for edge in self.environment[x][y].edges:
                        edge.edges.remove(node)
                    node.edges = []                   
                added = added + 1
        return self.environment
    
    def display(self):
        with pushMatrix():
            beginShape()
            xspace = 50
            yspace = 50
            for row in range(self.rows):
                for column in range(self.columns):
                    value = self.environment[row][column].type
                    r, g, b = COLORS[value]
                    fill(r, g, b)
                    ellipse(xspace, yspace, 25, 25)
                    xspace = xspace + 50
                xspace = 50
                yspace += 50
            endShape(CLOSE)
