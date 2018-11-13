class A:    
    def ping(self):
        print('ping: ', self)

class B(A):
    def pong(self):
        print('pong:', self)

class C(A):
    def pong(self):
        print('PONG:', self)

class D(B, C):
    def ping(self):
        super().ping()
        print('post ping: ', self)

    def pingpong(self):
        self.ping()
        super().pong()
        C.pong(self)


d = D()
d.ping()
d.pong()
d.pingpong()
print(','.join(c.__name__ for c in D.__mro__))
