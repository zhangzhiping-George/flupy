#!/usr/bin/python

import sys

def g():
    frame = sys._getframe()
    print 'frame fun: ', frame.f_code.co_name
    caller = frame.f_back
    print 'frame f_back fun: ', caller.f_code.co_name
    print 'caller local namespace: ', caller.f_locals
    print 'caller global namespace: ', caller.f_globals

    
def f():
    a = 1
    b = 2
    g()

f()
