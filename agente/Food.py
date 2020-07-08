# The "Food" class

class Food():

    def __init__(self, x, y):
        self.velocity = PVector(0, -2)
        self.position = PVector(x, y)
        self.r = 10

    def display(self):
        fill(127)
        noStroke()
        strokeWeight(1)
        with pushMatrix():
            translate(self.position.x, self.position.y)
            rect(0, 0, self.r, self.r)
            stroke(255, 0, 0);
            noFill()
            ellipse(0, 0, 150, 150)
