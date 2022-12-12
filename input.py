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

class InputHandler():
    def __init__(self):
        dct1 = {UP: False, DOWN: False, RIGHT: False, LEFT: False}
        dct2 = {UP: False, DOWN: False, RIGHT: False, LEFT: False}
        self.keys_pressed = [dct1, dct2] #for two players
    
    def clear(self):
        self.keys_pressed = [{}, {}] #for two players
    
    def check(self, plr_id, k):
        return self.keys_pressed[plr_id][k]

    def key_pressed(self):
        if key == CODED:
            self.keys_pressed[1][keyCode] = True
        else:
            if key not in input_map:
                return
            self.keys_pressed[0][input_map[key]] = True



    def key_released(self):
        if key == CODED:
            self.keys_pressed[1][keyCode] = False
        else:
            if key not in input_map:
                return
            self.keys_pressed[0][input_map[key]] = False
    

