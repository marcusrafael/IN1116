from Node import Node


class Grid:
    
    def __init__(self, environment):
        self.environment = environment.environment
        self.rows = len(self.environment)
        self.columns = len(self.environment[0])
        self.radius = 2

    def get_color(self, x, y):
        value = self.environment[x][y]
        color_mapping = {
            0: (255, 255, 255),
            1: (255, 0, 0),
            2: (150, 150, 150),
            3: (0, 0, 0),
            4: (100, 100, 255)}
        return color_mapping[value]
        
    def display(self):
        with pushMatrix():
            beginShape()
            xspace = 50
            yspace = 50
            for row in range(self.rows):
                for column in range(self.columns):
                    r, g, b = self.get_color(row, column)
                    fill(r, g, b)
                    ellipse(xspace, yspace, 25, 25)
                    xspace = xspace + 50
                xspace = 50
                yspace += 50
            endShape(CLOSE)
