from scenes import SceneManager
             
add_library('minim')
minim = Minim(this)

def setup():
    global scene_manager
    size(1280, 720)
    minim = Minim(this)
    import ui
    ui.set_minim(minim)
    import gameplay
    gameplay.set_minim(minim)
    scene_manager = SceneManager()

def draw():    
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
