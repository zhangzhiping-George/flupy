from functools import wraps
import inspect
def coroutine(func):
    @wraps(func)
    def primer(*arg, **kws):
        gen =  func(*arg, **kws)
        next(gen)
        return gen 
    return primer 

@coroutine
def make_avg():
    total = 0
    count = 0
    average = None # no piece of cake
    while True:
        try:
            term = yield average 
        except ZeroDivisionError:
            print('zero division error catched')
        else:
            total += term
            count +=1
            average = total/count
    print('never get here')

ag = make_avg()
print(inspect.getgeneratorstate(ag))
print(ag.send(10))
ag.throw(ZeroDivisionError)
print(inspect.getgeneratorstate(ag))
print(ag.send(20))
#print(ag.send('xxx'))
ag.close()
print(inspect.getgeneratorstate(ag))
