from maze import Maze
import collision as cl
import gameplay
from gameplay import Tank
from input import InputHandler

input_map = {
    "W": UP,
    "w": UP,
    "S": DOWN,
    "s": DOWN,
    "A": LEFT,
    "a": LEFT,
    "D": RIGHT,
    "d": RIGHT,
}
             
def setup():
    global tank1, tank2, input, mz
    size(505, 505)
    print(loadImage("./images/Track_1_A.png"))
    mz = Maze(5,5)
    input = InputHandler()
    tank1 = Tank(0, input, 250, 250, 30, 40)
    tank2 = Tank(1, input, 350, 250, 30, 40)

def draw():
    global tank1, tank2, input, mz
    # print("-------------- FRAME {} -----------------".format(frameCount))
    background(255)

    tank1.update()
    tank2.update()
    
    # ### Collision check
    mz.check_collision(tank1)
    mz.check_collision(tank2)
    tank1.check_collision(tank2)
    
    mz.display()    
    tank1.display()
    tank2.display()
    # tank1.display_debug()
    # tank2.display_debug()
    

def keyPressed():
    if key == CODED:
        input.keys_pressed[1][keyCode] = True
    else:
        if key not in input_map:
            return
        input.keys_pressed[0][input_map[key]] = True


def keyReleased():
    if key == CODED:
        input.keys_pressed[1][keyCode] = False
    else:
        if key not in input_map:
            return
        input.keys_pressed[0][input_map[key]] = False
    
