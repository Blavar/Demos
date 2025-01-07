from math import sqrt

#   a 2D vector class
class Vector:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def set(self, x, y):
        self.x = x
        self.y = y

    def isNull(self):
        return self.x == 0 and self.y == 0

    def __neg__(self):
        return Vector( -self.x, -self.y )
    def __add__(self, w):
        return Vector( self.x + w.x, self.y + w.y )
    def __sub__(self, w):
        return Vector( self.x - w.x, self.y - w.y )
    def __mul__(self, k):
        return Vector( self.x*k, self.y*k )
    def __div__(self, k):
        return Vector( self.x/k, self.y.k )
    
    def dot(self, v):
        self.x *= v.x
        self.y *= v.y
   
    def __eq__(self, w):
        return self.x == w.x and self.y == w.y   
   
    def __str__(self):
        return f'x:{self.x} y:{self.y}'
    

    def length(self):
        return sqrt( self.x**2 + self.y**2 )
    
    def lenghtSquared(self):
        return self.x**2 + self.y**2
    

    def normalized(self):
        #keep in mind how this goes
        if not self.isNull():
            l = self.length()
            return Vector( self.x / l, self.y / l )

    def to_pair(self):
        return (int(self.x), int(self.y))

Vector.null = Vector( 0, 0)
Vector.up   = Vector( 0,-1)
Vector.down = Vector( 0,+1)
Vector.right= Vector(+1, 0)
Vector.left = Vector(-1, 0)