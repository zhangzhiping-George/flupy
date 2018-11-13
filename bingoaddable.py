import itertools

from tombola import Tombola
from bingo import BingoCage

class AddableBingoCage(BingoCage):
    def __add__(self, other):
        if isinstance(other, Tombola):
            # re construct a new one
            return AddableBingoCage(self.inspect() + other.inspect()) 
        else:
            return NotImplemented
    def __iadd__(self, other):
        if isinstance(other, Tombola):
            other_iterable = other.inspect() 
        else:
            try:
                other_iterable= iter(other)
            except TypeError:
                errmsg = 'right operand in += must be {cls.__name__} or iterable'
                raise TypeError(errmsg.format(cls=type(self)))
        self.load(other_iterable)
        return self


aBc = AddableBingoCage('asdfa')         
aBc2 = AddableBingoCage('werqwe')         
print('aBc.inspect():', aBc.inspect())
aBc += 'werwq'
aBcAdd = aBc + aBc2
print('aBcAdd.inspect(): ', aBcAdd.inspect())
#aBcAdd2 = aBc + 'asdf'
aBc += 123
