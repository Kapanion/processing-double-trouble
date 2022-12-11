from collision import RectCollider, Vec2
from animation import Animation, StateMachine, Animator

TANK_SPEED = 2
TANK_ROT_SPEED = 0.06



class Tank(RectCollider):
    def __init__(self, plr_id, input_handler, x, y, w, h):
        RectCollider.__init__(self, x + w/2.0, y + h/2.0, w/2.0, h/2.0, 0, RectCollider.TYPE_DYNAMIC)
        self.input_handler = input_handler
        self.img = None
        self.plr_id = plr_id
        self.is_moving = True

        track1 = loadImage("./images/Track_1_A.png")
        track2 = loadImage("./images/Track_1_B.png")
        anim_move = Animation([track1, track2], 8, "move")
        anim_idle = Animation([track1], 1, "idle")
        anim = Animator()
        anim.add_animation(anim_move).add_animation(anim_idle)
        print(anim.current_animation.name)
        anim.state_machine.add_transition(0, 1, lambda: not self.is_moving)
        anim.state_machine.add_transition(1, 0, lambda: self.is_moving)
        self.animator = anim



    def update(self):
        # print(self.input_handler.check(self.plr_id, UP))
        mov = False
        rot = False
        if self.input_handler.check(self.plr_id, LEFT):
            self.rot -= TANK_ROT_SPEED
            rot = not rot
        if self.input_handler.check(self.plr_id, RIGHT):
            self.rot += TANK_ROT_SPEED           
            rot = not rot
        if self.input_handler.check(self.plr_id, UP):
            self.c += Vec2(0, -1).rotate(Vec2(0.0, 0.0), self.rot) * TANK_SPEED
            mov = not mov
        if self.input_handler.check(self.plr_id, DOWN):
            self.c += Vec2(0, 1).rotate(Vec2(0.0, 0.0), self.rot) * TANK_SPEED
            mov = not mov

        self.is_moving = rot or mov
        self.animator.update()
    

    def display(self):
        if self.img is None:
            self.img = loadImage("./images/Hull_06.png")
        # if self.img is None: return
        with pushMatrix():
            translate(*self.c)
            rotate(self.rot)
            # scale(2)
            translate(*(-self.c))
            x, y = (self.c - self.hs).as_tuple()
            track = self.animator.get_current_frame()
            image(self.img, x-1, y-1, self.hs.x*2+1, self.hs.y*2+1)
            # if track is not None:
            #     image(track, x-3, y-3, self.hs.x/2.0, self.hs.y*2 + 6)
            # self.animator.display(Vec2(x+50, y+50))
            # rect(x, y, *(self.hs*2).as_tuple())
