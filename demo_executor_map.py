import time
from concurrent import futures
from time import strftime

def display(*args):
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)


def loiter(n):
    display('{}loiter<{}> did nothing for {}s'.format('\t'*n, n, n) )
    time.sleep(n) 
    display('{}loiter<{}> done.'.format('\t'*n, n, n) )
    return n * 10 # for what?

def main():
    display('Starting Script...')
    #with futures.ThreadPoolExecutor(max_workers=3) as executor:
        #results = executor.map(loiter(i), [i for i in range(5)])
    #    results = executor.map(loiter, range(5))
    executor = futures.ThreadPoolExecutor(max_workers=2)
    results = executor.map(loiter, range(5))
    display('results: ', results)
    display('Wait for individual result:')
    for i, result in enumerate(results):
        display('result {}: {}'.format(i, result))


main()
