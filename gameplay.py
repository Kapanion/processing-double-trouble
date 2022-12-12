from collision import Collider, RectCollider, CirclePolyCollider, Vec2
from animation import Animation, StateMachine, Animator
from maze import Maze
from input import InputHandler

import random

TANK_SPEED = 2
TANK_ROT_SPEED = 0.06
BULLET_COL = color(0)
BULLET_SPEED = 12.0/6.0


class Bullet(CirclePolyCollider):
    def __init__(self, pos, v):
        self.diameter = 8
        CirclePolyCollider.__init__(self, pos, self.diameter / 2.0, 8, Collider.TYPE_TRIGGER)
        self.v = v
        # self.v = (self.pos + Vec2(0.0, 1.0)).rotate(self.pos, rot).normalized() * BULLET_SPEED
        # print "{} {}  {}".format(self.pos, rot, self.v)

    def update(self):
        self.c += self.v
        pass

    def bounce(self, mx, my):
        self.v = Vec2(self.v.x * mx, self.v.y * my)

    def display(self):
        fill(BULLET_COL)
        circle(self.c.x, self.c.y, self.diameter)


class Turret:
    def __init__(self, inst_bullet):
        self.img = loadImage("./images/Gun_05.png")
        self.inst_bullet = inst_bullet
        self.w = 15
        self.h = 35


    def shoot(self, pos, rot):
        bullet = Bullet(pos, rot)
        self.inst_bullet(bullet)


    def display(self, pos):
        # imageMode should be CENTER!!!
        stroke(0)
        strokeWeight(5)
        image(self.img, pos.x, pos.y - 5, self.w, self.h)
        noStroke()
        strokeWeight(1)


class Tank(RectCollider):
    def __init__(self, plr_id, input_handler, center, half_size, inst_bullet):
        rot = random.uniform(0, 2*PI)
        RectCollider.__init__(self, center, half_size.x, half_size.y, rot, Collider.TYPE_DYNAMIC)
        # CirclePolyCollider.__init__(self, center, half_size.x, 6, 0, Collider.TYPE_DYNAMIC)
        self.input_handler = input_handler
        self.img = loadImage("./images/Hull_06.png")
        self.plr_id = plr_id
        self.is_moving = True
        self.turret = Turret(inst_bullet)
        # self.inst_bullet = inst_bullet

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


    def shoot(self):
        pos = (self.c + Vec2(0.0, -self.hs.y)).rotate(self.c, self.rot)
        # print self.c, pos
        self.turret.shoot(pos, (pos-self.c).normalized() * BULLET_SPEED)


    def update(self):
        if frameCount == 200:
            self.shoot()
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
        with pushMatrix():
            translate(*self.c)
            rotate(self.rot)
            translate(*(-self.c))
            imageMode(CENTER)
            image(self.img, self.c.x, self.c.y, self.hs.x*2+2, self.hs.y*2+1)
            self.turret.display(self.c)
            imageMode(CORNER)

            # track = self.animator.get_current_frame()
            # if track is not None:
            #     image(track, x-3, y-3, self.hs.x/2.0, self.hs.y*2 + 6)
            # self.animator.display(Vec2(x+50, y+50))
            # rect(x, y, *(self.hs*2).as_tuple())

        # self.display_debug()


class Game:
    def __init__(self, num_plr = 2):
        self.maze = Maze(5,5)
        self.input = InputHandler()
        self.tanks = []
        self.bullets = []
        pos = self.maze.rand_pos_in_biggest_component(num_plr)
        for i in range(num_plr):
            self.tanks.append(Tank(i, self.input, pos[i], Vec2(15, 20), self.instantiate_bullet))


    def instantiate_bullet(self, bullet):
        self.bullets.append(bullet)

    def update(self):
        for tank in self.tanks:
            tank.update()

        for bullet in self.bullets:
            bullet.update()

        for tank in self.tanks:
            self.maze.check_collision(tank)

        for bullet in self.bullets:
            status, mpv = self.maze.check_collision(bullet)
            if status:
                mx, my = (-1, 1) if mpv.x != 0 else (1, -1)
                bullet.bounce(mx, my)

        for i, tank in enumerate(self.tanks):
            for j in range(i+1, len(self.tanks)):
                tank.check_collision(self.tanks[j])

    def display(self):
        self.maze.display()

        for tank in self.tanks:
            tank.display()
            # tank.display_debug()

        for bullet in self.bullets:
            bullet.display()
