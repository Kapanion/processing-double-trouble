from collision import Collider, RectCollider, CirclePolyCollider, Vec2
from animation import Animation, StateMachine, Animator
from assets import AssetManager
from maze import Maze, CELL_SZ
from input import InputHandler, SHOOT

import random

TANK_SPEED = 2
TANK_ROT_SPEED = 0.06
BULLET_COLOR = color(0)
BULLET_SPEED = 16/6.0
BULLET_LIFETIME = 10.0 # seconds
BULLET_DIAMETER = 8
BULLET_IMMUNITY = 0.1 # seconds

TURRET_RELOAD_TIME = 5.0 # seconds
TURRET_SHOT_DELAY = 0.15 # seconds
TURRET_AMMO = 5

SECONDS_AFTER_DEATH = 2.0

class Bullet(CirclePolyCollider):
    def __init__(self, plr_id, pos, v):
        self.diameter = BULLET_DIAMETER
        self.death_time = millis() + BULLET_LIFETIME * 1000
        self.spawntime = millis()
        CirclePolyCollider.__init__(self, pos, self.diameter / 2.0, 16, Collider.TYPE_TRIGGER)
        self.v = v
        self.plr_id = plr_id
        self.outside_tank_collider = False
        # self.v = (self.pos + Vec2(0.0, 1.0)).rotate(self.pos, rot).normalized() * BULLET_SPEED
        # print "{} {}  {}".format(self.pos, rot, self.v)


    def destroy(self):
        self.death_time = 0
        # the next update will destroy the bullet

    def bounce(self, mpv):
        # self.v = Vec2(self.v.x * mx, self.v.y * my)
        n = mpv.normalized()
        self.c += mpv
        self.v = self.v - 2 * self.v.dot(n) * n

    def can_damage_owner(self):
        return self.outside_tank_collider \
                or millis() >= self.spawntime + BULLET_IMMUNITY * 1000

    # Returns false if bullet should be destroyed
    def update(self):
        if millis() >= self.death_time:
            return False
        self.c += self.v
        return True

    def display(self):
        fill(BULLET_COLOR)
        circle(self.c.x, self.c.y, self.diameter)


class Turret:
    def __init__(self, plr_id, inst_bullet, img):
        self.img = img
        self.plr_id = plr_id
        self.inst_bullet = inst_bullet
        self.reload()
        self.last_shot = -10000
        self.w = 15
        self.h = 35
        self.visible = True


    def shoot(self, pos, rot):
        if self.ammo < 1 \
                or millis() < self.last_shot + TURRET_SHOT_DELAY * 1000:
            return
        self.ammo -= 1
        self.last_shot = millis()
        bullet = Bullet(self.plr_id, pos, rot)
        self.inst_bullet(bullet)

    def reload(self):
        self.ammo = TURRET_AMMO
        self.next_reload = millis() + TURRET_RELOAD_TIME * 1000

    def update(self):
        if self.ammo < TURRET_AMMO and millis() >= self.next_reload:
            self.reload()


    def display(self, pos):
        if not self.visible: return
        # imageMode should be CENTER!!!
        image(self.img, pos.x, pos.y - 5, self.w, self.h)


class Tank(RectCollider):
    def __init__(self, assets, plr_id, input_handler, center, half_size, inst_bullet, destroy_callback):
        rot = random.uniform(0, 2*PI)
        RectCollider.__init__(self, center, half_size.x, half_size.y, rot, Collider.TYPE_DYNAMIC)
        # CirclePolyCollider.__init__(self, center, half_size.x, 6, 0, Collider.TYPE_DYNAMIC)
        self.input_handler = input_handler
        self.img = assets.hulls[plr_id]
        self.plr_id = plr_id
        self.is_moving = True
        self.turret = Turret(self.plr_id, inst_bullet, assets.turrets[plr_id])
        self.destroyed = False
        self.destroy_callback = destroy_callback
        # self.inst_bullet = inst_bullet

        anim_explode = AssetManager.load_animation("./images/effects/Explosion_{}.png", 8, "explosion")
        anim_explode.set_fps(20);

        anim_explode.no_loop()
        # anim_idle = Animation([self.img], 1, "idle")
        self.anim_explode = anim_explode


    def shoot(self):
        if self.destroyed: return
        y_offs = self.hs.y
        pos = (self.c - Vec2(0.0, y_offs)).rotate(self.c, self.rot)
        # normalized form (magnitude is y_offs)
        norm = (pos-self.c) / y_offs
        self.turret.shoot(pos, norm * BULLET_SPEED)

    def destroy(self):
        self.destroyed = True


    def check_collision(self, other):
        if self.destroyed: return False, None
        return RectCollider.check_collision(self, other)


    def update(self):
        if self.destroyed:
            self.anim_explode.update()
            if self.anim_explode.finished():
                self.destroy_callback(self)
            return

        self.turret.update()

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
        if self.input_handler.check(self.plr_id, SHOOT):
            self.shoot()
            self.input_handler.reset_action(self.plr_id, SHOOT)

        self.is_moving = rot or mov
        # self.animator.update()
    

    def display(self):
        with pushMatrix():
            translate(*self.c)
            rotate(self.rot)
            translate(*(-self.c))
            imageMode(CENTER)
            if self.destroyed:
                self.anim_explode.display(self.c, Vec2() * self.hs.y * 5)
            else:
                image(self.img, self.c.x, self.c.y, self.hs.x*2+2, self.hs.y*2+1)
                self.turret.display(self.c)
            imageMode(CORNER)

            # track = self.animator.get_current_frame()
            # if track is not None:
            #     image(track, x-3, y-3, self.hs.x/2.0, self.hs.y*2 + 6)
            # self.animator.display(Vec2(x+50, y+50))
            # rect(x, y, *(self.hs*2).as_tuple())

        # self.display_debug()


class Match:
    def __init__(self, assets, num_plr = 2, maze_sz = Vec2(8, 5)):
        self.maze = Maze(*maze_sz)
        self.input = InputHandler()
        self.tanks = []
        self.bullets = []
        pos = self.maze.rand_pos_in_biggest_component(num_plr)
        for i in range(num_plr):
            self.tanks.append(Tank(assets, i, self.input, pos[i], Vec2(15, 20), self.instantiate_bullet, self.remove_tank))

        self.over_time = -1
        self.over = False


    def instantiate_bullet(self, bullet):
        self.bullets.append(bullet)

    def remove_tank(self, tank):
        # print("Removing {}".format(tank))
        self.tanks.remove(tank)
        if len(self.tanks) < 2:
            self.over_time = millis() + SECONDS_AFTER_DEATH * 1000

    def winner_id(self):
        if not self.over:
            raise Exception("winner_id() cannot be called if the game is not over yet.")
        if len(self.tanks) != 0:
            return self.tanks[0].plr_id
        return None

    def update(self):
        if self.over_time != -1 and millis() >= self.over_time:
            self.over = True
            return

        for tank in self.tanks:
            tank.update()

        for i, bullet in enumerate(self.bullets):
            st = bullet.update()
            if not st:
                self.bullets.pop(i)

        for tank in self.tanks:
            self.maze.check_collision(tank)

        for bullet in self.bullets:
            status, mpv = self.maze.check_collision(bullet)
            if status:
                # mx, my = (-1, 1) if mpv.x != 0 else (1, -1)
                bullet.bounce(mpv)

        # for ti, tank in enumerate(self.tanks):
        #     for bi, bullet in enumerate(self.bullets):
        #         st, _ = tank.check_collision(bullet)
        #         if bullet.plr_id == tank.plr_id:
        #             if not st:
        #                 bullet.outside_tank_collider = True
        #             if not bullet.can_damage_owner():                    continue
        #         if st:
        #             # one bullet cannot destroy two tanks on one frame
        #             tank.destroy()
        #             bullet.destroy()
        #             # self.tanks.pop(ti)
        #             self.bullets.pop(bi)
        #             break

        for i, tank in enumerate(self.tanks):
            for j in range(i+1, len(self.tanks)):
                tank.check_collision(self.tanks[j])

    def display(self):
        with pushMatrix():
            offs = Vec2(width - CELL_SZ * self.maze.rows, height - CELL_SZ * self.maze.cols) / 2.0
            translate(*offs)
            
            self.maze.display()
    
            for tank in self.tanks:
                tank.display()
                # tank.display_debug()
    
            for bullet in self.bullets:
                bullet.display()
                
            translate(*(-offs))


class Game:
    def __init__(self, num_plr):
        self.assets = AssetManager()
        self.num_plr = num_plr
        self.new_match()
        self.score = [0] * num_plr


    def new_match(self):
        mz_sz = Vec2(random.randint(3, 8), random.randint(3,5))
        self.match = Match(self.assets, self.num_plr, mz_sz)

    def input(self):
        return self.match.input


    def update(self):
        self.match.update()
        if self.match.over:
            winner_id = self.match.winner_id()
            if winner_id is not None:
                self.score[winner_id] += 1

            self.new_match()


    def display_score(self):
        textSize(40)
        textAlign(CENTER, CENTER)
        imageMode(CENTER)
        dx = 200
        for plr in range(self.num_plr):
            pos = Vec2(width/2 - dx / 2 * (self.num_plr-1) + plr * dx, height - 40)
            pos -= Vec2(25, 0)
            image(self.assets.hulls[plr], pos.x, pos.y, *Vec2(30, 40) * 1.5)
            image(self.assets.turrets[plr], pos.x, pos.y-5, *Vec2(15, 35) * 1.5)
            pos += 2*Vec2(25, 0)
            text(self.score[plr], *pos)
        imageMode(CORNER)


    def display(self):
        self.match.display()
        self.display_score()


class Menu:
    def __init__(self, gm):
        self.bg_img = loadImage('./images/bgimage.png')
        self.play_img = loadImage('./images/play.png')
        self.leaderboard_img = loadImage('./images/leaderboard.png')
        self.on_play_pressed = gm.start_game


    def update(self):
        pass

    
    def display(self):        
        image(self.bg_img, 0,0)
        image(self.play_img, 360,300)
        image(self.leaderboard_img, 360,500)

    def mouse_clicked(self):
        if 360 < mouseX < 360 + 550 and 300 < mouseY < 450:
            self.on_play_pressed()
        elif 360 < mouseX < 360 + 550 and 500 < mouseY < 650:
            print ("Clicked Leaderboard")


class GameManager:
    MENU = 0
    GAME = 1
    LEADERBOARD = 2

    def __init__(self):
        self.open_menu()

    def start_game(self):
        self.state = GameManager.GAME
        self.entity = Game(2)

    def open_menu(self):
        self.state = GameManager.MENU
        self.entity = Menu(self)

    def update(self):
        self.entity.update()

    def display(self):
        self.entity.display()

    def key_pressed(self):
        if self.state == GameManager.GAME:
            self.entity.input().key_pressed()

    def key_released(self):
        if self.state == GameManager.GAME:
            self.entity.input().key_released()

    def mouse_clicked(self):
        if self.state == GameManager.MENU:
            self.entity.mouse_clicked()
