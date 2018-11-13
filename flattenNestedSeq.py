from collections import Iterable

def flatten(items, ignore_type=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_type):
            yield from flatten(x) 
        else:
            yield x

#nestedseq = [1, 2, [3, 4], [5, 6]]
nestedseq = ['a', 'b', ['sam', 'Jack'], ['Tony', 'xx']]

for i in flatten(nestedseq):
    print(i)
 
