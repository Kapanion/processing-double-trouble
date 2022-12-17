from collision import Vec2

UI_DEFAULT_COLOR = color(68)

minim = None

def set_minim(mnm):
    global minim
    minim = mnm

class UIElement:
    def __init__(self, pos, sz):
        self.pos = pos
        self.sz = sz

    def display(self):
        fill(UI_DEFAULT_COLOR)
        noStroke()
        rect(self.pos.x, self.pos.y, self.sz.x, self.sz.y)

    def check_mouse_overlap(self):
        return self.pos.x <= mouseX <= self.pos.x + self.sz.x \
                and self.pos.y <= mouseY <= self.pos.y + self.sz.y

    def mouse_clicked(self):
        pass


    def key_typed(self):
        pass


class Button(UIElement):
    def __init__(self, img, on_pressed, pos, sz = Vec2()*0):
        sz = sz if sz != Vec2()*0 else Vec2(img.width, img.height)
        UIElement.__init__(self, pos, sz)
        self.img = img
        self.on_pressed = on_pressed
        self.sound = minim.loadFile("./sounds/click.wav")

    def display(self):
        image(self.img, self.pos.x, self.pos.y, self.sz.x, self.sz.y)

    
    def mouse_clicked(self):
        if self.check_mouse_overlap():
            self.on_pressed()
            self.sound.rewind()
            self.sound.play()
    
    @staticmethod
    def print_pressed():
        print("Pressed.")


class BackButton(Button):
    def __init__(self, on_pressed):
        Button.__init__(self, loadImage("./images/button_back.png"), on_pressed, Vec2()*20, Vec2()*50)


class InputField(UIElement):
    def __init__(self, pos, sz, placeholder = "Input text..."):
        UIElement.__init__(self, pos, sz)
        self.selected = False
        self.text_length_limit = 15
        self.text = ""
        self.placeholder = placeholder


    def get_input(self):
        return self.text #if len(self.text) > 0 else self.placeholder


    def display(self):
        UIElement.display(self)
        textSize(30)
        fill(255)
        textAlign(CENTER, CENTER)
        display_text = self.text
        if len(display_text) == 0:
            display_text = self.placeholder
            fill(200)

        text(display_text, *(self.pos + self.sz / 2))


    def mouse_clicked(self):
        self.selected = self.check_mouse_overlap()


    def key_typed(self):
        if self.selected:
            if key == BACKSPACE:
                if len(self.text) > 0:
                    self.text = self.text[:-1]
            else:
                if len(self.text) < self.text_length_limit - 1:
                    self.text += key
