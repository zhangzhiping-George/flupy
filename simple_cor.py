def simple_cor(a):
    print('Started with a = ', a)
    b = yield a
    print('-> Received: b=', b)
    c = yield a + b
    print('-> Received: c=', c)

sc = simple_cor(14)
next(sc)
sc.send(11)
sc.send(12)
