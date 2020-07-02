# The Nature of Code
# Daniel Shiffman
# http://natureofcode.com

# Stay Within Walls
# "Made-up" Steering behavior to stay within walls

from Vehicle import Vehicle
from Food import Food

def setup():
    global v, f, food_x, food_y, c
    food_x = int(random(20, 620))
    food_y = int(random(20, 340))
    size(640, 360)
    v = Vehicle(width / 2, height / 2)
    f = Food(food_x, food_y)
    c = 0


def draw():
    background(255)
    v.boundaries(25)
    v.run()
    distance = dist(f.position.x, f.position.y, v.position.x, v.position.y)
    #print(distance)
    if(distance < 75):
        f.position.x = int(random(20, 620))
        f.position.y = int(random(20, 340))
        global c
        c = c + 1
        print(c)

    f.display()
