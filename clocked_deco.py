import time
import functools


# factorial = clocked(factorial)
def clock(func):
    #@functools.wraps(func)
    def clocked(*args, **kwds):
        t0 = time.perf_counter() 
        result = func(*args, **kwds)
        escape = time.perf_counter() - t0
        args_str = ','.join([str(arg) for arg in args])
        kwds_str = ','.join(['%s=%s' %(str(k), str(v)) for k, v in kwds.items()])
        arg_str = args_str + ',' + kwds_str 
        name = func.__name__
        #print('{.8fs} {:5s} {s} -> {s}'.format(escape, name, arg_str, result))
        print('%.8fs %s %s -> %s' %(escape, name, arg_str, result))
        return result
    return clocked 
'''
@clock
def f(*args, **kwds):
    return sum(args) + sum(kwds.values())

f(1,2,3, x=4)
'''
@functools.lru_cache()
@clock
def fib(n):
    if n < 2:
        return n 
    else:
        return fib(n-2) + fib(n-1)
fib(30)
