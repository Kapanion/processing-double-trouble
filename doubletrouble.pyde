from maze import Maze

mz = Maze(5,5)

def setup():
    size(500, 500)
    background(255)
    noStroke()
    fill(0)

def draw():
    mz.display()
