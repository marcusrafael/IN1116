import time
import random
import sys
from ctypes import c_int64

from Node import Node

def increment(number):
    number.value += 1
    return number.value

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
        self.foodX = None
        self.foodY = None
        self.grid = self.create()
        self.add(OBSTACLE, self.obstacles)
        self.add(FOOD)
        self.add(VEHICLE)

        self.queue = [self.vehicle]
        self.stack = [self.vehicle]
        self.priority = [self.vehicle]
        
        # for row in range(self.rows):
        #     for column in range(self.columns):
        #         print(self.grid[row][column].state)

    def create(self):
        index = c_int64(0)
        grid = [[Node(row,column,increment(index)) for column in range(self.columns)] for row in range(self.rows)]
        
        for row in range(self.rows):
            for column in range(self.columns):
                if(column < self.columns - 1): # vai pra direita
                    grid[row][column].neighbors.append(grid[row][column + 1])
                    grid[row][column].neighbors_costs[grid[row][column + 1].index] = random.randint(1,4)
                if(column > 0): # vai para esquerda
                    grid[row][column].neighbors.append(grid[row][column - 1])
                    grid[row][column].neighbors_costs[grid[row][column - 1].index] = random.randint(1,4)
                if(row < self.rows - 1): # desce
                    grid[row][column].neighbors.append(grid[row + 1][column])
                    grid[row][column].neighbors_costs[grid[row + 1][column].index] = random.randint(1,4)
                if(row > 0): # sobe
                    grid[row][column].neighbors.append(grid[row - 1][column])
                    grid[row][column].neighbors_costs[grid[row - 1][column].index] = random.randint(1,4)
                if(row < self.rows - 1 and column < self.columns - 1): # diagonal esquerda descendo
                    grid[row][column].neighbors.append(grid[row + 1][column + 1])
                    grid[row][column].neighbors_costs[grid[row + 1][column + 1].index] = random.randint(1,4)
                if(row > 0 and column > 0): # diagonal esqueda subindo
                    grid[row][column].neighbors.append(grid[row - 1][column - 1])
                    grid[row][column].neighbors_costs[grid[row - 1][column - 1].index] = random.randint(1,4)
                if(row > 0 and column < self.columns - 1): # diagonal direita subindo
                    grid[row][column].neighbors.append(grid[row - 1][column + 1])
                    grid[row][column].neighbors_costs[grid[row - 1][column + 1].index] = random.randint(1,4)
                if(row < self.rows - 1 and column > 0): # diagonal direita descendo
                    grid[row][column].neighbors.append(grid[row + 1][column - 1])
                    grid[row][column].neighbors_costs[grid[row + 1][column - 1].index] = random.randint(1,4)
        
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
                if(state == FOOD):
                    self.foodX = x
                    self.foodY = y
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
    def ucs(self):
        if(self.priority):
            minIndex = self.minDistance(self.priority)
            current = self.priority.pop(minIndex)
       
            for node in current.neighbors:
                if(node.state == FOOD):
                    self.food = current
                    self.priority = []
                    break
                if(node.state == NOT_VISITED):
                    self.priority.append(node)
                    node.state = VISITED
                    node.parent = current
     
    def gbfs(self):
        if(self.queue):
            current = self.queue.pop()
            minIndex = self.minLocalCost(current.neighbors, current)
            
            while(minIndex < 0):
                current = current.parent
                minIndex = self.minLocalCost(current.neighbors, current)
            
            if(current.neighbors[minIndex].state == FOOD):
                self.food = current
                self.queue = []
                
            if(current.neighbors[minIndex].state == NOT_VISITED):
                self.queue.append(current.neighbors[minIndex])
                current.neighbors[minIndex].state = VISITED
                current.neighbors[minIndex].parent = current
    def aStar(self):
        if(self.priority):
            minIndex = self.minDistanceHeuristic(self.priority)
            current = self.priority.pop(minIndex)
       
            for node in current.neighbors:
                if(node.state == FOOD):
                    self.food = current
                    self.priority = []
                    break
                if(node.state == NOT_VISITED):
                    self.priority.append(node)
                    node.state = VISITED
                    node.parent = current
                    
    def minLocalCost(self, neighbors, parent):
        minValue = sys.maxint
        minIndex = -1 
        for id, n in enumerate(neighbors):
            if(n.state == NOT_VISITED or n.state == FOOD):
                food = self.grid[self.foodX][self.foodY]
                heuristic = dist(n.x, n.y, self.foodX, self.foodY)
                line(n.grid_x, n.grid_y, food.grid_x, food.grid_y)
                if(heuristic < minValue):
                    minValue = heuristic
                    minIndex = id
        return(minIndex)

    def minDistance(self, nodes):
        minValue = sys.maxint
        minIndex = 0 
        for id, n in enumerate(nodes):
            if(self.relativeCost(n) < minValue):
                minValue = self.relativeCost(n)
                minIndex = id 
        return(minIndex)

    def minDistanceHeuristic(self, nodes):
        minValue = sys.maxint
        minIndex = 0 
        cost = 0
        for id, n in enumerate(nodes):
            food = self.grid[self.foodX][self.foodY]
            heuristic = dist(n.x, n.y, self.foodX, self.foodY)
            line(n.grid_x, n.grid_y, food.grid_x, food.grid_y)
            cost = self.relativeCost(n) + heuristic
            if(cost < minValue):
                minValue = cost
                minIndex = id 
        return(minIndex)

    def relativeCost(self, current):
       tempCurrent = current 
       cost = 0
       while(tempCurrent.index != self.vehicle.index):
           if(tempCurrent.parent != None):
               cost += tempCurrent.parent.neighbors_costs[tempCurrent.index] 
               tempCurrent = tempCurrent.parent
       return(cost)

    def path(self):
        if(self.food):
            if(self.food.state != VEHICLE):
                self.food.state = PATH
                self.food = self.food.parent
            else:
                self.again()

    def again(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if(self.grid[row][column].state == FOOD):
                    self.grid[row][column].state = VEHICLE
                    self.vehicle = self.grid[row][column]
                elif(self.grid[row][column].state in [VISITED, VEHICLE, PATH]):
                    self.grid[row][column].state = NOT_VISITED

        self.food = None
        self.queue = [self.vehicle]
        self.stack = [self.vehicle]
        self.priority = [self.vehicle]
        self.add(FOOD)

    def display(self):
        with pushMatrix():
            beginShape()
            xspace = 50
            yspace = 50
            for row in range(self.rows):
                for column in range(self.columns):
                    self.grid[row][column].grid_x = xspace
                    self.grid[row][column].grid_y = yspace
                    value = self.grid[row][column].state
                    r, g, b = COLORS[value]
                    fill(r, g, b)
                    ellipse(xspace, yspace, 25, 25)
                    xspace = xspace + 50
                xspace = 50
                yspace += 50
            endShape(CLOSE)
