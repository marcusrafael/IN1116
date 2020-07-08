from Grid import Grid
from Environment import Environment

def setup():
    global grid
    size(800, 600)
    environment = Environment(rows=10, columns=15, obstacles=1)
    grid = Grid(environment)

def draw():
    background(255)
    grid.display()
