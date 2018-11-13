import time
import functools

register = set()

# factorial = clocked(factorial)
DEF_FMT = '<{escape:8f}s {name} {arg_str} -> {result}>'
def clock(fmt=DEF_FMT):
    def decorate(func):
        #@functools.wraps(func)
        def clocked(*args, **kwds):
            t0 = time.perf_counter() 
            result = func(*args, **kwds)
            escape = time.perf_counter() - t0
            args_str = ','.join([str(arg) for arg in args])
            kwds_str = ','.join(['%s=%s' %(str(k), str(v)) for k, v in kwds.items()])
            arg_str = args_str + ',' + kwds_str 
            name = func.__name__
            #print('%.8fs %s %s -> %s' %(escape, name, arg_str, result))
            print(fmt.format(**locals()))
            return result
        return clocked 
    return decorate
'''
@clock
def f(*args, **kwds):
    return sum(args) + sum(kwds.values())

f(1,2,3, x=4)
'''
if __name__ == '__main__':
    @functools.lru_cache()
    @clock(fmt='<{escape:8f}s {arg_str} -> {result}>')
    def fib(n):
        if n < 2:
            return n 
        else:
            return fib(n-2) + fib(n-1)
    fib(20)
