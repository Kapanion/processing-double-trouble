from maze import Maze
import collision as cl
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
             

mz = Maze(5,5)
input = InputHandler()
tank1 = Tank(0, input, 250, 250, 30, 40)
tank2 = Tank(1, input, 350, 250, 30, 40)

def setup():
    size(505, 505)
    background(255)
    noStroke()
    fill(0)

def draw():
    background(255)


    tank1.update()
    tank2.update()
    ### Maze check
    mz.display()
    
    ### Collision check
    col1 = mz.check_collision(tank1)
    col2 = mz.check_collision(tank2)

    tank1.check_collision(tank2)
        # col1 = False
        # col2 = False
            
        
    if col1:
        fill(255,0,0)
    else:
        fill(0,255,0)
    noStroke()
    circle(30, 30, 30)

    if col2:
        fill(255,0,0)
    else:
        fill(0,255,0)
    noStroke()
    circle(63, 30, 30)
    
    tank1.display_debug()
    tank2.display_debug()
    

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
    
