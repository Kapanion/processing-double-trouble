from collision import RectCollider, Vec2

TANK_SPEED = 2
TANK_ROT_SPEED = 0.06

class Tank(RectCollider):
    def __init__(self, plr_id, input_handler, x, y, w, h):
        RectCollider.__init__(self, x + w/2.0, y + h/2.0, w/2.0, h/2.0, 0, RectCollider.TYPE_DYNAMIC)
        self.input_handler = input_handler
        self.plr_id = plr_id

    def update(self):
        # print(self.input_handler.check(self.plr_id, UP))
        if self.input_handler.check(self.plr_id, LEFT):
            self.rot -= TANK_ROT_SPEED
        if self.input_handler.check(self.plr_id, RIGHT):
            self.rot += TANK_ROT_SPEED           
        if self.input_handler.check(self.plr_id, UP):
            self.c += Vec2(0, -1).rotate(Vec2(0.0, 0.0), self.rot) * TANK_SPEED
        if self.input_handler.check(self.plr_id, DOWN):
            self.c += Vec2(0, 1).rotate(Vec2(0.0, 0.0), self.rot) * TANK_SPEED
            
