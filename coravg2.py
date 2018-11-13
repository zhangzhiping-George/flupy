from functools import wraps
import inspect
from collections import namedtuple
def coroutine(func):
    @wraps(func)
    def primer(*arg, **kws):
        gen =  func(*arg, **kws)
        next(gen)
        return gen 
    return primer 

Result = namedtuple('Result', 'count average')
@coroutine
def coravg():
    total = 0
    count = 0
    average = None # no piece of cake
    while True:
        term = yield average 
        if term is None:
            break
        total += term
        count +=1
        average = total/count
    return Result(count,average) 

ag = coravg()
print(inspect.getgeneratorstate(ag))
print(ag.send(10))
print(ag.send(20))
try:
    print(ag.send(None))
except StopIteration as exc:
    res = exc.value 

print(res)
