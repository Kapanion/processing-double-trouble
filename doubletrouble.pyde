from gameplay import GameManager
             
def setup():
    global game
    size(1280, 720)
    game = GameManager()

def draw():
    # print("-------------- FRAME {} -----------------".format(frameCount))
    
    global game
    background(255)
    game.update()
    game.display()

def keyPressed():
    global game
    game.key_pressed()

def keyReleased():
    global game
    game.key_released()

def mouseClicked():
    global game
    game.mouse_clicked()
