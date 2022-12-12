DEBUG_PRINT = False

# Can also be used for storing a point
class Vec2:
    def __init__(self, x = 1, y = 1):
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

    def orthogonal(self):
        return Vec2(-self.y, self.x)
    
    
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


class Collider:
    TYPE_STATIC = 0
    TYPE_DYNAMIC = 1
    TYPE_TRIGGER = 2
    def __init__(self, center, rotation, tp):
        self.c = center
        self.rot = rotation
        self.type = tp
        self.callback = None

    def set_callback(self, callback):
        if self.type != TYPE_TRIGGER:
            raise Exception("Callback can be updated only to a trigger.")
        self.callback = callback

    def check_collision(self, other):
        if self.type == Collider.TYPE_STATIC:
            raise Exception("Collision cannot be checked on a static object.")
        self.prepare_for_collision()
        other.prepare_for_collision()
        col_status, mpv = check_collision(self, other)
        if col_status:
            if other.type == Collider.TYPE_STATIC:
                self.c += mpv
            else:
                self.c += 0.5 * mpv
                other.c -= 0.5 * mpv
                
        return col_status


class PolygonCollider(Collider):
    def __init__(self, points):
        self.points = points


    def get_axes(self):
        return polygon_edges(self.points)

    def recalculate_points(self):
        pass

    def prepare_for_collision(self):
        self.recalculate_points()

    def projection_range(self, ortho):
        return polygon_projection_range(ortho, self.points)


    def display_debug(self, clr = color(0, 255, 0) ):
        noFill()
        stroke(clr)
        self.recalculate_points()
        draw_polygon(self.points)


## approximation of a circle with a polygon
class CirclePolyCollider(PolygonCollider):
    def __init__(self, center, radius, num_vert, rotation = 0, tp = Collider.TYPE_STATIC):
        Collider.__init__(self, center, rotation, tp)
        self.radius = radius
        self.num_vert = num_vert
        self.recalculate_points()

    def recalculate_points(self):
        top = self.c + Vec2(0, -self.radius)
        self.points = [top.rotate(self.c, PI*2/self.num_vert*i) for i in range(self.num_vert)]



class RectCollider(PolygonCollider):
    def __init__(self, center, half_w, half_h, rotation = 0, tp = Collider.TYPE_STATIC):
        # center
        self.c = center
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


    def get_axes(self):
        axes = []
        for i in range(2):
            axes.append(self.points[i+1] - self.points[i])

        return axes


### Convex polygon collision/intersection

def draw_polygon(points):
    n = len(points)
    for i in range(n):
        u = points[i]
        v = points[(i+1)%n]
        line(u.x, u.y, v.x, v.y)

def polygon_edges(points):
    edges = []
    n = len(points)
    for i in range(n):
        edges.append(points[(i+1)%n] - points[i])

    return edges


def centers_displacement(poly1, poly2):
    c1 = sum(poly1, Vec2(0.0, 0.0)) / float(len(poly1))
    c2 = sum(poly2, Vec2(0.0, 0.0)) / float(len(poly2))
    return c2 - c1


def polygon_projection_range(ortho, points):
    mn, mx = float('+inf'), float('-inf')
    for v in points:
        projection_magnitude = v.dot(ortho)

        mn = min(mn, projection_magnitude)
        mx = max(mx, projection_magnitude)

    return mn, mx


def separating_axis(ortho, col1, col2):
    min1, max1 = col1.projection_range(ortho)
    min2, max2 = col2.projection_range(ortho)

    if max1 < min2 or max2 < min1:
        # no overlap
        return True, None

    d = min(max1 - min2, max2 - min1)
    sqr_mag = ortho.sqr_magnitude()
    pv = ortho * (d / sqr_mag + 1e-10)
    return False, pv


def check_collision(col1, col2):
    axes = col1.get_axes() + col2.get_axes()
    orthos = map(Vec2.orthogonal, axes)

    push_vectors = []
    for ortho in orthos:
        sep, pv = separating_axis(ortho, col1, col2)

        if sep:
            return False, None

        push_vectors.append(pv)

    mpv = min(push_vectors, key=Vec2.sqr_magnitude)
    
    d = centers_displacement(col1.points, col2.points) # direction from p1 to p2
    if d.dot(mpv) > 0: # if it's the same direction, then invert
        mpv = -mpv

    return True, mpv
