

class InputHandler():
    def __init__(self):
        dct1 = {UP: False, DOWN: False, RIGHT: False, LEFT: False}
        dct2 = {UP: False, DOWN: False, RIGHT: False, LEFT: False}
        self.keys_pressed = [dct1, dct2] #for two players
    
    def clear(self):
        self.keys_pressed = [{}, {}] #for two players
    
    def check(self, plr_id, k):
        return self.keys_pressed[plr_id][k]
