class A:
    @staticmethod
    def g(value):
        print value
a = A()
print a.g
print a.__class__.__dict__['g']
print A.g
print A.__dict__['g']
'''
class A:
    def g(self, value):
        self.value = value
        print self.value
a = A()
a.g(10)
A.g(a, 10)
'''
