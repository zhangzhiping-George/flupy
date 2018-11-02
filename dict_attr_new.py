'''
1. Access json-dict value of d[key] with d.key 
2. with __new__ method replace classmethod 
'''
from collections import abc
import keyword

from osconfeed import load

class FrozenJSON:

    def __new__(cls, obj):
        if isinstance(obj, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(obj, abc.MutableSequence):
            return [cls(item) for item in obj]
        else:
            return obj 

    def __init__(self, mapping):
        self.__data = dict(mapping) 
        #self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)

        else:
            return FrozenJSON(self.__data[name])
    
    ## classmethod replaced with metaclass method __new__
    #@classmethod
    #def build_attr(cls, obj):
    #    if isinstance(obj, abc.Mapping):
    #        return cls(obj)
    #    if isinstance(obj, abc.MutableSequence):
    #        return [cls.build_attr(item) for item in obj]
    #    else:
    #        return obj 


fr_returnarg = FrozenJSON({'a':1})
print(fr_returnarg.a)
raw_feed = load()
print(len(raw_feed['Schedule']['events']))

feed = FrozenJSON(raw_feed)

print(feed.Schedule.keys())
print(feed.Schedule.events[40].name)
print(feed.Schedule.events[40].speakers)
print(feed.Schedule.speakers[-1].name)

for key, value in sorted(feed.Schedule.items()):
    print('{:3} {}'.format(len(value), key))
