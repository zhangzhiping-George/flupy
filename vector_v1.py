from math import hypot, atan2, sqrt
from array import array
import reprlib


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

    def __eq__(self, other):
        return tuple(self) == tuple(other) 

    def __mul__(self, scalar):
        return Vector2d([x*scalar for x in self._components])
    
    def __bool__(self):
        return bool(abs(self)) 

    def __abs__(self):
        return sqrt(sum(x*x for x in self._components))

    def __len__(self):
        return len(self._components)

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
v3 = Vector2d(range(10))
print(v1)
print('len(v1):',len(v1))
print(v1 == v2)
print(v3)
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
v3.x = 7
