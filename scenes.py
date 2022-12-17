class Scene:
    def __init__(self):
        pass
    
    def update(self):
        pass

    def display(self):
        pass

    def key_pressed(self):
        pass

    def key_released(self):
        pass

    def key_typed(self):
        pass

    def mouse_clicked(self):
        pass


from gameplay import Game
from collision import Vec2
from ui import Button


class Menu(Scene):
    def __init__(self, on_play, on_lbrd = Button.print_pressed):
        self.bg_img = loadImage('./images/bgimage.png')
        self.button_play = Button(loadImage('./images/play.png'), on_play, Vec2(360, 300))
        self.button_lbrd = Button(loadImage('./images/leaderboard.png'), on_lbrd, Vec2(360, 500))

    
    def display(self):        
        image(self.bg_img, 0,0)
        self.button_play.display()
        self.button_lbrd.display()


    def mouse_clicked(self):
        self.button_play.check_click()
        self.button_lbrd.check_click()


class Leaderboard(Scene):
    def __init__(self):
        self.data = []
        with open("./leaderboard.csv", "r") as f:
            lines = f.readlines()
            for line in lines:
                name, score = map(str.strip, line.split(','))
                self.data.append((name, score))
        print(self.data)
        

    def display(self):
        x = 130
        textSize(30)
        fill(0)
        for i, (name, score) in enumerate(self.data):
            textAlign(RIGHT, CENTER)
            text(name, x - 5, i * 40 + 30)
            textAlign(LEFT, CENTER)
            text(score, x + 5, i * 40 + 30)


class SceneManager:
    def __init__(self):
        self.open_menu()
        # self.scene = Leaderboard()


    def start_game(self):
        self.scene = Game(2)


    def open_menu(self):
        self.scene = Menu(self.start_game)


    def scene_is(self, cls):
        return isinstance(self.scene, cls)
        

    def update(self):
        self.scene.update()

    def display(self):
        self.scene.display()

    def key_pressed(self):
        self.scene.key_pressed()

    def key_released(self):
        self.scene.key_released()

    def key_typed(self):
        self.scene.key_typed()

    def mouse_clicked(self):
        self.scene.mouse_clicked()
