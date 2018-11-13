import collections

#class Mydict(dict):
class Mydict(collections.UserDict):
    def __getitem__(self, key):
        return 'xx'

    def __setitem__(self, k, v):
        # self[k] = [v]*2 # infinite recursion, called by self
        super().__setitem__(k, [v]*2)

d = Mydict(one=1) # __init__: ignored subclass __setitem__
d[1] = 'd' 
print("d: ", d)
print("d[1]: ", d[1])

d.update(three=3) # __update__; ignored it too
print("d: ", d)
du = {}
du.update(d)
print("du: ", du)

