import random
from collision import RectCollider, Vec2

DCS = 16      # desired component size
WALL_SZ = 6
CELL_SZ = 100

dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

class Wall(RectCollider):
    def __init__(self, x, y, w, h):
        self.debug_color = color(0,255,0)
        RectCollider.__init__(self, x + w/2.0, y + h/2.0, w/2.0, h/2.0)


    def display(self):
        # background(255)
        fill(0)
        rect(self.c.x - self.hs.x, self.c.y - self.hs.y, self.hs.x * 2, self.hs.y * 2)
        self.display_debug(self.debug_color)
        self.debug_color = color(0,255,0)


class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.walls = []
        # For each cell, corresponding walls will be stored
        # (walls that should be checked for collision) 
        self.cell_walls = [[[] for _ in range(cols)] for _ in range(rows)]
        self.generate_maze()


    def change_component(self, r, c, comp):
        if r >= self.rows or c > self.cols:
            return 0
        if self.cell_component[r][c] == comp:
            return 0

        self.component_size[self.cell_component[r][c]] -= 1
        self.component_size[comp] += 1
        self.cell_component[r][c] = comp
        for i, (dr, dc) in enumerate(dirs):
            nr, nc = r + dr, c + dc
            if r < nr or c < nc:
                if self.maze[r][c][i%2]:
                    continue
            if r > nr or c > nc:
                if self.maze[nr][nc][i%2]:
                    continue
            self.change_component(nr, nc, comp)


    def add_to_cell_walls(self, wall, r, c, dr, dc):
        for wr in range(max(r-dr,0), min(r+2,self.rows)):
            for wc in range(max(c-dc,0), min(c+2, self.cols)):
                self.cell_walls[wr][wc].append(wall)


    def update_walls(self):
        self.walls = []
        self.cell_walls = [[[] for _ in range(self.cols)] for _ in range(self.rows)]

        wall_left = Wall(0, 0, WALL_SZ, self.cols * CELL_SZ)
        self.walls.append(wall_left)
        for c in range(self.cols):
            self.cell_walls[0][c].append(wall_left)

        wall_top = Wall(0, 0, self.rows * CELL_SZ, WALL_SZ)
        for r in range(self.rows):
            self.cell_walls[r][0].append(wall_top)
        self.walls.append(wall_top)

        for r in range(self.rows):
            for c in range(self.cols):
                if self.maze[r][c][0]:
                    wall_down = Wall((r+1)*CELL_SZ, c*CELL_SZ, WALL_SZ, CELL_SZ + WALL_SZ)
                    self.add_to_cell_walls(wall_down, r, c, 0, 1)
                    self.walls.append(wall_down)
                if self.maze[r][c][1]:
                    wall_right = Wall(r*CELL_SZ, (c+1)*CELL_SZ, CELL_SZ + WALL_SZ, WALL_SZ)
                    self.add_to_cell_walls(wall_right, r, c, 1, 0)
                    self.walls.append(wall_right)


    def generate_maze(self):
        self.maze = [[[True, True] for _ in range(self.cols)] for _ in range(self.rows)]
        self.cell_component = [[i*self.cols + j for j in range(self.cols)] for i in range(self.rows)]
        self.component_size = [1 for _ in range(self.cols*self.rows)]
        while True:
        # for _ in range(DCS):
            rem_r, rem_c, rem_d = 0,0,0
            while True:
                rem_r = random.randint(0, self.rows-1)
                rem_c = random.randint(0, self.cols-1)
                rem_d = random.randint(0,1)
                if not self.maze[rem_r][rem_c][rem_d]:
                    continue
                if rem_r == self.rows-1 and rem_d == 0 \
                        or rem_c == self.cols-1 and rem_d == 1:
                    continue
                break
            # print(rem_r, rem_c, rem_d)
            self.maze[rem_r][rem_c][rem_d] = False
            nr = rem_r + dirs[rem_d][0]
            nc = rem_c + dirs[rem_d][1]
            self.change_component(nr, nc, self.cell_component[rem_r][rem_c])
            if self.component_size[self.cell_component[rem_r][rem_c]] > DCS:
                break

        self.update_walls()


    def check_collision(self, target):
        # all collisions have to be checked to move
        # the object to an approppriate location
        r, c = (target.c / int(CELL_SZ)).to_int().as_tuple()
        col = False
        for wall in self.cell_walls[r][c]:
            wall.debug_color = color(255,0,0)
            if target.check_collision(wall):
                col = True
        return col


    def display(self):
        fill(0)
        for wall in self.walls:
            wall.display()


    def __str__(self):
        res = "+-" * self.cols + '+\n'
        for r in range(self.rows):
            res += '| ' + " ".join('|' if self.maze[r][c][1] else ' ' \
                    for c in range(self.cols)) + '\n'
            res += '+' + "+".join('-' if self.maze[r][c][0] else ' ' \
                    for c in range(self.cols)) + '+\n'
        return res



# maze = Maze(5, 5)
# print(maze)
# print(maze.maze)
