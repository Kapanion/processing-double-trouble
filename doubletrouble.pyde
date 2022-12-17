from scenes import SceneManager
             
def setup():
    global scene_manager
    global st
    st = ""
    size(1280, 720)
    scene_manager = SceneManager()

def draw():
    # print("-------------- FRAME {} -----------------".format(frameCount))
    
    global scene_manager
    background(255)
    scene_manager.update()
    scene_manager.display()

def keyPressed():
    global scene_manager
    scene_manager.key_pressed()

def keyReleased():
    global scene_manager
    scene_manager.key_released()

def keyTyped():
    global scene_manager
    scene_manager.key_typed()
    
def mouseClicked():
    global scene_manager
    scene_manager.mouse_clicked()
