from collections import namedtuple

Result = namedtuple('Result', 'count average')
def averager():
    count = 0
    total = 0
    average = None
    while True:
        term = yield 
        if term is None:
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average)


def grouper(results, key):
    while True:
        results[key] = yield from averager()

def report(results):
    for key, result in sorted(results.items()):
        gender, unit = key.split(';')
        print('{:5} from {:2} averaging {:3.2f}{}'.format(
        gender, result.count, result.average, unit))

def main(data):
    results = {}
    for key, values in data.items():
        group = grouper(results, key)
        next(group)
        for value in values:
            group.send(value)
        group.send(None)
    report(results)
        


data = {
    'girls;kg':
    [40.5, 38.7, 39.6, 41.2, 43.4, 37.8],
    'girls;m':
    [1.61, 1.53, 1.51, 1.49, 1.54, 1.51],
    'boys;kg':
    [41.5, 39.7, 49.6, 43.2, 45.4, 47.8],
    'boys;m':
    [1.62, 1.63, 1.61, 1.59, 1.59, 1.57]
    }
    

if __name__ == '__main__':
    main(data)


