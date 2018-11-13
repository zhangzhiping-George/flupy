import random

class LotteryBlower(Tombola)
    def __init__(self, iterable):
        self._balls = list(iterable) 
        
    def load(self, iterable):
        self._balls.extend(iterable)
        
    def pick(self):
        try:
            pos = random.randrange(len(self._balls))
        except IndexError:
            raise LookupError('pick from empty BingoCage')
        return self._balls.pop(pos) 
    
    def loaded(self):
        return bool(self._balls)

    def inpect(self):
        return tuple(sorted(self._balls))
