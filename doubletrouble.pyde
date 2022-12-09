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
rect1 = cl.RectCollider(200, 200, 5, 5)
rect2 = cl.RectCollider(200, 200, 50, 50)
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
    # rect1.c = cl.Vec2(mouseX, mouseY)
    
    # if mousePressed:
    #     rect1.rot += 0.03
    
    col1 = False
    for wall in mz.walls:
        if tank1.check_collision(wall):
            col1 = True

    col2 = False
    for wall in mz.walls:
        if tank2.check_collision(wall):
            col2 = True

    if tank1.check_collision(tank2):
        col1 = False
        col2 = False
            
        
    # col = rect1.check_collision(rect2)
    # print(col)
    # print(",".join(map(str,[k for k,v in input.keys_pressed[0].items() if v])))
    # textSize(20)
    # fill(0)
    # text(str(mouseX), 70,30)
    # text(str(mouseY), 130,30)

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


    # rect1.display_debug()
    tank1.display_debug()
    tank2.display_debug()
    # rect2.display_debug()

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
    
