import random

from Node import Node


NOT_VISITED = 0
VISITED = 1
OBSTACLE = 2
FOOD = 3
VEHICLE = 4
PATH = 5

COLORS = {
    NOT_VISITED: (255, 255, 255), # branco
    VISITED: (150, 0, 0), # vermelho escuro
    OBSTACLE: (0, 0, 0), # preto
    FOOD: (0, 0, 255), # azul
    VEHICLE: (255, 0, 0), # vermelho
    PATH: (0, 255, 0)} # verde


class Search:

    def __init__(self, rows=10, columns=15, obstacles=50):
        self.rows = rows
        self.columns = columns
        self.obstacles = obstacles
        self.food = None
        self.vehicle = None
        self.grid = self.create()
        self.add(OBSTACLE, self.obstacles)
        self.add(FOOD)
        self.add(VEHICLE)

        self.queue = [self.vehicle]
        self.stack = [self.vehicle]
        
        # for row in range(self.rows):
        #     for column in range(self.columns):
        #         print(self.grid[row][column].state)

    def create(self):
        grid = [[Node(row,column) for column in range(self.columns)] for row in range(self.rows)]
        for row in range(self.rows):
            for column in range(self.columns):
                if(column < self.columns - 1): # vai pra direita
                    grid[row][column].neighbors.append(grid[row][column + 1])
                if(column > 0): # vai para esquerda
                    grid[row][column].neighbors.append(grid[row][column - 1])
                if(row < self.rows - 1): # desce
                    grid[row][column].neighbors.append(grid[row + 1][column])
                if(row > 0): # sobe
                    grid[row][column].neighbors.append(grid[row - 1][column])
                if(row < self.rows - 1 and column < self.columns - 1): # diagonal esquerda descendo
                    grid[row][column].neighbors.append(grid[row + 1][column + 1])
                if(row > 0 and column > 0): # diagonal esqueda subindo
                    grid[row][column].neighbors.append(grid[row - 1][column - 1])
                if(row > 0 and column < self.columns - 1): # diagonal direita subindo
                    grid[row][column].neighbors.append(grid[row - 1][column + 1])
                if(row < self.rows - 1 and column > 0): # diagonal direita descendo
                    grid[row][column].neighbors.append(grid[row + 1][column - 1])
        return grid

    def add(self, state, amount=1):
        added = 0
        while(added < amount):
            x = random.randint(0, len(self.grid) - 1)
            y = random.randint(0, len(self.grid[0]) - 1)
            node = self.grid[x][y]
            is_not_visited = node.state == NOT_VISITED
            if(is_not_visited):
                node.state = state
                if(state == OBSTACLE):
                    for neighbor in self.grid[x][y].neighbors:
                        neighbor.neighbors.remove(node)
                    node.neighbors = []
                if(state == VEHICLE):
                    self.vehicle = node
                added = added + 1

    def bfs(self):
        if(self.queue):
            current = self.queue.pop(0)
            for node in current.neighbors:
                if(node.state == FOOD):
                    self.food = current
                    self.queue = []
                    break
                if(node.state == NOT_VISITED):
                    self.queue.append(node)
                    node.state = VISITED
                    node.parent = current

    def dfs(self):
        if(self.stack):
            current = self.stack.pop()
            for node in current.neighbors:
                if(node.state == FOOD):
                    self.food = current
                    self.stack = []
                    break
                if(node.state == NOT_VISITED):
                    self.stack.append(node)
                    node.state = VISITED
                    node.parent = current

    def path(self):
        if(self.food):
            if(self.food.state != VEHICLE):
                self.food.state = PATH
                self.food = self.food.parent

    def display(self):
        with pushMatrix():
            beginShape()
            xspace = 50
            yspace = 50
            for row in range(self.rows):
                for column in range(self.columns):
                    value = self.grid[row][column].state
                    r, g, b = COLORS[value]
                    fill(r, g, b)
                    ellipse(xspace, yspace, 25, 25)
                    xspace = xspace + 50
                xspace = 50
                yspace += 50
            endShape(CLOSE)
