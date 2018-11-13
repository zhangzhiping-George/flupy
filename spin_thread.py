import sys
import time
import itertools
import threading

class Signal:
    go = True # attribute <go> can be controlled from outside 

def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08'*len(status))
        time.sleep(.3)
        if not signal.go:
            break
    write(' '*len(status)+'\x08'*len(status))

def slow_function():
    time.sleep(3)
    return 42

def supervisor():
    signal = Signal()
    #signal = True # fail to control from outside
    tasks = threading.Thread(target=spin, args=('thinking..', signal))
    print('spinner: ', tasks)
    tasks.start()
    result = slow_function()
    signal.go = False
    #signal = False
    tasks.join()
    return result

def main():
    result = supervisor()
    print('Answer: ', result)


if __name__ == '__main__':
    main()
