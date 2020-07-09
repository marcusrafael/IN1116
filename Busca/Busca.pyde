from Search import Search

def setup():
    global search
    size(800, 600)
    search = Search()
    
def draw():
    background(255)
    search.display()
