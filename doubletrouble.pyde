from maze import Maze
import collision as cl
from gameplay import Tank, Game
from input import InputHandler
             
def setup():
    global game
    size(505, 505)
    game = Game(2)

def draw():
    global game
    # print("-------------- FRAME {} -----------------".format(frameCount))
    background(255)
    game.update()
    game.display()

def keyPressed():
    global game
    game.input.key_pressed()

def keyReleased():
    global game
    game.input.key_released()
