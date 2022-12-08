
# Can also be used for storing a point
class Vec2:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)
    
    __rmul__ = __mul__
    
    def __div__(self, other):
        return self * (1/other)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not (self == other)
    
    def __str__(self):
        return "({},{})".format(self.x, self.y)
    
    
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


class RectCollider:
    def __init__(self, center_x, center_y, half_w, half_h, rotation):
        self.center_x = center_x
        self.center_y = center_y
        self.half_w = half_w
        self.half_h = half_h
        self.rotation = rotation


    def recalculate_points(self):
        self.points = []
        self.points.append(Vec2(center_x + half_w, center_y + half_h))
        self.points.append(Vec2(center_x - half_w, center_y + half_h))
        self.points.append(Vec2(center_x + half_w, center_y - half_h))
        self.points.append(Vec2(center_x - half_w, center_y - half_h))