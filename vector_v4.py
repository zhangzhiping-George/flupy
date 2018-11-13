from math import hypot, atan2, sqrt, pi
from array import array
import reprlib
from functools import reduce
from operator import xor
from itertools import chain
from itertools import zip_longest
import numbers
from fractions import Fraction

class Vector2d:

    typecode = 'd'
    def __init__(self, components):
        self._components = array(self.typecode, components) 

    def __iter__(self):
        return iter(self._components) 

    #def __str__(self):
    #    return str(tuple(self))

    def __repr__(self):
        class_name = type(self).__name__ 
        #components = reprlib.repr(self._components)
        #components = components[components.find('['):-1] 
        return "{}({})".format(class_name, reprlib.repr(list(self._components)))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(array(self.typecode, self)))

    #def __eq__(self, other):
    #    return tuple(self) == tuple(other) 

    #def __eq__(self, other):
    #    if len(self) != len(other):
    #        return False
    #    for a, b in zip(self, other):
    #        if a != b:
    #            return False
    #    return True
    
    # pythonically a lot
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return len(self) == len(other) and \
            all(a == b for a, b in zip(self, other))
        else:
            return NotImplemented

    def __add__(self, other):
        try:
            pairs = zip_longest(self, other, fillvalue=0.0) 
            return Vector2d(a + b for a, b in pairs)
        except TypeError:
            return NotImplemented
    
    def __radd__(self, other):
        return self + other 
    
    def __hash__(self):
        hashvs = map(hash, self._components)
        return reduce(xor, hasvs, 0)


    #def __mul__(self, scalar):
    #    return Vector2d([x*scalar for x in self._components])
    def __mul__(self, scalar):
        if isinstance(scalar, numbers.Real):
            return Vector2d(x*scalar for x in self)
        else:
            return NotImplemented

    def __rmul__(self, scalar):
        return self * scalar
    
    def __matmul__(self, other):
        try:
            return Vector2d(a*b for a, b in zip(self, other))
        except TypeError:
            return NotImplemented

    def __rmatmul__(self, other):
        return self @ other
    
    def __bool__(self):
        return bool(abs(self)) 

    def __len__(self):
        return len(self._components)

    def __abs__(self):
        return sqrt(sum(x*x for x in self._components))

    def angle(self, n):
        r = sqrt(sum(x*x for x in self[n:]))
        a = atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1] <0):
            return pi * 2 - a
        else:
            return a

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))
    
    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('h'):
            fmt_spec = fmt_spec[:-1]
            # bad readability
            # return '<{}>'.format(','.join(format(c, fmt_spec) for c in (chain(abs(self), self.angles()))))
            coord = chain([abs(self)], self.angles())

        else:
            coord = self
        components = (format(c, fmt_spec) for c in coord)
        return '<{}>'.format(','.join(components))
            
        
    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        #elif isinstance(index, numbers.Integral):
        elif isinstance(index, int): 
            return self._components[index]
        else:
            errmsg = '{cls.__name__} indices must be integers'
            raise TypeError(errmsg.format(cls=cls))

    shortcut_names = 'xyzt' 
    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        else:
            errmsg = '{cls.__name__!r} object has no attribute {!r}'
            raise AttributeError(errmsg.format(cls, name))

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortcut_names:
                errmsg = 'readonly attribute {cls.__name__}.{attr_name!r}'
            elif name.islower():
                errmsg = "can't set 'a' to 'z' attribute in {cls.__name__}"
            else:
                errmsg = ''
            if errmsg: 
                raise AttributeError(errmsg.format(cls=cls, attr_name=name)) 
        super().__setattr__(name, value) 

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)

v1 = Vector2d((1,2,3))
v2 = Vector2d([1,2,3])
print("v1 == v2: ", v1 == v2)
print('id(v1):', id(v1))
v1 += v2
print('id(v1):', id(v1))
v1 *= 3 
print('id(v1):', id(v1))
t = (1,2,3)
print("v1: ", v1)
print("v1 == v2: ", v1 == v2)
print(v1 == t)
print('v1@v2: ', v1@v2)
v3 = Vector2d(range(10))
print('v1*3: ', v1*3)
print('3 *v1: ', 3*v1)
print('Fraction(3,4) *v1: ', Fraction(3, 4)*v1)
print(v1)
print(v1 == v2)
print(v3)
print("format(v3, '.2fh'): ", format(v3, '.2fh'))
print(abs(v1))
print(abs(v3))
print(v3[:5:2])
print(v3[5])
print(v3[-1])
#print(v3[1, 2])
print('v3.x: ', v3.x)
print('v3.t: ', v3.t)
v3.M = 7
print('v3.M: ', v3.M)
#v3.x = 7
