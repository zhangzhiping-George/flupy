from math import hypot, atan2
from array import array

class Vector2d:

    typecode = 'd'
    def __init__(self, x=0, y=0):
        self.__x = float(x) 
        self.__y = float(y)

    @property
    def x(self):
        return self.__x
        
    @property
    def y(self):
        return self.__y
        
    def __iter__(self):
        return (i for i in (self.x, self.y))

    #def __str__(self):
    #    return str(tuple(self))

    def __repr__(self):
        class_name = type(self).__name__ 
        return "{}({!r}, {!r})".format(class_name, *self)

    def __add__(self, other):
        m = self.x + other.x 
        n = self.y + other.y 
        return Vector2d(m,n)

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(array(self.typecode, self)))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        print(memv)
        return cls(*memv)

    def __eq__(self, other):
        return tuple(self) == tuple(other) 

    def __mul__(self, scalar):
        return Vector2d(self.x*scalar, self.y*scalar)
    
    def __bool__(self):
        return bool(abs(self)) 

    def __abs__(self):
        return hypot(self.x, self.y) 

    def angle(self):
        return atan2(self.x, self.y) 

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):
            coords = (abs(self), self.angle()) 
            outer_fmt = fmt_spec[:-1]
            #return '<{}, {}>'.format(*(format(c, fmt_spec[:-1])  for c in (abs(self), self.angle())))
        else:
            #return '<{}, {}>'.format(*(format(c, fmt_spec) for c in self))
            outer_fmt = fmt_spec
            coords = (self.x, self.y) 
        components = (format(c, outer_fmt) for c in coords)
        return '<{}, {}>'.format(*components)
    
    def __hash__(self):
        return hash(self.x)^hash(self.y)

v1 = Vector2d(1, 2)
v2 = Vector2d(3, 4)
print('v1: ', v1)
v3 = v1 + v2
print('v2: ', v2)
print('v3(v1 + v2): ', v3)
print('v1: ', v1)
print('hash(v3):', hash(v3))
print('hash(v2):', hash(v2))
print('hash(v1):', hash(v1))
v4 = v2*3
print(type(Vector2d))
print(Vector2d)
print('v1.x: ', v1.x)
print('v1.__dict__:', v1.__dict__)
print(v1)
print(bytes(v1))
print(v2 == [3, 4])
print(v4)
print(abs(v2))
print(bool(v2))
v5 = Vector2d()
print(v5.frombytes(b'd\x00\x00\x00\x00\x00\x00\x10@\x00\x00\x00\x00\x00\x00\x18@'))
print('4 format spec==============')
print(format(v3))
print(format(v3, 'p'))
print(format(v3, '.3ep'))
print(format(v3, '.2f'))

v = Vector2d(1/3, 2/5)
print(bytes(v))
class ShortVector2d(Vector2d):
    typecode = 'f'

sv = ShortVector2d(1/3, 2/5)
print(bytes(sv))
