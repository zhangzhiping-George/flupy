import re
import reprlib
from collections import abc

RE_WORD = re.compile('\w+')
class Sentence:
    def __init__(self, text):
        self.text = text
        self._items = RE_WORD.findall(self.text)

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __repr__(self):
        return '{cls.__name__}({args})'.format(cls=type(self), args=reprlib.repr(self.text))
        
        
s = Sentence('The negative and the anxious emotion help nothing, it kills')

print('s: ', s)
print('len(s): ', len(s))
print('list property: ', [w for w in s])
print(issubclass(Sentence, abc.Iterable))
iters = iter(s)
print(next(iters))
