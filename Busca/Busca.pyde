import Search

def setup():
    global search
    size(800, 600)
    search = Search.Search()
    
def draw():
    background(255)
    search.solve()
    search.path()
    search.display()
