from collision import RectCollider, Vec2
from animation import Animation, StateMachine, Animator
from maze import Maze
from input import InputHandler

import random

TANK_SPEED = 2
TANK_ROT_SPEED = 0.06



class Tank(RectCollider):
    def __init__(self, plr_id, input_handler, center, half_size):
        rot = random.uniform(0, 2*PI)
        RectCollider.__init__(self, center.x, center.y, half_size.x, half_size.y, rot, RectCollider.TYPE_DYNAMIC)
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


class Game:
    def __init__(self, num_plr = 2):
        self.maze = Maze(5,5)
        self.input = InputHandler()
        self.tanks = []
        pos = self.maze.rand_pos_in_biggest_component(num_plr)
        for i in range(num_plr):
            self.tanks.append(Tank(i, self.input, pos[i], Vec2(15, 20)))

    def update(self):
        for tank in self.tanks:
            tank.update()

        for tank in self.tanks:
            self.maze.check_collision(tank)

        for i, tank in enumerate(self.tanks):
            for j in range(i+1, len(self.tanks)):
                tank.check_collision(self.tanks[j])

    def display(self):
        self.maze.display()

        for tank in self.tanks:
            tank.display()
            # tank.display_debug()
