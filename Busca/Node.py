
class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = 0
        self.edges = []

    def __repr__(self):
        return "({},{}) : {}".format(self.x, self.y, [(node.x, node.y) for node in self.edges])
