from math import hypot

class Vector:
    def __init__(self, x=0, y=0):
        self.x = float(x) 
        self.y = float(y)
        
    def __repr__(self):
        return "Vector(%r, %r)" %(self.x, self.y)

    def __str__(self):
        return "Vector(%r, %r)" %(self.x, self.y)

    def __add__(self, other):
        self.x = self.x + other.x 
        self.y = self.y + other.y 
        return Vector(self.x, self.y)

    def __mul__(self, scalar):
        return Vector(self.x*scalar, self.y*scalar)
    
    def __bool__(self):
        return bool(abs(self)) 

    def __abs__(self):
        return hypot(self.x, self.y) 


v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = v1 + v2
v4 = v2*3
print(type(Vector))
print(Vector)
print('v1.x: ', v1.x)
print(v3)
print(v4)
print(abs(v2))
print(bool(v2))
