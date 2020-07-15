NOT_VISITED = 0


class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = NOT_VISITED
        self.parent = None
        self.neighbors = []

    def __repr__(self):
        return "({},{}) : {}".format(self.x, self.y, [(node.x, node.y) for node in self.neighbors])
