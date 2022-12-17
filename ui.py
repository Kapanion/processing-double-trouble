from collision import Vec2

class Button:
    def __init__(self, img, on_pressed, pos, sz = Vec2()*0):
        self.img = img
        self.on_pressed = on_pressed
        self.pos = pos
        self.sz = sz if sz != Vec2()*0 else Vec2(img.width, img.height)

    def display(self):
        image(self.img, self.pos.x, self.pos.y, *self.sz)

    def mouse_clicked(self):
        return self.pos.x <= mouseX <= self.pos.x + self.sz.x \
                and self.pos.y <= mouseY <= self.pos.y + self.sz.y

    def check_click(self):
        if self.mouse_clicked():
            self.on_pressed()
    
    @staticmethod
    def print_pressed():
        print("Pressed.")

class BackButton(Button):
    def __init__(self, on_pressed):
        Button.__init__(self, loadImage("./images/button_back.png"), on_pressed, Vec2()*20, Vec2()*50)