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


def get_leaderboard_data(path = "./leaderboard.csv"):
    data = []
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            name, score = map(str.strip, line.split(','))
            data.append((name, int(score)))

    return data

def set_leaderboard_data(data, path = "./leaderboard.csv"):
    with open(path, "w") as f:
        for line in data:
            f.write(",".join(map(str, line)) + "\n")


from gameplay import Game
from collision import Vec2
from ui import Button, BackButton, InputField


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
        self.button_play.mouse_clicked()
        self.button_lbrd.mouse_clicked()


class PreGameScene(Scene):
    def __init__(self, on_play, on_back, num_plr = 2):
        self.button_back = BackButton(on_back)
        self.button_play = Button(loadImage('./images/play.png'), on_play, Vec2(360, 450))
        self.input_fields = []
        for i in range(num_plr):
            pos = Vec2(360, 200 + i * 100)
            sz = Vec2(550, 80)
            placeholder = "Enter player {} name...".format(i+1)
            input_field = InputField(pos, sz, placeholder)
            self.input_fields.append(input_field)

    def get_plr_names(self):
        return [field.get_input() for field in self.input_fields]


    def display(self):
        self.button_play.display()
        self.button_back.display()
        for input_field in self.input_fields:
            input_field.display()


    def mouse_clicked(self):
        self.button_play.mouse_clicked()
        self.button_back.mouse_clicked()
        for input_field in self.input_fields:
            input_field.mouse_clicked()


    def key_typed(self):
        for input_field in self.input_fields:
            input_field.key_typed()


class Leaderboard(Scene):
    def __init__(self, on_back):
        self.button_back = BackButton(on_back)
        self.data = get_leaderboard_data()
        

    def display(self):
        textSize(100)
        textAlign(CENTER, TOP)
        x = width / 2
        text("LEADERBOARD", x, 40)
        textSize(40)
        fill(0)
        y = 200
        for i, (name, score) in enumerate(self.data):
            textAlign(RIGHT, CENTER)
            text(name, x - 15, i * 40 + y)
            textAlign(LEFT, CENTER)
            text(score, x + 15, i * 40 + y)

        self.button_back.display()


    def mouse_clicked(self):
        self.button_back.mouse_clicked()


class SceneManager:
    def __init__(self, minim = None, num_plr = 2):
        self.open_menu()
        self.num_plr = num_plr
        self.minim = minim


    def start_game(self):
        names = []
        if self.scene_is(PreGameScene):
            names = self.scene.get_plr_names()
        else:
            names = ["Player {}".format(i+1) for i in range(self.num_plr)]

        self.scene = Game(names, self.open_menu)


    def pre_game(self):
        self.scene = PreGameScene(self.start_game, self.open_menu, self.num_plr)


    def open_menu(self):
        self.scene = Menu(self.pre_game, self.open_lbrd)


    def open_lbrd(self):
        self.scene = Leaderboard(self.open_menu)


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
