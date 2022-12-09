import random

DCS = 16      # desired component size
WALL_SZ = 6
CELL_SZ = 50

dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
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


    def display(self):
        rect(0, 0, WALL_SZ, self.cols * CELL_SZ)
        rect(0, 0, self.rows * CELL_SZ, WALL_SZ)
        for r in range(self.rows):
            for c in range(self.cols):
                if self.maze[r][c][0]:
                    rect((r+1)*CELL_SZ, c*CELL_SZ, WALL_SZ, CELL_SZ)
                if self.maze[r][c][1]:
                    rect(r*CELL_SZ, (c+1)*CELL_SZ, CELL_SZ, WALL_SZ)


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
