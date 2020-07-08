import random

OBSTACLE = 3
FOOD = 4
VEHICLE = 1

class Environment:
    
    def __init__(self, rows, columns, obstacles):
        self.environment = [[0 for column in range(columns)]for row in range(rows)]
        self.environment = self.set_randomly_to_environment(OBSTACLE, obstacles)
        self.environment = self.set_randomly_to_environment(FOOD, 1)
        self.environment = self.set_randomly_to_environment(VEHICLE, 1)
        for row in self.environment:
            print(row)
        
    def set_randomly_to_environment(self, value, amount):
        elements_added = []
        while(len(elements_added) < amount):
            x = random.randint(0, len(self.environment) - 1)
            y = random.randint(0, len(self.environment[0]) - 1)
            if((x, y) not in elements_added):
                self.environment[x][y] = value
                elements_added.append((x, y))
        return self.environment
