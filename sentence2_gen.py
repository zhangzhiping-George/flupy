import re
from collections import abc
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(self.text)

    def __repr__(self):
        return '{cls.__name__}({args})'.format(cls=type(self), args=reprlib.repr(self.text))

    def __iter__(self):
        for word in self.words:
            yield word


#class SentenceIterator:
#    def __init__(self, words):
#        self.words= words 
#        self.index = 0
#
#    def __next__(self):
#        try: 
#            word = self.words[self.index]
#        except IndexError:
#            raise StopIteration()
#        self.index += 1
#        return word
#    def __iter__(self):
#        return self
#        
        
s = Sentence('The negative and the anxious emotion help nothing, it kills')
print('s: ', s)
print('list property: ', list(s))
iters = iter(s)
print('iters:',next(iters))
#ERR: print('len(iters):',len(iters))
#ERR: print('iters:',iters[0])
