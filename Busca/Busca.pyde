import time
import Search

def setup():
    global search
    size(800, 600)
    search = Search.Search()
    
def draw():
    background(255)
    #search.bfs()
    #search.dfs()
    #search.ucs()
    search.gbfs()
    #search.aStar()
    search.path()
    search.display()
    time.sleep(0.1)
