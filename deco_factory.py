register = set()
def clock(active=True):
    def deco(func):
        print('runing register func <%s>' %func)
        if active:
            register.add(func) 
        else:
            register.discard(func) 
    return deco

@clock()
def func1(*args):
    print(list(args))


@clock(active=False)
def func2(*args):
    print(list(args))

print(register)

