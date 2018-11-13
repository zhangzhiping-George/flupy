import re
from collections import abc
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:
    def __init__(self, text):
        self.text = text
        #self.words = RE_WORD.findall(self.text)

    def __repr__(self):
        return '{cls.__name__}({args})'.format(cls=type(self), args=reprlib.repr(self.text))

    def __iter__(self):
        #for word in RE_WORD.finditer(self.text):
        #    yield word.group()

        # generator expression '()' replaced <yield>
        return (word for word in RE_WORD.finditer(self.text))


s = Sentence('The negative and the anxious emotion help nothing, it kills')
print('s: ', s)
print('list property: ', [i.group() for i in s])
iters = iter(s)
print('iters:',next(iters))
#ERR: print('len(iters):',len(iters))
#ERR: print('iters:',iters[0])
