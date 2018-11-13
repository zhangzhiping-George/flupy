import json
from collections import abc
import keyword

from osconfeed import load

class FrozenJSON:

    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        #self.__data = dict(mapping) 
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)

        else:
            return FrozenJSON(self.__data[name])

raw_feed = load()
#print(json.dumps(raw_feed['Schedule']['conferences'][:2], indent=4))
#print(json.dumps(raw_feed['Schedule']['speakers'][:2], indent=4))
#print(json.dumps(raw_feed['Schedule']['events'][:2], indent=4))
print(json.dumps(raw_feed['Schedule']['venues'][:3], indent=4))

'''
feed = FrozenJSON(raw_feed)

print(feed.Schedule.keys())
print(feed.Schedule.events[40].name)
print(feed.Schedule.events[40].speakers)
print(feed.Schedule.speakers[-1].name)

for key, value in sorted(feed.Schedule.items()):
    print('{:3} {}'.format(len(value), key))
'''
