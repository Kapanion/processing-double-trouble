from maze import Maze
import collision as cl

mz = Maze(5,5)
rect1 = cl.RectCollider(200, 200, 50, 50)
rect2 = cl.RectCollider(200, 200, 50, 50)

def setup():
    size(500, 500)
    background(255)
    noStroke()
    fill(0)

def draw():
    background(255)
    # mz.display()
    rect1.c = cl.Vec2(mouseX, mouseY)
    
    if mousePressed:
        rect1.rot += 0.03
    
    col = rect1.check_collision(rect2)
    # print(col)
    textSize(20)
    fill(0)
    text(str(mouseX), 70,30)
    text(str(mouseY), 130,30)

    if col:
        fill(255,0,0)
    else:
        fill(0,255,0)
    noStroke()
    circle(30, 30, 30)


    rect1.display_debug()
    rect2.display_debug()
