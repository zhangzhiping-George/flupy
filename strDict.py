import collections
class StrDict(collections.UserDict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]
    def __contains__(self, key):
        return str(key) in self.data 
    def __setitems__(self, key, value):
        self.data[str(key)] = value 

strdict = StrDict([('a', 1)])
strdict
strdict[1]='a'
strdict
strdict[1]
