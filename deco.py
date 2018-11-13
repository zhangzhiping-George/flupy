def deco(func):
    def inner():    
        print('running deco innner')
    return inner

@deco
def func():
    print('running func')

func()
