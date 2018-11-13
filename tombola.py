import abc

class Tombola(abc.ABC):
    '''
    class Tombola(metaclass=abc.ABCMeta): # python(3 ~ 3.4)
    class Tombola(object):          # python 2
        __metaclass__ = abc.ABCMeta # Python 2
    '''
    @abc.abstractmethod
    def load(self, iterable):
        '''generate elements from iterable project'''

    @abc.abstractmethod
    def pick(self):
        '''remove element randomly'''

    def loaded(self):
        return bool(self.inspect())

    def inspect(self):
        items = [] 
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break 
        self.load(items)
        return tuple(sorted(items))
