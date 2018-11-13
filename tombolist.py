import random
from tombola import Tombola

@Tombola.register
class TomboList(list):
    def pick(self):
        if self:
            pos = random.randrange(len(self))
            return self.pop(pos)
        else:
            raise IndexError('pick from empty TomboList')

    load = list.extend # ? how could be called by instance without self ?
    a = 1

    def loaded(self):
        return  bool(self) 

    def inspect(self):
        return tuple(sorted(self))
