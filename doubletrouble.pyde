from gameplay import Game
             
def setup():
    global game
    size(1280, 720)
    game = Game(2)

def draw():
    # print("-------------- FRAME {} -----------------".format(frameCount))
    
    global game
    background(255)
    game.update()
    game.display()

def keyPressed():
    global game
    game.input().key_pressed()

def keyReleased():
    global game
    game.input().key_released()
