SHOOT = 69

PLR_ACTIONS = [UP, DOWN, RIGHT, LEFT, SHOOT]

input_map = [
    { # plr 1
        "W": UP,
        "w": UP,
        "S": DOWN,
        "s": DOWN,
        "A": LEFT,
        "a": LEFT,
        "D": RIGHT,
        "d": RIGHT,
        "H": SHOOT,
        "h": SHOOT,
    },
    { # plr 2
        " ": SHOOT,
        UP: UP,
        DOWN: DOWN,
        RIGHT: RIGHT,
        LEFT: LEFT,
    },
]

class InputHandler():
    def __init__(self):
        dct1 = {action: False for action in PLR_ACTIONS}
        dct2 = {action: False for action in PLR_ACTIONS}
        self.keys_pressed = [dct1, dct2] #for two players
    
    def clear(self):
        self.keys_pressed = [{}, {}] #for two players
    
    def check(self, plr_id, k):
        return self.keys_pressed[plr_id][k]

    @staticmethod
    def interpret_key():
        k = keyCode if key == CODED else key
        for i in range(len(input_map)):
            if k in input_map[i]:
                return i, input_map[i][k]
        return None, None

    def key_pressed(self):
        plr_id, action = InputHandler.interpret_key()
        if plr_id is None: return
        self.keys_pressed[plr_id][action] = True

    def key_released(self):
        plr_id, action = InputHandler.interpret_key()
        if plr_id is None: return
        self.keys_pressed[plr_id][action] = False

    def reset_action(self, plr_id, action):
        self.keys_pressed[plr_id][action] = False


    # def key_pressed_old(self):
    #     if key == CODED:
    #         self.keys_pressed[1][keyCode] = True
    #     else:
    #         if key not in input_map[0]:
    #             return
    #         self.keys_pressed[0][input_map[0][key]] = True


    # def key_released_old(self):
    #     if key == CODED:
    #         self.keys_pressed[1][keyCode] = False
    #     else:
    #         if key not in input_map:
    #             return
    #         self.keys_pressed[0][input_map[key]] = False
    
