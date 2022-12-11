DEBUG_PRINT = False

# Can also be used for storing a point
class Vec2:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
    def __neg__(self):
        return Vec2(-self.x, -self.y)
    
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        return Vec2(self.x * other, self.y * other)
    
    __rmul__ = __mul__
    
    def __div__(self, other):
        return Vec2(self.x / other, self.y / other)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not (self == other)

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("not valid index key '{}'".format(key))

    
    def __str__(self):
        return "({},{})".format(self.x, self.y)



    def to_float(self):
        return Vec2(float(self.x), float(self.y))

    def to_int(self):
        return Vec2(int(self.x), int(self.y))

    def as_tuple(self):
        return (self.x, self.y)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    
    def sqr_magnitude(self):
        return self.x ** 2 + self.y ** 2
    
    def magnitude(self):
        return self.sqr_magnitude() ** 0.5
    
    def sqr_distance(self, other):
        return (self.x - other.x)**2 + (self.y - other.y)**2
    
    def distance(self, other):
        return self.sqr_distance(other) ** 0.5

    # rotate a point in relation to another point
    def rotate(self, origin, angle):
        v = self - origin
        rotated = Vec2(v.x * cos(angle) - v.y * sin(angle), v.x * sin(angle) + v.y * cos(angle))
        return rotated + origin


class RectCollider:
    TYPE_STATIC = 0
    TYPE_DYNAMIC = 1
    def __init__(self, center_x, center_y, half_w, half_h, rotation = 0, tp = TYPE_STATIC):
        # center
        self.c = Vec2(center_x, center_y)
        # half size
        self.hs = Vec2(half_w, half_h)
        self.rot = rotation
        self.recalculate_points()
        self.type = tp


    def recalculate_points(self):
        self.points = [
            Vec2(self.c.x + self.hs.x, self.c.y + self.hs.y),
            Vec2(self.c.x - self.hs.x, self.c.y + self.hs.y),
            Vec2(self.c.x - self.hs.x, self.c.y - self.hs.y),
            Vec2(self.c.x + self.hs.x, self.c.y - self.hs.y),
        ]
        self.points = list(map(lambda v: v.rotate(self.c, self.rot), self.points))


    def check_collision(self, other):
        if self.type == RectCollider.TYPE_STATIC:
            raise Exception("Collision cannot be checked on a static object.")
        self.recalculate_points()
        other.recalculate_points()
        col, mpv = check_collision(self.points, other.points)
        if col:
            if other.type == RectCollider.TYPE_STATIC:
                self.c += mpv
            else:
                self.c += 0.5 * mpv
                other.c -= 0.5 * mpv
                
        return col


    def display_debug(self, clr = color(0, 255, 0) ):
        noFill()
        stroke(clr)
        self.recalculate_points()
        n = len(self.points)
        for i in range(n):
            u = self.points[i]
            v = self.points[(i+1)%n]
            line(u.x, u.y, v.x, v.y)


### Convex polygon collision/intersection

def edges_of(poly):
    edges = []
    n = len(poly)
    for i in range(n):
        edges.append(poly[(i+1)%n] - poly[i])

    return edges


def orthogonal(v):
    return Vec2(-v.y, v.x)


def centers_displacement(poly1, poly2):
    c1 = sum(poly1, Vec2(0.0, 0.0)) / float(len(poly1))
    c2 = sum(poly2, Vec2(0.0, 0.0)) / float(len(poly2))
    return c2 - c1


def separating_axis(ortho, poly1, poly2):
    min1, max1 = float('+inf'), float('-inf')
    min2, max2 = float('+inf'), float('-inf')

    if DEBUG_PRINT: print("Checking axis {}".format(ortho))
    for v in poly1:
        projection_magnitude = v.dot(ortho)
        if DEBUG_PRINT:
            print("Poly1: point {}, proj {}".format(v, projection_magnitude))

        min1 = min(min1, projection_magnitude)
        max1 = max(max1, projection_magnitude)

    for v in poly2:
        projection_magnitude = v.dot(ortho)
        if DEBUG_PRINT:
            print("Poly2: point {}, proj {}".format(v, projection_magnitude))

        min2 = min(min2, projection_magnitude)
        max2 = max(max2, projection_magnitude)

    if max1 < min2 or max2 < min1:
        # no overlap
        return True, None

    if DEBUG_PRINT:
        print("{}: {} {} {} {}".format(frameCount, min1, max1, min2, max2))

    d = min(max1 - min2, max2 - min1)
    sqr_mag = ortho.sqr_magnitude()
    pv = ortho * (d / sqr_mag + 1e-10)
    return False, pv


def check_collision(poly1, poly2):
    # poly1 = [np.array(v, 'float64') for v in poly1]
    # poly2 = [np.array(v, 'float64') for v in poly2]
    poly1 = list(map(lambda v: Vec2(float(v.x), float(v.y)), poly1))
    poly2 = list(map(lambda v: Vec2(float(v.x), float(v.y)), poly2))

    edges = edges_of(poly1) + edges_of(poly2)
    orthos = map(orthogonal, edges)

    push_vectors = []
    for ortho in orthos:
        sep, pv = separating_axis(ortho, poly1, poly2)

        if sep:
            return False, None

        push_vectors.append(pv)

    if DEBUG_PRINT:
        print("{}: rect1: {}".format(frameCount, ",".join(map(str, poly1))))
        print("{}: rect2: {}".format(frameCount, ",".join(map(str, poly2))))

    mpv = min(push_vectors, key=(lambda v: v.sqr_magnitude()))
    
    d = centers_displacement(poly1, poly2) # direction from p1 to p2
    if d.dot(mpv) > 0: # if it's the same direction, then invert
        mpv = -mpv

    return True, mpv
